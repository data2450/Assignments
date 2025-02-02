import mysql.connector

def get_db_connection():
    print('1')
    try:
        print('2')
        connection = mysql.connector.connect(
            host='localhost',  # Example: 'localhost' or 'sql12.freemysqlhosting.net'
            database='chat_history',
            user='root',
            password='2450242',
            port=3306
        )
        print('3')
        if connection.is_connected():
            print('Connected to MySQL server')
        return connection
    
    except mysql.connector.Error as e:
        print(f"Error while connecting to MySQL: {e}")
        return None

# Example usage:
connection = get_db_connection()
print('5')
if connection:
    try:
        # Perform database operations here
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM your_table_name")
        rows = cursor.fetchall()
        for row in rows:
            print(row)
    finally:
        connection.close()
        print('MySQL connection is closed')