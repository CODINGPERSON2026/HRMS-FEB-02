from imports import *

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
<<<<<<< HEAD
    'password': 'yawar@123',
=======
    'password': 'qaz123QAZ!@#',
>>>>>>> e8e994c03789b9dcaf247f862cf5d55063c08bf5
    'database': 'hrms',
    'port': 3306,
    'autocommit': True
}


def get_db_connection():
    
    try:
        return mysql.connector.connect(**DB_CONFIG)
    except Error as e:
        print("Error connecting to MySQL:", e)
        return None
