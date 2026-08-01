
import pyodbc

# Define variables for connection
SERVER = 'localhost'
DATABASE = 'DB_SmartArchive'

def get_connection():
    # استخدام f-string وتمرير المتغيرات بشكل صحيح
    conn = pyodbc.connect(
        f'DRIVER={{SQL Server}};SERVER={SERVER};DATABASE={DATABASE};Trusted_Connection=yes;'
    )
    return conn

def get_sequence_next_value(sequence_name):
    conn = get_connection()
    cursor = conn.cursor()
    
    # تنفيذ استعلام الـ Sequence
    cursor.execute(f"SELECT NEXT VALUE FOR {sequence_name}")
    next_val = cursor.fetchone()[0]
    
    cursor.close()
    conn.close()
    return next_val

if __name__ == '__main__':
    try:
        conn = get_connection()
        print("Connected to the database successfully!")
        conn.close() 
    except pyodbc.Error as e:
        print("Error while connecting to the database:", e)

