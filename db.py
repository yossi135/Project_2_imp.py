import pyodbc


def connect():
    conn = pyodbc.connect(
        'DRIVER={SQL Server};'
        'SERVER=DESKTOP-7PBRITT\\SQLEXPRESS;'
        'DATABASE=TicketsystemDB;'
        'Trusted_Connection=yes;'
        'TrustServerCertificate=yes;'
    )
    return conn



def execute_query(query, params=()):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute(query, params)
    conn.commit()
    conn.close()


def fetch_query(query, params=()):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()
    return rows
