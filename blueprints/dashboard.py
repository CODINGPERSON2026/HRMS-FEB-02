from imports import *
from blueprints.personal_information import get_db_connection
dashboard_bp =  Blueprint('dasboard',__name__,url_prefix='/stats')

@dashboard_bp.route('/get_detachment_details')
def get_det_personnel():
    print("yawar")
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        query = """
            SELECT 
                p.name,
                p.army_number,
                p.rank,
                ad.det_id,
                d.det_name
            FROM personnel p
            LEFT JOIN assigned_det ad ON p.army_number = ad.army_number
            LEFT JOIN dets d ON ad.det_id = d.det_id
            WHERE p.detachment_status = 1
        """
        cursor.execute(query)
        result = cursor.fetchall()
        print(result)
        return jsonify({"status": "success", "data": result})

    except Exception as e:
        print("Error:", e)
        return jsonify({"status": "error", "message": "Database error"})

    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

