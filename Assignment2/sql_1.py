import mysql.connector
from mysql.connector import Error

print("Starting script...")  # Debugging statement

try:
    print("Attempting to connect to MySQL...")  # Debugging statement
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='password',  # Replace with your actual password
        port=3306
    )
    if connection.is_connected():
        print("Connected to MySQL successfully!")

        # Create a cursor object
        cursor = connection.cursor()

        # Create a database
        print("Creating database 'mydatabase'...")  # Debugging statement
        cursor.execute("CREATE DATABASE IF NOT EXISTS mydatabase")
        print("Database 'mydatabase' created successfully!")

        # Switch to the new database
        print("Switching to database 'mydatabase'...")  # Debugging statement
        cursor.execute("USE mydatabase")

        # Create a table
        print("Creating table 'users'...")  # Debugging statement
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL
            )
        """)
        print("Table 'users' created successfully!")

except Error as err:
    print("MySQL Error occurred!")
    print(f"Error Code: {err.errno}")
    print(f"SQLSTATE: {err.sqlstate}")
    print(f"Message: {err.msg}")
except Exception as e:
    print("An unexpected error occurred!")
    print(f"Error: {e}")
finally:
    if 'connection' in locals() and connection.is_connected():
        cursor.close()
        connection.close()
        print("MySQL connection closed.")