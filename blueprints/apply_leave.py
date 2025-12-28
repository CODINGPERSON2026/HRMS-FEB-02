from imports import *
from db_config import get_db_connection


leave_bp = Blueprint('apply_leave', __name__, url_prefix='/apply_leave')
@leave_bp.route("/", methods=["GET"])
def apply_leave():
       return render_template("apply_leave/apply_leave.html")

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
    print("in this route")
    query = request.args.get("query", "").strip()
    print('search ',query)
    if query == "":
        return jsonify([])

    try:

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        existing_leave_query = '''select army_number,request_status,leave_type from leave_status_info where army_number = %s'''
        cursor.execute(existing_leave_query,(query,))
        existing = cursor.fetchone()
        print(existing)
        if not existing:

        # Search by army number (exact or partial)
            cursor.execute("""
                SELECT name, army_number,`rank`,trade,company
                FROM personnel
                WHERE army_number LIKE %s
                LIMIT 1
            """, (f"%{query}%",))
            results = cursor.fetchall()
            cursor.close()
            conn.close()
            return jsonify(results)
        return jsonify({'exists':'True','existing_leave':existing})
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    


@leave_bp.route("/submit_leave", methods=["POST"])
def submit_leave_request():
    data = request.get_json()
    print("Received data:", data)

    army_number = data.get("person_id")
    leave_type = data.get("leave_type")
    total_days = data.get("total_days")  # total_days includes prefix/suffix
    from_date = data.get("from_date")
    to_date = data.get("to_date")
    reason = data.get("reason")

    # Validate required fields
    if not all([army_number, leave_type, total_days, from_date, to_date, reason]):
        return jsonify({"message": "Missing required fields"}), 400

    # Get company of personnel
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT company FROM personnel WHERE army_number = %s", (army_number,))
        result = cursor.fetchone()
        if not result:
            return jsonify({"message": "Invalid Army Number. Personnel not found"}), 404
        company_name = result['company']
        print(company_name,'this is company')
        # Find SEC NCO of the same company
        cursor.execute('SELECT role FROM users WHERE company = %s AND role = %s', (company_name,'SEC NCO'))
        sec_nco = cursor.fetchone()
        print('#########################################################################################')
        print(sec_nco,'this is sec nco')
        request_sent_to = 'SEC NCO'

    except Exception as e:
        return jsonify({"message": "Database error", "error": str(e),'status':'error'}), 500
    finally:
        cursor.close()
        conn.close()

    # Insert leave request
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO leave_status_info
            (army_number, leave_type, leave_days, from_date, to_date, request_sent_to, request_status, recommend_date, rejected_date, remarks, leave_reason, created_at, updated_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, NULL, NULL, %s, %s, NOW(), NOW())
        """, (
            army_number,
            leave_type,
            int(total_days),
            from_date,
            to_date,
            request_sent_to,
            "Pending at SEC NCO",
            f"{leave_type} for {total_days} day(s)",
            reason
        ))
        conn.commit()
        return jsonify({'status':'success',"message": f"Leave request for {total_days} day(s) sent to OC successfully!"})
    except Exception as e:
        conn.rollback()
        return jsonify({"message": "Failed to apply leave", "error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()


# FOR SENDING THE LEAVE REQUEST TO HIGHER LEVEL
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
    print('in this route')
    conn = get_db_connection()

    cursor = conn.cursor(dictionary=True)
    user = require_login()
    email = user["role"]
    current_user_role = user['role']

    

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

        # Fetch only necessary leave request data including from_date and to_date
        cursor.execute("""
            SELECT 
                id,
                army_number,
                leave_type,
                leave_days,
                from_date,
                to_date,
                leave_reason,
                request_status
            FROM leave_status_info
            WHERE id = %s
        """, (leave_id,))
        leave = cursor.fetchone()
        cursor.execute("select name from personnel where army_number = %s",(leave['army_number'],))
        name_result = cursor.fetchone()        
        leave['name'] = name_result['name']
        print(leave['name'])
        if not leave:
            return jsonify({
                "success": False,
                "message": "Leave request not found"
            }), 404

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





@leave_bp.route("/recommend_leave", methods=["POST"])
def recommend_leave():
    data = request.get_json()
    leave_id = data.get("leave_id")

    if not leave_id:
        return jsonify({"message": "Leave ID missing"}), 400
    user =  require_login()
    current_user_role = user['role']
    print('current_user_role',current_user_role)
    if current_user_role == 'SEC NCO':
        sent_request_to = 'SEC JCO'
        
        request_status  = 'Pending at SEC JCO'
    if current_user_role == 'SEC JCO':
        sent_request_to = 'OC'
        request_status = 'Pending at OC'
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        # 1️⃣ Fetch leave request details
        cursor.execute("""
            SELECT 
                id,
                army_number,
                leave_type,
                leave_days,
                from_date,
                to_date,
                leave_reason
            FROM leave_status_info
            WHERE id = %s
        """, (leave_id,))
        leave = cursor.fetchone()

        if not leave:
            return jsonify({"message": "Leave request not found"}), 404
        print(leave,"this is leave")
        # Logged-in user (SEC NCO)
        
 
        # 2️⃣ Insert into leave_history
        cursor.execute("""
            INSERT INTO hrms.leave_history (
                leave_request_id,
                army_number,
                name,
                leave_type,
                from_date,
                to_date,
                total_days,
                recommended_by,
                remarks
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            leave["id"],
            leave["army_number"],
            "N/A",  # replace with actual name if available
            leave["leave_type"],
            leave["from_date"],
            leave["to_date"],
            leave["leave_days"],
            current_user_role,
            leave["leave_reason"]
        ))

        # 3️⃣ Update main leave table
        cursor.execute("""
            UPDATE leave_status_info
            SET
                request_sent_to = %s,
                request_status = %s,
                recommend_date = NOW(),
                rejected_date = NULL,
                updated_at = NOW()
            WHERE id = %s
        """, (sent_request_to,request_status,leave_id))

        conn.commit()

        return jsonify({"message": "Leave recommended successfully"}), 200

    except Exception as e:
        conn.rollback()
        print("ERROR:", e)
        return jsonify({"message": "Server error"}), 500

    finally:
        cursor.close()
        conn.close()
