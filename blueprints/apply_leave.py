from imports import *
from db_config import get_db_connection


leave_bp = Blueprint('apply_leave', __name__, url_prefix='/apply_leave')
@leave_bp.route('/')
def apply_leave():
    return render_template('apply_leave/apply_leave.html')
@leave_bp.route("/get_leave_details", methods=["POST"])
def get_leave_details():
    data = request.get_json()
    army_no = data.get("person_id")

    if not army_no:
        return jsonify({"success": False, "message": "Army number missing"}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT name, army_number, trade, `rank`, company
            FROM personnel
            WHERE army_number = %s
        """, (army_no,))
        personnel = cursor.fetchone()

        if not personnel:
            return jsonify({"success": False, "message": "No such soldier found"}), 404

        cursor.execute("""
            SELECT sr_no, year, al_days, cl_days, aal_days, total_days, remarks
            FROM leave_details
            WHERE army_number = %s
            ORDER BY year DESC
            LIMIT 1
        """, (army_no,))
        leaveinfo = cursor.fetchone()
        print(leaveinfo)

        cursor.close()
        conn.close()

        if not leaveinfo:
            return jsonify({
                "success": True,
                "personnel": personnel,
                "leave_balance": []
            })

        # Return leave rows as an ARRAY
        leave_balance = [
            {
                "leave_type": "AL",
                "total_leave": leaveinfo["al_days"],
                "leave_taken": 0,
                "balance_leave": leaveinfo["al_days"]
            },
            {
                "leave_type": "CL",
                "total_leave": leaveinfo["cl_days"],
                "leave_taken": 0,
                "balance_leave": leaveinfo["cl_days"]
            },
            {
                "leave_type": "AAL",
                "total_leave": leaveinfo["aal_days"],
                "leave_taken": 0,
                "balance_leave": leaveinfo["aal_days"]
            }
        ]

        return jsonify({
            "success": True,
            "personnel": personnel,
            "leave_balance": leave_balance
        })

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@leave_bp.route("/search_personnel")
def search_personnel():
    query = request.args.get("query", "").strip()

    if query == "":
        return jsonify([])

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # Search by army number (exact or partial)
        cursor.execute("""
            SELECT name, army_number,`rank`,trade 
            FROM personnel
            WHERE army_number LIKE %s
            LIMIT 1
        """, (f"%{query}%",))

        results = cursor.fetchall()

        cursor.close()
        conn.close()
        
        return jsonify(results)

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    


# FOR SENDING THE LEAVE REQUEST TO HIGHER LEVEL
@leave_bp.route("/submit_leave", methods=["POST"])
def submit_leave_request():
    data = request.get_json()
    print(data)
    army_number = data.get("person_id")
    leave_type = data.get("leave_type")
    days = data.get("days")

    if not all([army_number, leave_type, days]):
        return jsonify({"message": "Missing required fields"}), 400
    

    # check the company of the leave applicat first
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        query= 'SELECT company from personnel where army_number = %s'
        cursor.execute(query,(army_number,))
        result = cursor.fetchone()
        company_name =  result['company']
        if company_name:
            query = 'SELECT email from users  where company = %s AND role = "CLERK"'
            cursor.execute(query,(company_name,))
            result = cursor.fetchone()
            request_sent_to =  result['email']
    except Exception as e:
        print('Database error',str(e))
    finally:
        conn.close()
    
    
    # Set request to be sent to OC
    
    request_status = "Pending"

    conn = get_db_connection()
    cursor = conn.cursor()
    print('before inserting')
    try:
        cursor.execute("""
            INSERT INTO leave_status_info
            (army_number, leave_type, leave_days, request_sent_to, request_status, approval_date, rejected_date, remarks, created_at, updated_at)
            VALUES (%s, %s, %s, %s, %s, NULL, NULL, %s, NOW(), NOW())
        """, (
            army_number, 
            leave_type, 
            int(days), 
            request_sent_to, 
            request_status, 
            f"{leave_type} for {days} day(s)"
        ))

        conn.commit()
        return jsonify({"message": f"Leave request for {days} day(s) sent to OC successfully!"})
    except Exception as e:
        conn.rollback()
        return jsonify({"message": "Failed to apply leave", "error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()
@leave_bp.route("/update_leave_status", methods=["POST"])
def update_leave_status():
    data = request.get_json()
    leave_id = data.get("id")
    status = data.get("status")

    if status not in ['Approved', 'Rejected']:
        return jsonify({"status": "error", "message": "Invalid status"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        if status == 'Approved':
            cursor.execute("""
                UPDATE leave_status_info
                SET request_status = %s, approval_date = NOW()
                WHERE id = %s
            """, (status, leave_id))
        else:
            cursor.execute("""
                UPDATE leave_status_info
                SET request_status = %s, rejected_date = NOW()
                WHERE id = %s
            """, (status, leave_id))

        conn.commit()
        return jsonify({"status": "success"})
    except Exception as e:
        conn.rollback()
        return jsonify({"status": "error", "message": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@leave_bp.route("/get_leave_requests", methods=["GET"])
def get_leave_requests():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    user = require_login()
    email = user['email']

    try:
        cursor.execute("""
            SELECT id, army_number, leave_type, leave_days,
                   request_status, remarks, created_at
            FROM leave_status_info
            WHERE request_sent_to = %s
            ORDER BY created_at DESC
        """, (email,))

        rows = cursor.fetchall()
        return jsonify({"status": "success", "data": rows})

    except Exception as e:
        print("Error fetching leave requests:", e)
        return jsonify({"status": "error", "message": str(e)}), 500
    finally:
        cursor.close()
        conn.close()


@leave_bp.route("/get_leave_request/<int:leave_id>", methods=["GET"])
def get_leave_request(leave_id):
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        query = """
            SELECT 
                id,
                army_number,
                leave_type,
                leave_days,
                created_at,
                leave_reason,
                request_status
            FROM leave_status_info
            WHERE id = %s
        """
        cursor.execute(query, (leave_id,))
        leave = cursor.fetchone()
        print(leave_id)

        if not leave:
            return jsonify({
                "success": False,
                "message": "Leave request not found"
            }), 404
        query = ''' select name from personnel where army_number = %s'''
        cursor.execute(query,(leave['army_number'],))
        result_name =  cursor.fetchone()
        leave['name'] = result_name['name']
        
        query = '''SELECT
  CASE %s
    WHEN   'AL'  THEN al_days
    WHEN  'CL'  THEN cl_days
    WHEN  'AAL' THEN aal_days
  END AS leave_days
FROM leave_details
WHERE army_number = %s;
'''      
        print('fine till herer')
        cursor.execute(query,(leave['leave_type'],leave['army_number']))
        leave_days_left = cursor.fetchone()
        leave['days_left'] = leave_days_left['leave_days']
         
        return jsonify({
            "success": True,
            "data": leave
        })

    except Exception as e:
        print(str(e))
        return jsonify({
            "success": False,
            "message": "Server error",
            "error": str(e)
        }), 500

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
