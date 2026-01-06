from imports import *
import os
from datetime import date
from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
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
    return render_template('dashboard.html', username = username,role = user['role'])


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
def search_person():
    print("in this route")

    query = request.form.get('army_number')  # ✅ CORRECT
    print(query)

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
    search = request.args.get("search", "").strip()
    try:
        query = """
            SELECT name, army_number, home_state,company
            FROM personnel
            WHERE interview_status = 0
        """
        params = []

        if search:
            query += " AND army_number LIKE %s"
            params.append(f"%{search}%")

        
        cursor.execute(query, params)
        data = cursor.fetchall()
        return jsonify({"status": "success", "data": data})

    except Exception as e:
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
def index():
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
        ORDER BY ad.assigned_on ASC;
        '''

        cursor.execute(query)
        rows = cursor.fetchall()

        return jsonify({"status": "success", "rows": rows})

    except Exception as e:
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
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
        SELECT id, event_name, venue
        FROM daily_events
        WHERE event_date = CURDATE()
    """
    cursor.execute(query)
    rows = cursor.fetchall()

    return jsonify({"rows": rows})



# ===============================================
# PROJECTS
# ===============================================

@app.route('/projects')
def get_projects():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT project_id, head, project_name, current_stage, project_cost, project_items, quantity, project_description
        FROM projects
    """)
    projects = cursor.fetchall()
    conn.close()
    return render_template("projects/projects.html", projects=projects)




@app.route("/add_project", methods=["POST"])
def add_project():
    data = request.form
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
            project_description
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (
        data["project_name"],
        data["head"],              # ✅ NEW
        data["current_stage"],
        data["project_cost"],
        data['project_items'],
        data["quantity"],
        data["project_description"]
    ))

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

def log_audit(parade_state_id, action_type, performed_by, ip_address=None, 
              user_agent=None, old_data=None, new_data=None, changes=None):
    """Log audit trail"""
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO parade_state_audit 
                (parade_state_id, action_type, performed_by, ip_address, 
                 user_agent, old_data, new_data, changes_summary)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                parade_state_id, action_type, performed_by, ip_address,
                user_agent,
                json.dumps(old_data) if old_data else None,
                json.dumps(new_data) if new_data else None,
                changes
            ))
            conn.commit()
            cursor.close()
        except Exception as e:
            logger.error(f"Error logging audit: {e}")
        finally:
            conn.close()

# API Routes

@app.route('/api/parade-state/save', methods=['POST'])
def save_parade_state():
    """Save or update parade state data"""
    try:
        data = request.get_json()
        report_date = data.get('date')
        parade_data = data.get('data')
        metadata = data.get('metadata', {})
        user = request.headers.get('X-User', 'anonymous')
        
        if not report_date or not parade_data:
            return jsonify({
                'success': False, 
                'error': 'Missing required data'
            }), 400
        
        conn = get_db_connection()
        if not conn:
            return jsonify({
                'success': False,
                'error': 'Database connection failed'
            }), 500
        
        cursor = conn.cursor(dictionary=True)
        
        try:
            # Calculate totals
            total_auth = sum(parade_data.get('grandTotal', [0]))
            total_present = parade_data.get('grandTotal', [0])[14] if len(parade_data.get('grandTotal', [])) > 14 else 0
            
            # Check if record exists for this date
            cursor.execute(
                'SELECT id, status FROM parade_state_main WHERE report_date = %s',
                (report_date,)
            )
            existing = cursor.fetchone()
            
            if existing:
                # Update existing record
                parade_state_id = existing['id']
                old_status = existing['status']
                
                cursor.execute("""
                    UPDATE parade_state_main 
                    SET report_title = %s, location = %s, prepared_by = %s,
                        approved_by = %s, status = %s, total_auth = %s,
                        total_present = %s, updated_by = %s, updated_at = NOW()
                    WHERE id = %s
                """, (
                    metadata.get('title'),
                    metadata.get('location'),
                    metadata.get('prepared_by'),
                    metadata.get('approved_by'),
                    metadata.get('status', 'draft'),
                    total_auth,
                    total_present,
                    user,
                    parade_state_id
                ))
                
                # Get old data for audit
                cursor.execute(
                    'SELECT * FROM parade_state_details WHERE parade_state_id = %s',
                    (parade_state_id,)
                )
                old_details = cursor.fetchall()
                
                # Delete old details
                cursor.execute(
                    'DELETE FROM parade_state_details WHERE parade_state_id = %s',
                    (parade_state_id,)
                )
                
                action_type = 'update'
                changes = f"Updated parade state for {report_date}"
                
            else:
                # Insert new record
                cursor.execute("""
                    INSERT INTO parade_state_main 
                    (report_date, report_title, location, prepared_by, approved_by,
                     status, total_auth, total_present, created_by, updated_by)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    report_date,
                    metadata.get('title'),
                    metadata.get('location'),
                    metadata.get('prepared_by'),
                    metadata.get('approved_by'),
                    metadata.get('status', 'draft'),
                    total_auth,
                    total_present,
                    user,
                    user
                ))
                parade_state_id = cursor.lastrowid
                action_type = 'create'
                changes = f"Created new parade state for {report_date}"
            
            # Insert all category data
            categories = [
                'offr', 'jco', 'jcoEre', 'or', 'orEre',
                'oaOr', 'attSummary', 'attOffr', 'attJco', 'attOr',
                'firstTotal', 'secondTotal', 'grandTotal'
            ]
            
            for category in categories:
                if category in parade_data and isinstance(parade_data[category], list):
                    values = parade_data[category]
                    
                    # Ensure we have exactly 18 values
                    padded_values = values + [0] * (18 - len(values)) if len(values) < 18 else values[:18]
                    
                    cursor.execute("""
                        INSERT INTO parade_state_details 
                        (parade_state_id, category, auth, hs, posted_str, lve, course, det, mh,
                         sick_lve, ex, td, att, awl_osl_jc, trout_det, unit, present, dues_in, dues_out, remarks)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """, (
                        parade_state_id, category,
                        padded_values[0], padded_values[1], padded_values[2], 
                        padded_values[3], padded_values[4], padded_values[5],
                        padded_values[6], padded_values[7], padded_values[8], 
                        padded_values[9], padded_values[10], padded_values[11],
                        padded_values[12], padded_values[13], padded_values[14],
                        padded_values[15], padded_values[16], padded_values[17]
                    ))
            
            # Update daily statistics
            update_daily_statistics(report_date, parade_state_id, cursor)
            
            conn.commit()
            
            # Log audit
            ip_address = request.remote_addr
            user_agent = request.headers.get('User-Agent')
            log_audit(parade_state_id, action_type, user, ip_address, user_agent, 
                     old_data if existing else None, parade_data, changes)
            
            return jsonify({
                'success': True,
                'message': 'Parade state saved successfully',
                'id': parade_state_id,
                'date': report_date
            }), 200
            
        except Exception as e:
            conn.rollback()
            logger.error(f'Error saving parade state: {str(e)}')
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500
            
        finally:
            cursor.close()
            conn.close()
            
    except Exception as e:
        logger.error(f'Unexpected error in save_parade_state: {str(e)}')
        return jsonify({
            'success': False,
            'error': 'Internal server error'
        }), 500


def update_daily_statistics(report_date, parade_state_id, cursor):
    """Update daily statistics table"""
    try:
        # Get category-wise data
        categories = ['offr', 'jco', 'or']
        stats = {}
        
        for category in categories:
            cursor.execute("""
                SELECT auth, present FROM parade_state_details 
                WHERE parade_state_id = %s AND category = %s
            """, (parade_state_id, category))
            result = cursor.fetchone()
            if result:
                stats[f'{category}_auth'] = result['auth'] or 0
                stats[f'{category}_present'] = result['present'] or 0
        
        # Get grand total
        cursor.execute("""
            SELECT auth, present FROM parade_state_details 
            WHERE parade_state_id = %s AND category = 'grandTotal'
        """, (parade_state_id,))
        grand_total = cursor.fetchone()
        
        if grand_total:
            total_auth = grand_total['auth'] or 0
            total_present = grand_total['present'] or 0
            total_absent = total_auth - total_present if total_auth > total_present else 0
            
            cursor.execute("""
                INSERT INTO daily_statistics 
                (report_date, total_records, total_auth, total_present, total_absent,
                 offr_auth, offr_present, jco_auth, jco_present, or_auth, or_present)
                VALUES (%s, 1, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                total_auth = VALUES(total_auth),
                total_present = VALUES(total_present),
                total_absent = VALUES(total_absent),
                offr_auth = VALUES(offr_auth),
                offr_present = VALUES(offr_present),
                jco_auth = VALUES(jco_auth),
                jco_present = VALUES(jco_present),
                or_auth = VALUES(or_auth),
                or_present = VALUES(or_present),
                updated_at = NOW()
            """, (
                report_date, total_auth, total_present, total_absent,
                stats.get('offr_auth', 0), stats.get('offr_present', 0),
                stats.get('jco_auth', 0), stats.get('jco_present', 0),
                stats.get('or_auth', 0), stats.get('or_present', 0)
            ))
            
    except Exception as e:
        logger.error(f'Error updating daily statistics: {str(e)}')


@app.route('/api/parade-state/<date>', methods=['GET'])
def get_parade_state(date):
    """Retrieve parade state by date"""
    conn = get_db_connection()
    if not conn:
        return jsonify({
            'success': False,
            'error': 'Database connection failed'
        }), 500
    
    cursor = conn.cursor(dictionary=True)
    
    try:
        # Get main record
        cursor.execute("""
            SELECT * FROM parade_state_main 
            WHERE report_date = %s
        """, (date,))
        main = cursor.fetchone()
        
        if not main:
            return jsonify({
                'success': False,
                'message': 'No data found for this date'
            }), 404
        
        # Get all details
        cursor.execute("""
            SELECT * FROM parade_state_details 
            WHERE parade_state_id = %s
            ORDER BY FIELD(category, 
                'offr', 'jco', 'jcoEre', 'or', 'orEre',
                'firstTotal', 'oaOr', 'attSummary', 'attOffr', 
                'attJco', 'attOr', 'secondTotal', 'grandTotal'
            )
        """, (main['id'],))
        details = cursor.fetchall()
        
        # Format data for frontend
        formatted_data = {}
        for detail in details:
            formatted_data[detail['category']] = [
                detail['auth'], detail['hs'], detail['posted_str'],
                detail['lve'], detail['course'], detail['det'],
                detail['mh'], detail['sick_lve'], detail['ex'],
                detail['td'], detail['att'], detail['awl_osl_jc'],
                detail['trout_det'], detail['unit'], detail['present'],
                detail['dues_in'], detail['dues_out']
            ]
        
        return jsonify({
            'success': True,
            'data': {
                'main': main,
                'details': formatted_data
            }
        }), 200
        
    except Exception as e:
        logger.error(f'Error retrieving parade state: {str(e)}')
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
        
    finally:
        cursor.close()
        conn.close()


@app.route('/api/parade-state/search', methods=['GET'])
def search_parade_states():
    """Search parade states with filters"""
    try:
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        status = request.args.get('status')
        location = request.args.get('location')
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 20))
        offset = (page - 1) * limit
        
        conn = get_db_connection()
        if not conn:
            return jsonify({
                'success': False,
                'error': 'Database connection failed'
            }), 500
        
        cursor = conn.cursor(dictionary=True)
        
        try:
            # Build query
            query = """
                SELECT 
                    m.id, m.report_date, m.report_title, m.location,
                    m.prepared_by, m.approved_by, m.status,
                    m.total_auth, m.total_present,
                    m.created_by, m.created_at, m.updated_at,
                    COUNT(d.id) as detail_count
                FROM parade_state_main m
                LEFT JOIN parade_state_details d ON m.id = d.parade_state_id
                WHERE 1=1
            """
            params = []
            
            if start_date:
                query += " AND m.report_date >= %s"
                params.append(start_date)
            
            if end_date:
                query += " AND m.report_date <= %s"
                params.append(end_date)
            
            if status:
                query += " AND m.status = %s"
                params.append(status)
            
            if location:
                query += " AND m.location LIKE %s"
                params.append(f"%{location}%")
            
            query += " GROUP BY m.id ORDER BY m.report_date DESC LIMIT %s OFFSET %s"
            params.extend([limit, offset])
            
            cursor.execute(query, params)
            results = cursor.fetchall()
            
            # Get total count
            count_query = "SELECT COUNT(*) as total FROM parade_state_main WHERE 1=1"
            count_params = []
            
            if start_date:
                count_query += " AND report_date >= %s"
                count_params.append(start_date)
            
            if end_date:
                count_query += " AND report_date <= %s"
                count_params.append(end_date)
            
            if status:
                count_query += " AND status = %s"
                count_params.append(status)
            
            if location:
                count_query += " AND location LIKE %s"
                count_params.append(f"%{location}%")
            
            cursor.execute(count_query, count_params)
            total_count = cursor.fetchone()['total']
            
            return jsonify({
                'success': True,
                'data': results,
                'pagination': {
                    'page': page,
                    'limit': limit,
                    'total': total_count,
                    'pages': (total_count + limit - 1) // limit
                }
            }), 200
            
        except Exception as e:
            logger.error(f'Error searching parade states: {str(e)}')
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500
            
        finally:
            cursor.close()
            conn.close()
            
    except Exception as e:
        logger.error(f'Unexpected error in search: {str(e)}')
        return jsonify({
            'success': False,
            'error': 'Internal server error'
        }), 500


@app.route('/api/parade-state/list', methods=['GET'])
def list_parade_states():
    """List all parade states with pagination"""
    conn = get_db_connection()
    if not conn:
        return jsonify({
            'success': False,
            'error': 'Database connection failed'
        }), 500
    
    cursor = conn.cursor(dictionary=True)
    
    try:
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 50))
        offset = (page - 1) * limit
        
        cursor.execute("""
            SELECT 
                m.id, m.report_date, m.report_title, m.location,
                m.status, m.total_auth, m.total_present,
                m.created_by, m.created_at, m.updated_at,
                (SELECT COUNT(*) FROM parade_state_details WHERE parade_state_id = m.id) as detail_count
            FROM parade_state_main m
            ORDER BY m.report_date DESC
            LIMIT %s OFFSET %s
        """, (limit, offset))
        results = cursor.fetchall()
        
        cursor.execute("SELECT COUNT(*) as total FROM parade_state_main")
        total_count = cursor.fetchone()['total']
        
        return jsonify({
            'success': True,
            'data': results,
            'pagination': {
                'page': page,
                'limit': limit,
                'total': total_count,
                'pages': (total_count + limit - 1) // limit
            }
        }), 200
        
    except Exception as e:
        logger.error(f'Error listing parade states: {str(e)}')
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
        
    finally:
        cursor.close()
        conn.close()


@app.route('/api/parade-state/export/csv/<date>', methods=['GET'])
def export_parade_state_csv(date):
    """Export parade state to CSV"""
    conn = get_db_connection()
    if not conn:
        return jsonify({
            'success': False,
            'error': 'Database connection failed'
        }), 500
    
    cursor = conn.cursor(dictionary=True)
    
    try:
        # Get main record
        cursor.execute(
            'SELECT * FROM parade_state_main WHERE report_date = %s',
            (date,)
        )
        main = cursor.fetchone()
        
        if not main:
            return jsonify({
                'success': False,
                'message': 'No data found for this date'
            }), 404
        
        # Get all details
        cursor.execute(
            'SELECT * FROM parade_state_details WHERE parade_state_id = %s',
            (main['id'],)
        )
        details = cursor.fetchall()
        
        # Create CSV
        output = StringIO()
        writer = csv.writer(output)
        
        # Write headers
        headers = ['Category', 'AUTH', 'H/S', 'POSTED/STR', 'LVE', 'COURSE', 'DET', 'MH',
                   'SICK/LVE', 'EX', 'TD', 'ATT', 'AWL/OSL/JC', 'T/OUT', 'PRESENT DET',
                   'PRESENT UNIT', 'DUES IN', 'DUES OUT']
        writer.writerow(headers)
        
        # Write data
        for detail in details:
            row = [
                detail['category'],
                detail['auth'], detail['hs'], detail['posted_str'],
                detail['lve'], detail['course'], detail['det'],
                detail['mh'], detail['sick_lve'], detail['ex'],
                detail['td'], detail['att'], detail['awl_osl_jc'],
                detail['trout_det'], detail['unit'], detail['present'],
                detail['dues_in'], detail['dues_out']
            ]
            writer.writerow(row)
        
        # Log export
        exported_by = request.headers.get('X-User', 'anonymous')
        log_export_history(main['id'], 'csv', exported_by, cursor)
        
        # Prepare response
        csv_data = output.getvalue()
        output.close()
        
        response = BytesIO(csv_data.encode('utf-8-sig'))
        
        return send_file(
            response,
            mimetype='text/csv',
            as_attachment=True,
            download_name=f'parade_state_{date}.csv'
        )
        
    except Exception as e:
        logger.error(f'Error exporting CSV: {str(e)}')
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
        
    finally:
        cursor.close()
        conn.close()


def log_export_history(parade_state_id, export_type, exported_by, cursor):
    """Log export history"""
    try:
        cursor.execute("""
            INSERT INTO export_history 
            (parade_state_id, exported_by, export_type)
            VALUES (%s, %s, %s)
        """, (parade_state_id, exported_by, export_type))
    except Exception as e:
        logger.error(f'Error logging export history: {str(e)}')


@app.route('/api/parade-state/stats/<date>', methods=['GET'])
def get_parade_stats(date):
    """Get statistics for a specific parade state"""
    conn = get_db_connection()
    if not conn:
        return jsonify({
            'success': False,
            'error': 'Database connection failed'
        }), 500
    
    cursor = conn.cursor(dictionary=True)
    
    try:
        cursor.execute(
            'SELECT id FROM parade_state_main WHERE report_date = %s',
            (date,)
        )
        main = cursor.fetchone()
        
        if not main:
            return jsonify({
                'success': False,
                'message': 'No data found for this date'
            }), 404
        
        # Get grand total row
        cursor.execute("""
            SELECT auth, hs, posted_str, lve, course, det, mh, 
                   sick_lve, ex, td, att, awl_osl_jc, trout_det, 
                   unit, present, dues_in, dues_out
            FROM parade_state_details 
            WHERE parade_state_id = %s AND category = 'grandTotal'
        """, (main['id'],))
        
        grand_total = cursor.fetchone()
        
        # Get category breakdown
        cursor.execute("""
            SELECT category, auth, present FROM parade_state_details 
            WHERE parade_state_id = %s AND category IN ('offr', 'jco', 'or')
        """, (main['id'],))
        categories = cursor.fetchall()
        
        return jsonify({
            'success': True,
            'stats': {
                'grand_total': grand_total,
                'categories': categories
            }
        }), 200
        
    except Exception as e:
        logger.error(f'Error getting parade stats: {str(e)}')
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
        
    finally:
        cursor.close()
        conn.close()


@app.route('/api/parade-state/dashboard/stats', methods=['GET'])
def get_dashboard_stats():
    """Get dashboard statistics"""
    conn = get_db_connection()
    if not conn:
        return jsonify({
            'success': False,
            'error': 'Database connection failed'
        }), 500
    
    cursor = conn.cursor(dictionary=True)
    
    try:
        # Today's date
        today = date.today().isoformat()
        
        # Get total records count
        cursor.execute("SELECT COUNT(*) as total FROM parade_state_main")
        total_records = cursor.fetchone()['total']
        
        # Get today's record if exists
        cursor.execute(
            "SELECT * FROM parade_state_main WHERE report_date = %s",
            (today,)
        )
        today_record = cursor.fetchone()
        
        # Get recent records
        cursor.execute("""
            SELECT report_date, total_auth, total_present 
            FROM parade_state_main 
            ORDER BY report_date DESC LIMIT 5
        """)
        recent_records = cursor.fetchall()
        
        # Get status distribution
        cursor.execute("""
            SELECT status, COUNT(*) as count 
            FROM parade_state_main 
            GROUP BY status
        """)
        status_distribution = cursor.fetchall()
        
        return jsonify({
            'success': True,
            'stats': {
                'total_records': total_records,
                'today_record': today_record,
                'recent_records': recent_records,
                'status_distribution': status_distribution
            }
        }), 200
        
    except Exception as e:
        logger.error(f'Error getting dashboard stats: {str(e)}')
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
        
    finally:
        cursor.close()
        conn.close()


@app.route('/api/parade-state/<date>', methods=['DELETE'])
def delete_parade_state(date):
    """Delete parade state by date"""
    conn = get_db_connection()
    if not conn:
        return jsonify({
            'success': False,
            'error': 'Database connection failed'
        }), 500
    
    cursor = conn.cursor(dictionary=True)
    user = request.headers.get('X-User', 'anonymous')
    
    try:
        # Get the record ID
        cursor.execute(
            'SELECT id FROM parade_state_main WHERE report_date = %s',
            (date,)
        )
        main = cursor.fetchone()
        
        if not main:
            return jsonify({
                'success': False,
                'message': 'No data found for this date'
            }), 404
        
        parade_state_id = main['id']
        
        # Log audit before deletion
        ip_address = request.remote_addr
        user_agent = request.headers.get('User-Agent')
        log_audit(parade_state_id, 'delete', user, ip_address, user_agent, 
                 None, None, f"Deleted parade state for {date}")
        
        # Delete details first (foreign key constraint)
        cursor.execute(
            'DELETE FROM parade_state_details WHERE parade_state_id = %s',
            (parade_state_id,)
        )
        
        # Delete main record
        cursor.execute(
            'DELETE FROM parade_state_main WHERE id = %s',
            (parade_state_id,)
        )
        
        conn.commit()
        
        return jsonify({
            'success': True,
            'message': 'Parade state deleted successfully'
        }), 200
        
    except Exception as e:
        conn.rollback()
        logger.error(f'Error deleting parade state: {str(e)}')
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
        
    finally:
        cursor.close()
        conn.close()


@app.route('/api/parade-state/update-status/<date>', methods=['PUT'])
def update_parade_status(date):
    """Update parade state status"""
    try:
        data = request.get_json()
        new_status = data.get('status')
        user = request.headers.get('X-User', 'anonymous')
        
        if not new_status:
            return jsonify({
                'success': False,
                'error': 'Status is required'
            }), 400
        
        conn = get_db_connection()
        if not conn:
            return jsonify({
                'success': False,
                'error': 'Database connection failed'
            }), 500
        
        cursor = conn.cursor(dictionary=True)
        
        try:
            # Get current record
            cursor.execute(
                'SELECT id, status FROM parade_state_main WHERE report_date = %s',
                (date,)
            )
            main = cursor.fetchone()
            
            if not main:
                return jsonify({
                    'success': False,
                    'message': 'No data found for this date'
                }), 404
            
            old_status = main['status']
            
            # Update status
            cursor.execute("""
                UPDATE parade_state_main 
                SET status = %s, updated_by = %s, updated_at = NOW()
                WHERE id = %s
            """, (new_status, user, main['id']))
            
            conn.commit()
            
            # Log audit
            ip_address = request.remote_addr
            user_agent = request.headers.get('User-Agent')
            log_audit(main['id'], 'update', user, ip_address, user_agent,
                     {'status': old_status}, {'status': new_status},
                     f"Status changed from {old_status} to {new_status}")
            
            return jsonify({
                'success': True,
                'message': 'Status updated successfully'
            }), 200
            
        except Exception as e:
            conn.rollback()
            logger.error(f'Error updating status: {str(e)}')
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500
            
        finally:
            cursor.close()
            conn.close()
            
    except Exception as e:
        logger.error(f'Unexpected error in update_status: {str(e)}')
        return jsonify({
            'success': False,
            'error': 'Internal server error'
        }), 500


@app.route('/api/parade-state/audit/<date>', methods=['GET'])
def get_parade_audit_logs(date):
    """Get audit logs for a parade state"""
    conn = get_db_connection()
    if not conn:
        return jsonify({
            'success': False,
            'error': 'Database connection failed'
        }), 500
    
    cursor = conn.cursor(dictionary=True)
    
    try:
        cursor.execute(
            'SELECT id FROM parade_state_main WHERE report_date = %s',
            (date,)
        )
        main = cursor.fetchone()
        
        if not main:
            return jsonify({
                'success': False,
                'message': 'No data found for this date'
            }), 404
        
        cursor.execute("""
            SELECT * FROM parade_state_audit 
            WHERE parade_state_id = %s 
            ORDER BY performed_at DESC
            LIMIT 100
        """, (main['id'],))
        
        logs = cursor.fetchall()
        
        return jsonify({
            'success': True,
            'logs': logs
        }), 200
        
    except Exception as e:
        logger.error(f'Error getting audit logs: {str(e)}')
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
        
    finally:
        cursor.close()
        conn.close()



if __name__ == '__main__':
    app.run(debug=True, port=1000)