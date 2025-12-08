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
>>>>>>> 0e0652dafe12e63618e695484522fad4c2bcfb5c
    'autocommit': True
}

def get_db_connection():
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None