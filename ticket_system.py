import streamlit as st
from db import execute_query,fetch_query
from security import hash_password ,verify_password
import pandas as pd
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
# Ticket System Application
# This application allows users to create, view, and update tickets.
st.set_page_config(page_title='Ticket System 🎫',layout='wide')

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = None
    st.session_state.role = None
    
def send_email(to_email,subject, message):
    query='''
    SELECT * FROM Users WHERE Username=?'''
    sender_email = "taskmangment62@gmail.com"  
    sender_password = "xeqd jjcg fmnx vmug"  
    #to_email='yossifhendy32@gmail.com'
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        print(f"error  {e}")
        return False
    
def create_ticket(username,title,description):
    query='''
    INSERT INTO Tickets(UserName,Title, Description)
    VALUES (?,?,?)
    '''
    execute_query(query,(username,title,description))

def get_tickets():
    query='''
    SELECT * FROM Tickets
    '''
    ticket=fetch_query(query)
    return ticket 

def view_my_Tickets():
    username= st.session_state.username
    query='''
    SELECT * FROM Tickets WHERE UserName=?
    '''
    tickets=fetch_query(query, (username,))
    return tickets

def update_ticket_status(ticket_id, new_status):
    query = 'UPDATE Tickets SET Status = ? WHERE FormattedID = ?'
    execute_query(query, (new_status, ticket_id))
    
def update_tiket_touser(ticket_id, new_status):
    query=''' UPDATE Tickets SET Status =? WHERE FormattedID= ?'''
    execute_query(query,(new_status,ticket_id))    

def logout():
    st.session_state.logged_in= False
    st.session_state.username = None
    st.session_state.role= None
    st.success('Logged out successfully ✅')
    
def Login():
    st.subheader('Login Page 🔐')
    username_input= st.text_input('Username')
    password_input = st.text_input('Password', type='password')
    
    if st.button('Login'):
         query='''
              SELECT * FROM Users WHERE Username=?
         '''
    
         result=fetch_query(query, (username_input,))
         if not result:
            st.write('User not found ❌')
            return
    
         user_data=result[0]
         hashed_password=user_data.Password
         role=user_data.Role
         if verify_password(password_input,hashed_password):
            st.session_state.logged_in =True
            st.session_state.username= username_input
            st.session_state.role=role
            st.success(f"Login Successful as {username_input} ✅")
         else:
            st.error("❌ Incorrect password")
            

def main_application():
    st.title('Task Mangement')
    query='''SELECT * FROM Users WHERE Username=?'''
    username = st.session_state.username
    st.sidebar.write(f'Welcome {username} 👋')
    result=fetch_query(query, (username,))
    if not result:
        st.write('User not found ❌')
        
    user_data=result[0]
    hashed_password=user_data.Password
    role=user_data.Role
    if role == 'admin':
            menu= st.sidebar.selectbox('Menu',['View Tickets','Update Ticket Status'])
            
            if menu=='Update Ticket Status':
                st.subheader('Update Ticket Status')
                ticket_id = st.text_input('FormattedID')
                new_status= st.selectbox('New Status',['Received','In Progress','it was fixed','Closed'])
                if st.button('Update Status'):
                    if ticket_id and new_status:
                        update_ticket_status(ticket_id, new_status)
                        st.success(f'Ticket {ticket_id} status updated to {new_status} ✅')
                    else:
                        st.error('Please provide Ticket ID and New Status ❌')
            
            elif menu=='View Tickets':
                st.subheader('View Tickets')
                if st.button('Refresh Ticket'):
                    tickets=get_tickets()
                    if tickets:
                      data=[]
                      for i in tickets:
                        data.append({
                            'Ticket ID': i.TicketID,
                            'Title': i.Title,
                            'Description': i.Description,
                            'Status': i.Status,
                            'UserName': i.UserName,
                            'FormattedID':i.FormattedID
                        })
                      st.dataframe(pd.DataFrame(data),use_container_width=True)    
                                             
                    else:
                        st.write('No tickets found ❌')
                            
    # if the user is a regular user
    
    elif role =='user':
        menu= st.sidebar.selectbox('Menu',['Create ticket','View Tickets'])
        if menu=='Create ticket':
            st.subheader('Create Ticket')
            title=st.text_input('Ticket Title')
            description=st.text_area('Ticket Description')
            final_description = f'Hi i am {username},\n\n {description}'
            send_email('ahmed.abdellatif@almada-eg.com',title,final_description)
            if st.button('Crreate Ticket'):
                if title and description:
                    create_ticket(username, title,final_description)
                    st.success('Ticket created successfully ✅')
                else:
                    st.error('Please provide Title and Description ❌')
        elif menu=='View Tickets':
            st.subheader('View Tickets')
            if st.button('Refresh Ticket'):
                tickets=view_my_Tickets()
                data=[]
                if tickets:
                    for i in tickets:
                        data.append({
                            'Ticket ID': i.TicketID,
                            'Title': i.Title,
                            'Description': i.Description,
                            'Status': i.Status,
                            'UserName': i.UserName,
                            'FormattedID': i.FormattedID 
                           
                        })
                    st.dataframe(pd.DataFrame(data),use_container_width=True)    
                else:
                    st.write('No tickets found ❌')    
       
                    
# Add a logout button
st.sidebar.button('Logout', on_click=logout)

if __name__== '__main__':
    st.sidebar.title('Ticket System Menu')
    if not st.session_state.logged_in:
        Login()
    else:
        main_application()
        
 #python -m streamlit run ticket_system.py               