from imports import *
from blueprints.personal_information import get_db_connection
dashboard_bp =  Blueprint('dasboard',__name__,url_prefix='/stats')

@dashboard_bp.route('/get_detachment_details')
def get_det_personnel():
    print("yawar")
    company = request.args.get('company')  # <-- get company filter

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        query = """
    SELECT 
        p.name,
        p.army_number,
        p.rank,
        p.company,
        ad.det_id,
        ad.det_status,
        d.det_name
    FROM personnel p
    LEFT JOIN assigned_det ad ON p.army_number = ad.army_number
    LEFT JOIN dets d ON ad.det_id = d.det_id
    WHERE p.detachment_status = 1
      AND ad.det_status = 1
"""

        params = []

        if company:  # <-- inject filter
            query += " AND p.company = %s"
            params.append(company)

        cursor.execute(query, params)
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





# ***********************************************************DELETE DETACHMENT**********************

@dashboard_bp.route('/delete_personnel', methods=['POST'])
def delete_personnel():
    data = request.get_json()
    army_number = data.get('army_number')
    status= 0

    if not army_number:
        return jsonify({"status": "error", "message": "Missing army_number"}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Start transaction
        conn.start_transaction()

        # Update personnel table
        cursor.execute("""
            UPDATE personnel
            SET detachment_status = 0
            WHERE army_number = %s
        """, (army_number,))

        # Update assigned_det table with det_removed_date
        cursor.execute("""
            UPDATE assigned_det
            SET det_removed_date = %s,
                        det_status = %s
            WHERE army_number = %s
        """, (datetime.now(),0,army_number))

        # Commit transaction
        conn.commit()

        cursor.close()
        conn.close()

        return jsonify({"status": "success", "message": f"{army_number} removed from detachment"})

    except Exception as e:
        print(e)
        conn.rollback()  # rollback on error
        return jsonify({"status": "error", "message": "Database error"}), 500