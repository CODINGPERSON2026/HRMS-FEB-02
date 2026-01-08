from imports import *
import os
from datetime import date, datetime, timedelta
from flask import Flask
from flask_cors import CORS
import csv
from io import StringIO, BytesIO
from flask import send_file

app = Flask(__name__)
CORS(app, supports_credentials=True)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 31536000
app.secret_key = os.urandom(24)

app.register_blueprint(personnel_info)
app.register_blueprint(weight_ms)
app.register_blueprint(leave_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(task_bp)
app.register_blueprint(accounts_bp)

@app.route("/admin_login", methods=["POST",'GET'])
def admin_login():
    if request.method == 'GET':
        return render_template('/loginpage/loginpage.html')
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM users WHERE email=%s AND password=%s", (email, password))
    user = cursor.fetchone()

    if not user:
        return jsonify({"success": False, "error": "Invalid email or password"}), 401
    username  =  user['username']
    
    cursor.close()
    conn.close()


    # create JWT
    payload = {
        "user_id": user["id"],
        "email": user["email"],
        'username':user['username'],
        "role": user["role"],
        'company':user['company']
    }

    token = jwt.encode(payload, JWT_SECRET, algorithm="HS256")

    # set JWT in cookie
    resp = jsonify({"success": True,"username":username})
    resp.set_cookie("token", token, httponly=True, samesite="Lax")

    return resp

@app.route("/logout")
def logout():
    resp = redirect(url_for("admin_login"))
    resp.set_cookie("token", "", expires=0)
    return resp


@app.route('/')
def dashboard():
    user = require_login()

    if not user:
        return redirect(url_for('admin_login'))
    username = user['username'].capitalize()
    user_company = user['company']
    return render_template('dashboard.html', username = username,role = user['role'],user_company=user_company)




@app.route('/api/dashboard_heading')
def dashboard_heading():
    # Determine heading dynamically
    # You can base this on user role, current tab, or any condition
    user = require_login()
    if user['role'] == 'CO':
        company = 'CO 15CESR'
    elif user['role'] == '2IC':
        company = '2IC 15CESR'
    else:
        company = user['company']  # Example
    print(company)
    
    
    return jsonify({"heading": company})










@app.route('/mt', methods=['GET', 'POST'])
def mt():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
        vehicle_no = request.form['vehicle_no']
        vtype = request.form['type']
        vclass = request.form['class']
        detailment = request.form['detailment']
        dist_travelled = request.form['dist_travelled']
        quantity = request.form['quantity']
        bullet_proof = request.form.get('bullet_proof', 'N')

        insert_query = """
            INSERT INTO Vehicle_detail 
            (vehicle_no, type, class, detailment, dist_travelled, quantity, bullet_proof)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(insert_query, (vehicle_no, vtype, vclass, detailment, dist_travelled, quantity, bullet_proof))
        conn.commit()

        cursor.close()
        conn.close()
        return redirect(url_for('mt'))

    cursor.execute("SELECT * FROM Vehicle_detail")
    vehicles = cursor.fetchall()
    cursor.close()
    conn.close()

    drivers = [
        {"name": "Rajesh Kumar", "license": "MH14A12345", "hill_test": True, "vehicle": "Jeep"},
        {"name": "Amit Verma", "license": "MH12B67890", "hill_test": False, "vehicle": "Truck"},
        {"name": "Suresh Patel", "license": "MH13C99887", "hill_test": True, "vehicle": "Scorpio"},
    ]

    maintenance = [
        {"vehicle": "Truck MH14CD5678", "issue": "Brake fluid leakage", "date_reported": "2025-10-25", "status": "In Progress"},
        {"vehicle": "Motorcycle MH13GH2345", "issue": "Engine oil change", "date_reported": "2025-10-27", "status": "Pending"},
    ]

    return render_template('mt/mtView.html', vehicles=vehicles, drivers=drivers, maintenance=maintenance)
    
@app.route('/personal_info')
def personal_info():
    return render_template('personalInfoView.html')

@app.route('/personal/create', methods=['GET', 'POST'])
def create_personal():
    if request.method == 'POST':
        data = request.form.to_dict()
    return render_template('personalInfoView.html', form_view='create')

@app.route('/personal/update')
def update_personal():
    return render_template('personalInfoView.html', form_view='update')

@app.route('/personal/view')
def view_personal():
    return render_template('personalInfoView.html', form_view='view')

@app.route('/search_personnel', methods=['POST'])
@app.route('/search_personnel', methods=['POST'])
def search_person():
    print("in this route")

    query = request.form.get('army_number')  # ✅ CORRECT
    

    if not query:
        return jsonify([])

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT 
            name, 
            army_number, 
            `rank`, 
            trade, 
            company,
            detachment_status AS det_status,
            posting_status,
            onleave_status AS leave_status
        FROM personnel
        WHERE army_number = %s
    """, (query,))

    results = cursor.fetchall()
    cursor.close()
    conn.close()

    return jsonify(results)



@app.route('/get_locations')
def get_locations():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT det_id, det_name FROM dets")
    locations = cursor.fetchall()
    conn.close()
    return jsonify(locations)

@app.route('/get_dets')
def get_dets():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT COUNT(*) AS count from personnel where detachment_status = 1")
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return jsonify({'count': result['count']})

@app.route('/get_interview_pending_count')
def interview():
    conn = get_db_connection()
    cursor  =  conn.cursor(dictionary=True)
    query = """
    SELECT 
        SUM(interview_status = 0) AS pending_count,
        COUNT(*) AS total_count
    FROM personnel
"""

    cursor.execute(query)
    result = cursor.fetchone()
    pending_count = result["pending_count"]
    total_count = result["total_count"]
    percentage = 0
    if total_count > 0:
        percentage = pending_count/total_count * 100
    cursor.close()
    conn.close()
    return jsonify({'result':result,'percentage':round(percentage, 2)})


@app.route('/get_pending_interview_list')
def get_pending_interview_list():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    user = require_login()  # Get logged-in user
    company = user['company']
    search = request.args.get("search", "").strip()

    try:
        query = """
            SELECT name, army_number, home_state, company
            FROM personnel
            WHERE interview_status = 0
        """
        params = []

        # Apply company filter if user is not Admin
        if company != "Admin":
            query += " AND company = %s"
            params.append(company)

        # Apply search filter
        if search:
            query += " AND army_number LIKE %s"
            params.append(f"%{search}%")

        cursor.execute(query, params)
        data = cursor.fetchall()
        return jsonify({"status": "success", "data": data})

    except Exception as e:
        print("Error fetching pending interview list:", str(e))
        return jsonify({"status": "error", "message": "Server error"}), 500

    finally:
        cursor.close()
        conn.close()


