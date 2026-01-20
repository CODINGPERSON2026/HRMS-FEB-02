from imports import *

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'qaz123QAZ!@#',
    'database': 'hrms',
    'port': 3306,
    'autocommit': True
}


def get_db_connection():
    try:
        # Try with auth_plugin
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='qaz123QAZ!@#',
            database='hrms',
            port=3306,
            auth_plugin='mysql_native_password'
        )
        print("✅ Database connected successfully (with auth_plugin)")
        return conn
    except mysql.connector.Error as e:
        print(f"❌ Connection with auth_plugin failed: {e}")
        
        try:
            # Try without auth_plugin
            conn = mysql.connector.connect(
                host='localhost',
                user='root',
                password='qaz123QAZ!@#',
                database='hrms',
                port=3306
            )
            print("✅ Database connected successfully (without auth_plugin)")
            return conn
        except mysql.connector.Error as e2:
            print(f"❌ Connection without auth_plugin also failed: {e2}")
            return None
