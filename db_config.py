from imports import *

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
<<<<<<< HEAD
    'password': 'password123',
    'database': 'army_personnel_db',
=======
    'password': 'qaz123QAZ!@#',
    'database': 'hrms',
>>>>>>> c53e434c1d0b4c8279258d3d70d357532c835504
    'autocommit': True
}

def get_db_connection():
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None