@app.route('/assign_personnel', methods=['POST'])
def assign_personnel():
    data = request.get_json()

    personnel_ids = data.get('army_number', [])
    action_type = data.get('status', '').lower()
    remarks = data.get('remarks', '')

    if not personnel_ids or not action_type:
        return jsonify({"error": "Missing data"}), 400

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        for pid in personnel_ids:
            cursor.execute("""
    SELECT detachment_status, posting_status, td_status
    FROM personnel
    WHERE army_number=%s
""", (pid,))
        status = cursor.fetchone()
        if not status:
            return jsonify({"error": f"{pid} not found"}), 404

        det_flag = int(status['detachment_status']) if status['detachment_status'] else 0
        post_flag = int(status['posting_status']) if status['posting_status'] else 0
        td_flag = int(status['td_status']) if status['td_status'] else 0

        if action_type == "det" and det_flag == 1:
            return jsonify({"error": f"{pid} is already in Detachment"}), 400

        if action_type == "posting" and post_flag == 1:
            return jsonify({"error": f"{pid} is already Posted"}), 400

        if action_type == "td" and td_flag == 1:
            return jsonify({"error": f"{pid} is already on TD"}), 400

        for pid in personnel_ids:

            if action_type == "det":
                cursor.execute("""
                    INSERT INTO assigned_det (army_number, det_id)
                    VALUES (%s, %s)
                """, (pid, remarks))

                cursor.execute("UPDATE personnel SET detachment_status=1 WHERE army_number=%s", (pid,))

            elif action_type == "posting":
                cursor.execute("""
                    INSERT INTO posting_details_table (army_number, action_type, posting_date)
                    VALUES (%s, %s, NOW())
                """, (pid, remarks))

                cursor.execute("UPDATE personnel SET posting_status=1 WHERE army_number=%s", (pid,))

            elif action_type == "td":
                cursor.execute("""
                    INSERT INTO td_table (army_number, remarks)
                    VALUES (%s, %s)
                """, (pid, remarks))

                cursor.execute("UPDATE personnel SET td_status=1 WHERE army_number=%s", (pid,))

        conn.commit()
        return jsonify({"message": f"{action_type.upper()} Assigned Successfully"}), 200

    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500

    finally:
        cursor.close()
        conn.close()


@app.route("/get_personnel_details/<army_number>")
def get_personnel_details(army_number):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    try:
        cursor.execute("""
            SELECT company 
            FROM personnel 
            WHERE army_number = %s
        """, (army_number,))
        
        result = cursor.fetchone()
        
        if result:
            return jsonify(result)
        else:
            return jsonify({"company": "N/A"}), 404
            
    except Exception as e:
        print("Error:", e)
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()


@app.route("/get_sales_data")
def get_sales_data():
    try:
        data_type = request.args.get("type")

        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT date, liquor_sale, grocery_sale FROM sales")
        rows = cursor.fetchall()
        db.close()

        df = pd.DataFrame(rows)
        df['date'] = pd.to_datetime(df['date'])

        if data_type == "daily":
            df_group = df.groupby(df['date'].dt.date)[['liquor_sale', 'grocery_sale']].sum()

        elif data_type == "monthly":
            df_group = df.groupby(df['date'].dt.to_period('M'))[['liquor_sale', 'grocery_sale']].sum()
            df_group.index = df_group.index.astype(str)

        elif data_type == "yearly":
            df_group = df.groupby(df['date'].dt.year)[['liquor_sale', 'grocery_sale']].sum()

        labels = list(df_group.index.astype(str))
        liquor = df_group['liquor_sale'].tolist()
        grocery = df_group['grocery_sale'].tolist()

        return jsonify({
            "labels": labels,
            "liquor": liquor,
            "grocery": grocery
        })

    except Exception as e:
        print("ERROR:", e)
        return jsonify({"error": str(e)}), 500
    

@app.route('/apply_leave')
def apply_leave():
    return render_template('apply_leave.html')

@app.route('/daily_running')
def daily_running():
    return render_template('mt/daily_running.html')


@app.route('/get_vehicle_details', methods=['POST'])
def get_vehicle_details():
    vehicle_no = request.form.get('vehicle_no')
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT type, class FROM vehicle_detail WHERE vehicle_no=%s", (vehicle_no,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()

    if result:
        return jsonify(result)
    else:
        return jsonify({"error": "Vehicle not found"}), 500


@app.route('/submit_running', methods=['POST'])
def submit_running():
    vehicle_no = request.form['vehicle_no']
    v_type = request.form['type']
    v_class = request.form['class']
    from_place = request.form['from_place']
    to_place = request.form['to_place']
    remarks = request.form['remarks']
    conn = get_db_connection()
    cursor = conn.cursor()
    query = """
        INSERT INTO daily_running (vehicle_no, type, class, from_place, to_place, remarks, date)
        VALUES (%s, %s, %s, %s, %s, %s, NOW())
    """
    cursor.execute(query, (vehicle_no, v_type, v_class, from_place, to_place, remarks))
    conn.commit()

    cursor.close()
    conn.close()

    return jsonify({"message": "Saved successfully"})


@app.route('/board_details')
def board_details():
    return render_template('boo/board_details.html')


@app.route("/get_boards")
def get_boards():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM boards ORDER BY id DESC")
    boards = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(boards)


@app.route("/add_board", methods=["POST"])
def add_board():
    data = request.form

    conn = get_db_connection()
    cur = conn.cursor()
    query = """
        INSERT INTO boards 
        (order_no, entry_date, authority, subject, presiding_officer, completion_date, remarks)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """

    cur.execute(query, (
        data.get("order_no"),
        data.get("entry_date"),
        data.get("authority"),
        data.get("subject"),
        data.get("presiding_officer"),
        data.get("completion_date"),
        data.get("remarks"),
    ))

    conn.commit()
    cur.close()

    return jsonify({"status": "success"})