@leave_bp.route("/get_recommended_requests")
def get_recommended_requests():
    print("in this recommended route")

    user = require_login()
    recommended_by = user['role']

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            lh.id,                      -- used by View button
            lh.leave_request_id,
            lh.army_number,
            lh.leave_type,
            lsi.leave_days,
            lsi.from_date,
            lsi.to_date,
            lh.status,
            lh.recommended_at
        FROM leave_history lh
        JOIN leave_status_info lsi
            ON lh.leave_request_id = lsi.id
        WHERE lh.recommended_by = %s
        ORDER BY lh.recommended_at DESC
    """, (recommended_by,))

    data = cursor.fetchall()
    cursor.close()
    conn.close()

    return jsonify({"data": data})


@leave_bp.route("/get_leave_history/<int:id>")
def get_leave_history(id):
    user = require_login()
    recommended_by = user['role']

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            lh.id,
            lh.leave_request_id,
            lh.army_number,
            lh.name,
            lh.leave_type,
            lsi.leave_days,
            lsi.from_date,
            lsi.to_date,
            lsi.leave_reason,
            lh.status,
            lh.remarks,
            lh.recommended_at
        FROM leave_history lh
        JOIN leave_status_info lsi
            ON lh.leave_request_id = lsi.id
        WHERE lh.id = %s
          AND lh.recommended_by = %s
    """, (id, recommended_by))

    data = cursor.fetchone()
    cursor.close()
    conn.close()

    if not data:
        return jsonify({"message": "Record not found"}), 404

    return jsonify({"data": data})
