from imports import *
from blueprints.personal_information import get_db_connection
dashboard_bp =  Blueprint('dasboard',__name__,url_prefix='/stats')


@dashboard_bp.route('/get_detachment_details')
def get_det_personnel():
    print("yawar")
    try:
        conn =get_db_connection()
        cursor = conn.cursor(dictionary=True)

        query = """
            SELECT name, army_number, `rank` 
            FROM personnel 
            WHERE detachment_status = 1
        """
        cursor.execute(query)
        result = cursor.fetchall()

        return jsonify({"status": "success", "data": result})

    except Exception as e:
        print("Error:", e)
        return jsonify({"status": "error", "message": "Database error"})

    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()