@app.route("/delete_board/<int:board_id>", methods=["DELETE"])
def delete_board(board_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM boards WHERE id=%s", (board_id,))
    conn.commit()
    cur.close()
    return jsonify({"status": "success"})


@app.route("/edit_board/<int:board_id>", methods=["POST"])
def edit_board(board_id):
    data = request.form

    conn = get_db_connection()
    cur = conn.cursor()
    query = """
        UPDATE boards
        SET order_no=%s, entry_date=%s, authority=%s, subject=%s,
            presiding_officer=%s, completion_date=%s, remarks=%s
        WHERE id=%s
    """

    cur.execute(query, (
        data.get("order_no"),
        data.get("entry_date"),
        data.get("authority"),
        data.get("subject"),
        data.get("presiding_officer"),
        data.get("completion_date"),
        data.get("remarks"),
        board_id
    ))

    conn.commit()
    cur.close()

    return jsonify({"status": "success"})


@app.route("/get_board_members/<int:order_no>")
def get_board_members(order_no):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM board_members WHERE order_no=%s", (order_no,))
    members = cur.fetchall()
    cur.close()
    return jsonify(members)


@app.route("/add_member", methods=["POST"])
def add_member():
    data = request.form
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO board_members (order_no, member_name, army_number)
        VALUES (%s, %s, %s)
    """, (data.get("order_no"), data.get("member_name"), data.get("army_number")))
    conn.commit()
    cur.close()

    return jsonify({"status": "success"})
















@app.route("/delete_member/<int:member_id>", methods=["DELETE"])
def delete_member(member_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM board_members WHERE id=%s", (member_id,))
    conn.commit()
    cur.close()
    return jsonify({"status": "success"})


@app.route("/edit_member/<int:member_id>", methods=["POST"])
def edit_member(member_id):
    data = request.form

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE board_members
        SET member_name=%s, army_number=%s
        WHERE id=%s
    """, (data.get("member_name"), data.get("army_number"), member_id))

    conn.commit()
    cur.close()

    return jsonify({"status": "success"})


# ===============================================
# SENSITIVE PERSONNEL MANAGEMENT - FIXED
# ===============================================
@app.route("/search_personnel_to_mark", methods=["POST"])
def search_personnel():
    query = request.form.get("query", "").strip()
    
    print("THIS IS INCOMING:", query)  # Should now print
    import sys
    sys.stdout.flush()

    if len(query) < 2:
        return jsonify([])

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        like_pattern = f"%{query}%"

        
        cursor.execute("""
            SELECT army_number, name,`rank`, company
            FROM personnel
            WHERE LOWER(name) LIKE LOWER(%s)
               OR army_number LIKE %s
            ORDER BY name
            LIMIT 50
        """, (like_pattern, like_pattern))

        rows = cursor.fetchall()
        results = []
        for row in rows:
            results.append({
                "army_number": row[0],
                "name": row[1],
                "rank": row[2],
                "company": row[3] or "N/A"
            })

        print(f"Found {len(results)} results for '{query}'")
        return jsonify(results)

    except Exception as e:
        print("Search error:", e)
        import traceback
        traceback.print_exc()  # This will show full error in console
        return jsonify({"error": "Database error"}), 500

    finally:
        cursor.close()
        conn.close()

@app.route("/mark_personnel", methods=["GET"])
def mark_personnel():
    conn = get_db_connection()
    cursor = conn.cursor()   
    cursor.execute("""
        SELECT s.id, s.army_number, s.reason, s.marked_on, 
               p.name, p.rank, p.company
        FROM sensitive_marking s
        JOIN personnel p ON s.army_number = p.army_number
        ORDER BY s.marked_on DESC
    """)
    rows = cursor.fetchall()

    sensitive_list = []
    for r in rows:
        sensitive_list.append({
            "id": r[0],
            "army_number": r[1],
            "reason": r[2],
            "marked_on": r[3].strftime("%Y-%m-%d %H:%M:%S") if r[3] else "",
            "name": r[4],
            "rank": r[5],
            "company": r[6] or "N/A"
        })
    
    cursor.close()
    conn.close()
    
    response = make_response(render_template("sensitive_indl/mark_personnel.html", sensitive_list=sensitive_list))
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response


