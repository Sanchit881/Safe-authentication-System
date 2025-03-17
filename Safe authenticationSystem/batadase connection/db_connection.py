import mysql.connector
from mysql.connector import Error
def create_connection():
    try: 
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='sc88@stc',
            database='userlogin'  
        )
        if conn.is_connected():
            print("Connectioin done!")
            return conn
    except Error as e:
        print(f"Error : {e}")
        return None
    