# AJAX: Mark as Sensitive
@app.route("/mark_sensitive", methods=["POST"])
def mark_sensitive():
    army_number = request.form.get("army_number")
    reason = request.form.get("reason")
    
    if not army_number or not reason:
        return jsonify({"success": False, "error": "Missing army number or reason"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Check if already marked
        cursor.execute("SELECT 1 FROM sensitive_marking WHERE army_number = %s", (army_number,))
        if cursor.fetchone():
            return jsonify({"success": False, "error": "This personnel is already marked as sensitive."}), 400

        cursor.execute("""
            INSERT INTO sensitive_marking (army_number, reason, marked_on)
            VALUES (%s, %s, %s)
        """, (army_number, reason.strip(), datetime.now()))
        conn.commit()

        return jsonify({"success": True, "message": "Personnel marked as sensitive successfully."})

    except Exception as e:
        conn.rollback()
        print("ERROR in mark_sensitive:", e)
        return jsonify({"success": False, "error": "Database error"}), 500
    finally:
        cursor.close()
        conn.close()


# AJAX: Update Reason
@app.route("/update_sensitive_reason", methods=["POST"])
def update_sensitive_reason():
    army_number = request.form.get("army_number")
    reason = request.form.get("reason")
    
    if not army_number or not reason:
        return jsonify({"success": False, "error": "Missing data"}), 400
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("UPDATE sensitive_marking SET reason = %s WHERE army_number = %s", (reason.strip(), army_number))
        if cursor.rowcount == 0:
            return jsonify({"success": False, "error": "Personnel not found in sensitive list"}), 404
        
        conn.commit()
        return jsonify({"success": True, "message": "Reason updated successfully."})
    except Exception as e:
        conn.rollback()
        print("Error:", e)
        return jsonify({"success": False, "error": "Update failed"}), 500
    finally:
        cursor.close()
        conn.close()


# AJAX: Remove from Sensitive List
@app.route("/remove_sensitive", methods=["POST"])
def remove_sensitive():
    army_number = request.form.get("army_number")
    
    if not army_number:
        return jsonify({"success": False, "error": "Missing army number"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("DELETE FROM sensitive_marking WHERE army_number = %s", (army_number,))
        if cursor.rowcount == 0:
            return jsonify({"success": False, "error": "Personnel not found in sensitive list"}), 404
        
        conn.commit()
        return jsonify({"success": True, "message": "Personnel removed from sensitive list."})

    except Exception as e:
        conn.rollback()
        print("ERROR in remove_sensitive:", e)
        return jsonify({"success": False, "error": "Remove failed"}), 500
    finally:
        cursor.close()
        conn.close()


# New: AJAX endpoint to refresh sensitive list
@app.route("/get_sensitive_list", methods=["GET"])
def get_sensitive_list():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            SELECT s.id, s.army_number, s.reason, s.marked_on, 
                   p.name, p.rank, p.company
            FROM sensitive_marking s
            JOIN personnel p ON s.army_number = p.army_number
            ORDER BY s.marked_on DESC
        """)
        rows = cursor.fetchall()
        print(rows)

        sensitive_list = []
        for r in rows:
            sensitive_list.append({
                "army_number": r[1],
                "reason": r[2],
                "marked_on": r[3].strftime("%Y-%m-%d %H:%M:%S") if r[3] else "",
                "name": r[4],
                "rank": r[5],
                "company": r[6] or "N/A"
            })
        print(sensitive_list,"this is sensitive list")
        return jsonify({"success": True, "data": sensitive_list})
    
    except Exception as e:
        print("Error fetching sensitive list:", e)
        return jsonify({"success": False, "error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# ===============================================
# PARADE STATE
# ===============================================

@app.route("/leave_status")
def leave_status():
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)

    cur.execute("""
        SELECT 
    company,
    SUM(CASE WHEN onleave_status = '1' THEN 1 ELSE 0 END) AS leave_count,
    COUNT(*) AS total_count,
    ROUND((SUM(CASE WHEN onleave_status = '1' THEN 1 ELSE 0 END) / COUNT(*)) * 100, 2) AS leave_percentage
    FROM personnel
    GROUP BY company
    ORDER BY company
    """)

    data = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(data)


@app.route("/company_status")
def company_status():
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)
    data = []

    rank_sql = """
    SELECT
        SUM(CASE WHEN `rank` IN ('agniveer', 'Signal Man','nk','lnk','hav') THEN 1 ELSE 0 END) AS other_rank_count,
        SUM(CASE WHEN `rank` IN ('nbsub','subedar','JCO','sub maj') THEN 1 ELSE 0 END) AS jco_count,
        SUM(CASE WHEN `rank` IN ('lt','capt','maj','ltcol','col','OC') THEN 1 ELSE 0 END) AS officer_count
    FROM personnel
    """

    try:
        cur.execute(rank_sql)
        overall = cur.fetchone() or {"other_rank_count": 0, "jco_count": 0, "officer_count": 0}
        overall["company"] = "15 XYZ"
        data.append(overall)

        companies = ["1 company", "2 company", "3 company", "4 company"]
        sql_with_where = rank_sql + " WHERE company = %s"

        for company in companies:
            cur.execute(sql_with_where, (company,))
            row = cur.fetchone() or {"other_rank_count": 0, "jco_count": 0, "officer_count": 0}
            row["company"] = company
            data.append(row)

        return jsonify(data)

    finally:
        cur.close()
        conn.close()


@app.route("/paradeState")
def paradeState():
    return render_template("daily_state/daily_parade_state.html")

@app.route("/add_event", methods=["POST"])
def add_event():
    event_date = request.form["event_date"]
    event_name = request.form["event_name"]
    venue = request.form["venue"]

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO daily_events (event_date, event_name, venue) VALUES (%s, %s, %s)",
        (event_date, event_name, venue)
    )
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"status": "success"})

@app.route("/daily_event")
def daily_event():
    today = date.today()

    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM daily_events WHERE event_date = %s", (today,))
    data = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(data)


# ===============================================
# ALARM FUNCTIONALITY
# ===============================================

@app.route('/api/assigned_alarm')
def assigned_alarm():
    conn = None
    cursor = None
    try:
        user = require_login()  # Get logged-in user
        user_company = user['company']
        print("Logged-in user's company:", user_company)

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        query = '''
        SELECT 
            ad.army_number, 
            p.name,
            p.rank,
            p.company,
            ad.det_id, 
            d.det_name, 
            ad.assigned_on,
            ad.det_status,
            DATEDIFF(NOW(), ad.assigned_on) AS days_on_det
        FROM assigned_det ad
        LEFT JOIN dets d ON ad.det_id = d.det_id
        LEFT JOIN personnel p ON ad.army_number = p.army_number
        WHERE DATEDIFF(NOW(), ad.assigned_on) > 5
          AND ad.det_status = 1
        '''

        params = []

        # Apply company filter if user is not Admin
        if user_company != "Admin":
            query += " AND p.company = %s"
            params.append(user_company)

        query += " ORDER BY ad.assigned_on ASC"

        cursor.execute(query, params)
        rows = cursor.fetchall()

        return jsonify({"status": "success", "rows": rows})

    except Exception as e:
        print("Error fetching assigned alarms:", e)
        return jsonify({"status": "error", "message": str(e)})

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()



@app.route("/api/leave_pending_alarm", methods=["GET"])
def leave_pending_alarm():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    user = require_login()
    role = user['role']

    try:
        query = """
            SELECT
                COUNT(*) AS pending_count
            FROM leave_status_info
            WHERE request_status LIKE 'Pending%'
            AND updated_at < NOW() - INTERVAL 5 MINUTE
        """
        cursor.execute(query)
        result = cursor.fetchone()
        if role != 'CO':
            result['pending_count'] = 0
            print(result,"THIS IS RESULT FOR ALARM")

        return jsonify({
            "pending": result["pending_count"]
        })

    except Exception as e:
        print(str(e))
        return jsonify({
            "pending": 0,
            "error": str(e)
        }), 500

    finally:
        cursor.close()
        conn.close()





@app.route('/api/today_event_alarm')
def today_event_alarm():
    user = require_login()  # Get logged-in user
    user_company = user['company']
    print("Logged-in user's company:", user_company)

    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        query = """
            SELECT id, event_name, venue
            FROM daily_events
            WHERE event_date = CURDATE()
        """

        params = []

        # Apply company filter if not Admin
        if user_company != "Admin":
            query += " AND company = %s"  # assuming there is a 'company' column
            params.append(user_company)

        cursor.execute(query, params)
        rows = cursor.fetchall()

        return jsonify({"status": "success", "rows": rows})

    except Exception as e:
        print("Error fetching today's events:", e)
        return jsonify({"status": "error", "message": str(e)})

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()




# ===============================================
# PROJECTS
# ===============================================

@app.route('/projects')
def get_projects():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    user = require_login()
    company = user['company']

    try:
        # 1️⃣ Fetch projects
        project_query = """
            SELECT project_id, head, project_name, current_stage, project_cost, project_items, quantity, project_description
            FROM projects
        """
        params = []

        # Apply company filter if not Admin
        if company != "Admin":
            project_query += " WHERE company = %s"
            params.append(company)

        cursor.execute(project_query, params)
        projects = cursor.fetchall()

        # 2️⃣ Fetch all heads from project_heads table
        cursor.execute("SELECT id, head_name, created_at FROM project_heads ORDER BY head_name ASC")
        heads = cursor.fetchall()  # List of dicts: [{'id':1, 'head_name':'John', 'created_at':...}, ...]

        # 3️⃣ Render template with both projects and heads
        return render_template("projects/projects.html", projects=projects, heads=heads)

    except Exception as e:
        print("Error fetching projects or heads:", str(e))
        return "Server Error", 500

    finally:
        cursor.close()
        conn.close()




@app.route("/add_project", methods=["POST"])
def add_project():
    data = request.form
    print(data)
    user = require_login()
    user_company = user['company']

    project_items_json = json.dumps(data.get('project_items', ''))

    project_cost = float(data.get("project_cost", 0))
    quantity = int(data.get("quantity", 0))

    values = (
        data.get("project_name", ""),
        data.get("head", ""),
        data.get("current_stage", ""),
        project_cost,
        project_items_json,
        quantity,
        data.get("project_description", ""),
        user_company
    )

    print("Inserting values:", values)
    print("Values count:", len(values))  # Should print 8

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO projects (
            project_name,
            head,
            current_stage,
            project_cost,
            project_items,
            quantity,
            project_description,
            company
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """, values)
    conn.commit()
    conn.close()

    return jsonify({"status": "success"})


@app.route("/get_projects_count", methods=["GET"])
def get_project_count():
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('select count(*) as count from projects')
    project_count = cursor.fetchone()
    count = project_count['count']
    conn.close()
    return jsonify({"status": "success",'count':count})


@app.route('/update_project_stage', methods=['POST'])
def update_project_stage():
    print('update api called')
    data = request.get_json()
    project_id = data.get('project_id')
    new_stage = data.get('new_stage')

    if not project_id or not new_stage:
        return jsonify({"status": "error", "message": "Missing project ID or stage"}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE projects
            SET current_stage = %s
            WHERE project_id = %s
        """, (new_stage, project_id))
        conn.commit()
        conn.close()
        return jsonify({"status": "success"})
    except Exception as e:
        print("Error updating stage:", e)
        return jsonify({"status": "error", "message": "Database error"}), 500


# Add new head
@app.route('/add_head', methods=['POST'])
def add_head():
    data = request.get_json()
    head_name = data.get("head_name").strip()
    if not head_name:
        return jsonify(status='error', message='Head name cannot be empty')
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO project_heads (head_name) VALUES (%s)", (head_name,))
        conn.commit()
        return jsonify(status='success')
    except mysql.connector.IntegrityError:
        return jsonify(status='error', message='Head already exists')
    except Exception as e:
        return jsonify(status='error', message=str(e))


@app.route("/search_officer")
def search_officer():
    name_query = request.args.get("name", "")

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT name,`rank`, company
        FROM personnel
        WHERE name LIKE %s AND `rank` = 'JCO'
        LIMIT 10
    """, (f"%{name_query}%",))

    results = cursor.fetchall()
    cursor.close()
    conn.close()

    return jsonify(results)


@app.route('/get_man_power')
def manPower():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        query= 'select count(*) as total_count from personnel'
        cursor.execute(query,)
        total_count = cursor.fetchone()
        count = total_count['total_count']
        return jsonify({'count':count}),200
    except Exception as e:
        print('There was an exception',str(e))
        return jsonify({'error':'Internal Server Error'}),500


@app.route('/api/get-parade-count')
def get_parade_count():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT `rank`, `company`, COUNT(*) AS count 
        FROM personnel
        GROUP BY `rank`, `company`
        ORDER BY `rank`;
    """)

    results = cursor.fetchall()

    cursor.close()
    conn.close()

    formatted = {}

    for row in results:
        rank = row['rank']
        company_name = row['company']
        count = row['count']

        company_number = ''.join(filter(str.isdigit, company_name))
        company_key = f"c{company_number}"

        if rank not in formatted:
            formatted[rank] = {"c1": 0, "c2": 0, "c3": 0, "c4": 0}

        formatted[rank][company_key] = count

    return jsonify(formatted)


@app.route('/api/unfit-graph')
def line_unfit_graph():
    company = request.args.get('company', 'All')
    print('the value is',company)

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT month, unfit_count
        FROM monthly_medical_status
        WHERE year = YEAR(CURDATE())
          AND unit = %s
        ORDER BY month
    """, (company,))
    result = cursor.fetchall()
    return jsonify(result)





# single route for all dashboard

@app.route('/api/dashboard_summary', methods=['GET'])
def dashboard_summary():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    user = require_login()
    company = user['company']
    print("Logged-in user's company:", company)
    
    try:
        # 1️⃣ Detachments Count
        cursor.execute(
            "SELECT COUNT(*) AS count FROM personnel WHERE detachment_status = 1" + 
            (f" AND company = %s" if company != "Admin" else ""),
            (company,) if company != "Admin" else ()
        )
        detachment_result = cursor.fetchone()
        detachments = detachment_result['count'] if detachment_result else 0

        # 2️⃣ Total Manpower
        cursor.execute(
            "SELECT COUNT(*) AS total_count FROM personnel" + 
            (f" WHERE company = %s" if company != "Admin" else ""),
            (company,) if company != "Admin" else ()
        )
        manpower_result = cursor.fetchone()
        manpower = manpower_result['total_count'] if manpower_result else 0

        # 3️⃣ Interview Pending
        cursor.execute(
            "SELECT SUM(interview_status = 0) AS pending_count, COUNT(*) AS total_count FROM personnel" + 
            (f" WHERE company = %s" if company != "Admin" else ""),
            (company,) if company != "Admin" else ()
        )
        interview_result = cursor.fetchone()
        pending_count = interview_result['pending_count'] if interview_result else 0
        total_interview_count = interview_result['total_count'] if interview_result else 0
        interview_percentage = round((pending_count / total_interview_count) * 100, 2) if total_interview_count > 0 else 0

        # 4️⃣ Projects Count
        cursor.execute("SELECT COUNT(*) AS count FROM projects")
        projects_result = cursor.fetchone()
        projects = projects_result['count'] if projects_result else 0

        # 5️⃣ Assigned Alarm (Assignments older than 5 days)
        cursor.execute(
            '''
            SELECT 
                ad.army_number, 
                p.name,
                p.rank,
                p.company,
                ad.det_id, 
                d.det_name, 
                ad.assigned_on,
                ad.det_status,
                DATEDIFF(NOW(), ad.assigned_on) AS days_on_det
            FROM assigned_det ad
            LEFT JOIN dets d ON ad.det_id = d.det_id
            LEFT JOIN personnel p ON ad.army_number = p.army_number
            WHERE DATEDIFF(NOW(), ad.assigned_on) > 5
              AND ad.det_status = 1
              ''' + (f" AND p.company = %s" if company != "Admin" else "") +
            '''
            ORDER BY ad.assigned_on ASC;
            ''',
            (company,) if company != "Admin" else ()
        )
        assigned_alarm_rows = cursor.fetchall()

        # 6️⃣ Sensitive Personnel Count
        cursor.execute(
            '''
            SELECT COUNT(*) AS count
            FROM sensitive_marking sm
            LEFT JOIN personnel p ON sm.army_number = p.army_number
            ''' + (f" WHERE p.company = %s" if company != "Admin" else ""),
            (company,) if company != "Admin" else ()
        )
        sensitive_result = cursor.fetchone()
        sensitive_count = sensitive_result['count'] if sensitive_result else 0
        # 7️⃣ Boards Count
        cursor.execute("SELECT COUNT(*) AS count FROM boards")
        boards_result = cursor.fetchone()
        boards_count = boards_result['count'] if boards_result else 0


        # Return combined JSON
        return jsonify({
            "status": "success",
            "detachments": detachments,
            "manpower": manpower,
            "interview": {
                "pending_count": pending_count,
                "total_count": total_interview_count,
                "percentage": interview_percentage
            },
            "projects": projects,
            "boards_count": boards_count, 
            "assigned_alarm": assigned_alarm_rows,
            "sensitive_count": sensitive_count
        }), 200

    except Exception as e:
        print("Error fetching dashboard summary:", str(e))
        return jsonify({"status": "error", "message": "Internal Server Error"}), 500

    finally:
        cursor.close()
        conn.close()
        
@app.route('/api/user-info', methods=['GET'])
def get_user_info():
    """Get current user information"""
    user = get_current_user()
    if not user:
        return jsonify({'success': False, 'error': 'Unauthorized'}), 401
    
    return jsonify({
        'success': True,
        'username': user.get('username'),
        'company': user.get('company'),
        'role': user.get('role')
    })

def get_current_user():
    """Get current user from JWT token"""
    token = request.cookies.get('token')
    if not token:
        return None
    
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        return payload
    except:
        return None

def get_column_name(index):
    """Helper to map index to column names"""
    columns = [
        'auth', 'hs', 'posted_str', 'lve', 'course', 'det', 'mh',
        'sick_lve', 'ex', 'td', 'att', 'awl_osl_jc', 'trout_det',
        'present_det', 'present_unit', 'dues_in', 'dues_out'
    ]
    return columns[index] if index < len(columns) else f'col_{index}'

@app.route('/api/parade-state/get/<date_str>', methods=['GET'])
def get_parade_state(date_str):
    """Get parade state with calculated columns"""
    print(f"\n=== GET PARADE STATE for date: {date_str} ===")
    
    # Get current user
    user = get_current_user()
    if not user:
        return jsonify({'success': False, 'error': 'Unauthorized'}), 401
    
    company = user.get('company')
    if not company:
        return jsonify({'success': False, 'error': 'No company assigned'}), 400
    
    print(f"User: {user.get('username')}, Company: {company}")
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    try:
        # FIX: Use datetime.strptime and date.today() correctly
        requested_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        today_date = date.today()
        
        # If user is trying to access future date, return error
        if requested_date > today_date:
            return jsonify({
                'success': False,
                'error': 'Cannot access data for future dates',
                'is_future': True
            }), 400
        
        # Get data for specific date and company
        cursor.execute("""
            SELECT * FROM parade_state_daily 
            WHERE report_date = %s AND company = %s
        """, (date_str, company))
        
        row = cursor.fetchone()
        
        # If no data found for today, try to get previous day's data
        if not row and requested_date == today_date:
            print(f"No data found for today ({date_str}), trying previous day...")
            
            # Get previous day's date
            previous_date = today_date - timedelta(days=1)
            cursor.execute("""
                SELECT * FROM parade_state_daily 
                WHERE report_date = %s AND company = %s
            """, (previous_date.strftime('%Y-%m-%d'), company))
            
            row = cursor.fetchone()
            
            if row:
                print(f"Using previous day's data ({previous_date}) as template")
                row['is_previous_day_template'] = True
                row['original_date'] = row['report_date']
                row['report_date'] = date_str
                
        elif not row:
            print(f"No data found for date: {date_str}, company: {company}")
            return jsonify({
                'success': False,
                'message': 'No data found for this date'
            }), 404
        
        print(f"Data found for {date_str}")
        
        # Convert database row back to frontend format
        result = {
            'date': row['report_date'],
            'company': row['company'],
            'data': {}
        }
        
        # Add flags if using previous day's data
        if 'is_previous_day_template' in row:
            result['is_previous_day_template'] = True
            result['original_date'] = row['original_date']
        
        # All categories in the exact order they appear in frontend
        all_categories = [
            'offr', 'jco', 'jcoEre', 'or', 'orEre',
            'firstTotal',
            'oaOr', 'attSummary', 'attOffr', 'attJco', 'attOr',
            'secondTotal',
            'grandTotal'
        ]
        
        for category in all_categories:
            category_data = []
            for i in range(17):
                column_name = f"{category}_{get_column_name(i)}"
                category_data.append(row.get(column_name, 0))
            result['data'][category] = category_data
        
        result['calculations'] = {
            't_out_formula': 'LVE + COURSE + MH + SICK/LVE + EX + TD + ATT + AWL/OSL/JC',
            'present_det': 'Same as DET column value',
            'present_unit': 'POSTED/STR - T/OUT'
        }
        
        return jsonify({
            'success': True,
            'data': result
        })
        
    except Exception as e:
        print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/api/parade-state/save', methods=['POST'])
def save_parade_state():
    """Save parade state data with calculated columns"""
    print("\n=== SAVE PARADE STATE ===")
    
    # Get current user
    user = get_current_user()
    if not user:
        return jsonify({'success': False, 'error': 'Unauthorized'}), 401
    
    company = user.get('company')
    if not company:
        return jsonify({'success': False, 'error': 'No company assigned'}), 400
    
    print(f"User: {user.get('username')}, Company: {company}")
    
    try:
        data = request.get_json()
        print(f"Received data for date: {data.get('date')}")
        
        if not data:
            return jsonify({'success': False, 'error': 'No data received'}), 400
            
        report_date_str = data.get('date')
        parade_data = data.get('data')
        
        if not report_date_str or not parade_data:
            return jsonify({'success': False, 'error': 'Missing date or data'}), 400
        
        # Check if user is trying to save data for future date
        requested_date = datetime.strptime(report_date_str, '%Y-%m-%d').date()
        today_date = date.today()
        
        if requested_date > today_date:
            return jsonify({
                'success': False,
                'error': 'Cannot save data for future dates',
                'is_future': True
            }), 400
        
        conn = get_db_connection()
        if not conn:
            return jsonify({'success': False, 'error': 'Database connection failed'}), 500
        
        cursor = conn.cursor()
        
        try:
            # All input categories from your frontend
            input_categories = [
                'offr', 'jco', 'jcoEre', 'or', 'orEre',  # First section
                'oaOr', 'attSummary', 'attOffr', 'attJco', 'attOr'  # Second section
            ]
            
            # Build SQL columns and values
            columns = ['report_date', 'company']
            values = [report_date_str, company]
            
            # Process each input category with calculations
            for category in input_categories:
                category_data = parade_data.get(category, [0]*17)
                print(f"Processing {category}: raw data = {category_data}")
                
                # Ensure we have at least 13 values (minimum needed for calculations)
                if len(category_data) < 13:
                    # Pad with zeros if needed
                    category_data = category_data + [0] * (13 - len(category_data))
                
                # Extract values for calculations
                posted_str = category_data[2] if len(category_data) > 2 else 0
                lve = category_data[3] if len(category_data) > 3 else 0
                course = category_data[4] if len(category_data) > 4 else 0
                det_value = category_data[5] if len(category_data) > 5 else 0
                mh = category_data[6] if len(category_data) > 6 else 0
                sick_lve = category_data[7] if len(category_data) > 7 else 0
                ex = category_data[8] if len(category_data) > 8 else 0
                td = category_data[9] if len(category_data) > 9 else 0
                att = category_data[10] if len(category_data) > 10 else 0
                awl_osl_jc = category_data[11] if len(category_data) > 11 else 0
                
                # CORRECTED: Calculate T/OUT = LVE + COURSE + MH + SICK/LVE + EX + TD + ATT + AWL/OSL/JC
                trout = lve + course + mh + sick_lve + ex + td + att + awl_osl_jc
                # Ensure non-negative
                trout = max(0, trout)
                
                # PRESENT/STR DET = DET column value
                present_det = det_value
                
                # PRESENT/STR UNIT = POSTED/STR - T/OUT
                present_unit = posted_str - trout
                # Ensure non-negative
                present_unit = max(0, present_unit)
                
                # Create final array with calculated values
                final_data = [
                    category_data[0] if len(category_data) > 0 else 0,  # AUTH
                    category_data[1] if len(category_data) > 1 else 0,  # H/S
                    posted_str,  # POSTED/STR
                    lve,         # LVE
                    course,      # COURSE
                    det_value,   # DET
                    mh,          # MH
                    sick_lve,    # SICK/LVE
                    ex,          # EX
                    td,          # TD
                    att,         # ATT
                    awl_osl_jc,  # AWL/OSL/JC
                    trout,       # T/OUT (calculated)
                    present_det, # PRESENT/STR DET (from DET column)
                    present_unit, # PRESENT/STR UNIT (calculated)
                    category_data[15] if len(category_data) > 15 else 0,  # DUES IN
                    category_data[16] if len(category_data) > 16 else 0   # DUES OUT
                ]
                
                print(f"{category} - Posted/STR: {posted_str}, T/OUT: {trout}, Present Det: {present_det}, Present Unit: {present_unit}")
                
                # Add each of the 17 columns for this category
                for i in range(17):
                    column_name = f"{category}_{get_column_name(i)}"
                    columns.append(column_name)
                    values.append(final_data[i])
            
            # Calculate FIRST TOTAL (sum of offr, jco, jcoEre, or, orEre)
            first_total_values = [0] * 17
            for cat in ['offr', 'jco', 'jcoEre', 'or', 'orEre']:
                cat_data = parade_data.get(cat, [0]*17)
                # Apply same calculations for totals
                if len(cat_data) >= 13:
                    posted_str = cat_data[2] if len(cat_data) > 2 else 0
                    lve = cat_data[3] if len(cat_data) > 3 else 0
                    course = cat_data[4] if len(cat_data) > 4 else 0
                    mh = cat_data[6] if len(cat_data) > 6 else 0
                    sick_lve = cat_data[7] if len(cat_data) > 7 else 0
                    ex = cat_data[8] if len(cat_data) > 8 else 0
                    td = cat_data[9] if len(cat_data) > 9 else 0
                    att = cat_data[10] if len(cat_data) > 10 else 0
                    awl_osl_jc = cat_data[11] if len(cat_data) > 11 else 0
                    
                    # CORRECTED: T/OUT = sum of deductions
                    trout = lve + course + mh + sick_lve + ex + td + att + awl_osl_jc
                    trout = max(0, trout)                                               
                    
                    present_unit = posted_str - trout
                    present_unit = max(0, present_unit)
                    
                    # Sum all columns
                    for i in range(17):
                        if i == 12:  # T/OUT
                            first_total_values[i] += trout
                        elif i == 14:  # PRESENT/STR UNIT
                            first_total_values[i] += present_unit
                        elif i < len(cat_data):
                            first_total_values[i] += cat_data[i]
                        else:
                            first_total_values[i] += 0
            
            # Store first total in database
            for i in range(17):
                column_name = f"firstTotal_{get_column_name(i)}"
                columns.append(column_name)
                values.append(first_total_values[i])
            
            # Calculate SECOND TOTAL (sum of oaOr, attSummary, attOffr, attJco, attOr)
            second_total_values = [0] * 17
            for cat in ['oaOr', 'attSummary', 'attOffr', 'attJco', 'attOr']:
                cat_data = parade_data.get(cat, [0]*17)
                if len(cat_data) >= 13:
                    posted_str = cat_data[2] if len(cat_data) > 2 else 0
                    lve = cat_data[3] if len(cat_data) > 3 else 0
                    course = cat_data[4] if len(cat_data) > 4 else 0
                    mh = cat_data[6] if len(cat_data) > 6 else 0
                    sick_lve = cat_data[7] if len(cat_data) > 7 else 0
                    ex = cat_data[8] if len(cat_data) > 8 else 0
                    td = cat_data[9] if len(cat_data) > 9 else 0
                    att = cat_data[10] if len(cat_data) > 10 else 0
                    awl_osl_jc = cat_data[11] if len(cat_data) > 11 else 0
                    
                    # CORRECTED: T/OUT = sum of deductions
                    trout = lve + course + mh + sick_lve + ex + td + att + awl_osl_jc
                    trout = max(0, trout)
                    
                    present_unit = posted_str - trout
                    present_unit = max(0, present_unit)
                    
                    # Sum all columns
                    for i in range(17):
                        if i == 12:  # T/OUT
                            second_total_values[i] += trout
                        elif i == 14:  # PRESENT/STR UNIT
                            second_total_values[i] += present_unit
                        elif i < len(cat_data):
                            second_total_values[i] += cat_data[i]
                        else:
                            second_total_values[i] += 0
            
            # Store second total in database
            for i in range(17):
                column_name = f"secondTotal_{get_column_name(i)}"
                columns.append(column_name)
                values.append(second_total_values[i])
            
            # Calculate GRAND TOTAL (firstTotal + secondTotal)
            grand_total_values = [0] * 17
            for i in range(17):
                grand_total_values[i] = first_total_values[i] + second_total_values[i]
            
            # Store grand total in database
            for i in range(17):
                column_name = f"grandTotal_{get_column_name(i)}"
                columns.append(column_name)
                values.append(grand_total_values[i])
            
            print(f"Total columns: {len(columns)}")
            print(f"Grand Total Auth: {grand_total_values[0]}, Present Unit: {grand_total_values[14]}")
            
            # Build SQL query
            placeholders = ['%s'] * len(values)
            
            sql = f"""
                INSERT INTO parade_state_daily ({', '.join(columns)})
                VALUES ({', '.join(placeholders)})
                ON DUPLICATE KEY UPDATE
                {', '.join([f"{col} = VALUES({col})" for col in columns if col not in ['report_date', 'company']])},
                updated_at = NOW()
            """
            
            print(f"Executing SQL...")
            cursor.execute(sql, values)
            conn.commit()
            
            return jsonify({
                'success': True,
                'message': f'Parade state saved for {report_date_str} ({company})',
                'calculations': {
                    't_out_calculation': 'LVE + COURSE + MH + SICK/LVE + EX + TD + ATT + AWL/OSL/JC',
                    'present_det': 'Same as DET column',
                    'present_unit': 'POSTED/STR - T/OUT'
                }
            })
            
        except Exception as e:
            conn.rollback()
            print(f"ERROR: {str(e)}")
            import traceback
            traceback.print_exc()
            return jsonify({'success': False, 'error': str(e)}), 500
            
        finally:
            cursor.close()
            conn.close()
            
    except Exception as e:
        print(f"General error: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)}), 500
    

# co dashboard view
# Add these routes to your Flask app (app.py)

@app.route('/api/co-dashboard/all-data/<date_str>', methods=['GET'])
def get_co_all_dashboard_data(date_str):
    """Get all CO dashboard data in a single request for a specific date"""
    user = require_login()
    
    if user['role'] != 'CO':
        return jsonify({'success': False, 'error': 'Unauthorized - CO access only'}), 403
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    try:
        cursor.execute("""
            SELECT 
                SUM(grandTotal_auth) as total_auth,
                SUM(grandTotal_present_unit) as present_unit,
                SUM(grandTotal_trout_det) as total_out,
                COUNT(DISTINCT company) as company_count
            FROM parade_state_daily
            WHERE report_date = %s
        """, (date_str,))
        parade_summary = cursor.fetchone()
        
        cursor.execute("""
            SELECT 
                company,
                grandTotal_lve as on_leave,
                grandTotal_auth as total_strength,
                ROUND((grandTotal_lve / NULLIF(grandTotal_auth, 0) * 100), 2) as leave_percentage
            FROM parade_state_daily
            WHERE report_date = %s
            ORDER BY company
        """, (date_str,))
        leave_data = cursor.fetchall()
        
        cursor.execute("""
            SELECT 
                company,
                (offr_auth + attOffr_auth) as officers,
                (jco_auth + jcoEre_auth + attJco_auth) as jcos,
                (or_auth + orEre_auth + oaOr_auth + attOr_auth) as other_ranks
            FROM parade_state_daily
            WHERE report_date = %s
            ORDER BY company
        """, (date_str,))
        manpower_data = cursor.fetchall()
        
        if not parade_summary or parade_summary['company_count'] == 0:
            return jsonify({
                'success': False,
                'message': 'No data found for this date'
            }), 404
        
        total_on_leave = sum(row['on_leave'] or 0 for row in leave_data)
        total_strength = sum(row['total_strength'] or 0 for row in leave_data)
        total_leave_percentage = round((total_on_leave / total_strength * 100), 2) if total_strength > 0 else 0
        
        for row in manpower_data:
            row['total'] = (row['officers'] or 0) + (row['jcos'] or 0) + (row['other_ranks'] or 0)
        
        total_officers = sum(row['officers'] or 0 for row in manpower_data)
        total_jcos = sum(row['jcos'] or 0 for row in manpower_data)
        total_other_ranks = sum(row['other_ranks'] or 0 for row in manpower_data)
        total_manpower = total_officers + total_jcos + total_other_ranks
        
        return jsonify({
            'success': True,
            'data': {
                'parade_summary': {
                    'total_auth': parade_summary['total_auth'] or 0,
                    'present_unit': parade_summary['present_unit'] or 0,
                    'total_out': parade_summary['total_out'] or 0,
                    'company_count': parade_summary['company_count'] or 0,
                    'report_date': date_str
                },
                'leave_status': {
                    'by_company': leave_data,
                    'total': {
                        'on_leave': total_on_leave,
                        'total_strength': total_strength,
                        'leave_percentage': total_leave_percentage
                    }
                },
                'manpower': {
                    'by_company': manpower_data,
                    'total': {
                        'officers': total_officers,
                        'jcos': total_jcos,
                        'other_ranks': total_other_ranks,
                        'total': total_manpower
                    }
                }
            }
        })
        
    except Exception as e:
        print(f"Error fetching CO dashboard data: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()
        
# Add this new route to your Flask app (app.py)
# Place it near your other CO dashboard endpoints

@app.route('/api/co-dashboard/parade-table/<date_str>', methods=['GET'])
def get_co_aggregated_parade_table(date_str):
    """Get aggregated parade state data from all companies for CO view"""
    user = require_login()
    
    if user['role'] != 'CO':
        return jsonify({'success': False, 'error': 'Unauthorized - CO access only'}), 403
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    try:
        # Get all companies' data for the specified date
        cursor.execute("""
            SELECT * FROM parade_state_daily
            WHERE report_date = %s
        """, (date_str,))
        
        companies_data = cursor.fetchall()
        
        if not companies_data:
            return jsonify({
                'success': False,
                'message': 'No data found for this date'
            }), 404
        
        # Initialize aggregated data structure
        aggregated = {
            'date': date_str,
            'company': 'ALL COMPANIES (CO VIEW)',
            'data': {}
        }
        
        # All categories to aggregate
        all_categories = [
            'offr', 'jco', 'jcoEre', 'or', 'orEre',
            'firstTotal',
            'oaOr', 'attSummary', 'attOffr', 'attJco', 'attOr',
            'secondTotal',
            'grandTotal'
        ]
        column_names = [
            'auth', 'hs', 'posted_str', 'lve', 'course', 'det', 'mh',
            'sick_lve', 'ex', 'td', 'att', 'awl_osl_jc', 'trout_det',
            'present_det', 'present_unit', 'dues_in', 'dues_out'
        ]
        for category in all_categories:
            aggregated['data'][category] = [0] * 17
        
        for company_row in companies_data:
            for category in all_categories:
                for i, col_name in enumerate(column_names):
                    db_column = f"{category}_{col_name}"
                    if db_column in company_row:
                        aggregated['data'][category][i] += (company_row[db_column] or 0)
        
        return jsonify({
            'success': True,
            'data': aggregated,
            'companies_count': len(companies_data)
        })
        
    except Exception as e:
        print(f"Error fetching CO aggregated parade table: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()
    
if __name__ == '__main__':
    app.run(debug=True, port=1000)