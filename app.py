from imports import *
import os
from datetime import date

app = Flask(__name__)
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

@app.route('/search_personnel')
def search_person():
    query = request.args.get('query', '')
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
            onleave_status as leave_status
        FROM personnel
        WHERE army_number = %s
    """, (query,))

    results = cursor.fetchall()
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
            "marked_on": r[3],
            "name": r[4],
            "rank": r[5],
            "company": r[6]
        })
    
    cursor.close()
    conn.close()
    
    # Prevent browser caching
    response = make_response(render_template("sensitive_indl/mark_personnel.html", sensitive_list=sensitive_list))
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response


@app.route("/mark_sensitive", methods=["POST"])
def mark_sensitive():
    army_number = request.form.get("army_number")
    reason = request.form.get("reason")
    
    if not army_number or not reason:
        return "Missing data", 400

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""INSERT INTO sensitive_marking (army_number, reason, marked_on)
                          VALUES (%s, %s, %s)""", (army_number, reason, datetime.now()))
        conn.commit()

        # Re-fetch updated list
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
                "id": r[0], "army_number": r[1], "reason": r[2], "marked_on": r[3],
                "name": r[4], "rank": r[5], "company": r[6]
            })

        return render_template("sensitive_indl/mark_personnel.html", sensitive_list=sensitive_list)

    except Exception as e:
        conn.rollback()
        print("ERROR in mark_sensitive:", e)
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()


@app.route("/update_sensitive_reason", methods=["POST"])
def update_sensitive_reason():
    army_number = request.form.get("army_number")
    reason = request.form.get("reason")
    
    if not army_number or not reason:
        return jsonify({"success": False, "error": "Missing data"}), 400
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("UPDATE sensitive_marking SET reason = %s WHERE army_number = %s", (reason, army_number))
        conn.commit()
        return jsonify({"success": True})
    except Exception as e:
        conn.rollback()
        print("Error:", e)
        return jsonify({"success": False, "error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()


@app.route("/remove_sensitive", methods=["POST"])
def remove_sensitive():
    army_number = request.form.get("army_number")
    
    if not army_number:
        return "Missing data", 400

    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("DELETE FROM sensitive_marking WHERE army_number = %s", (army_number,))
        conn.commit()

        # Re-fetch fresh list and re-render full page
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
                "id": r[0], "army_number": r[1], "reason": r[2], "marked_on": r[3],
                "name": r[4], "rank": r[5], "company": r[6]
            })

        return render_template("sensitive_indl/mark_personnel.html", sensitive_list=sensitive_list)

    except Exception as e:
        conn.rollback()
        print("ERROR in remove_sensitive:", e)
        return "Server error", 500
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

# ===============================================
# PROJECTS
# ===============================================

@app.route("/projects")
def home():
    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)

    filter_stage = request.args.get("stage", "all")

    if filter_stage == "aon":
        cur.execute("SELECT * FROM projects WHERE LOWER(current_stage) LIKE '%aon%'")
    elif filter_stage == "tob":
        cur.execute("SELECT * FROM projects WHERE LOWER(current_stage) LIKE '%tob%' OR LOWER(current_stage) LIKE '%tec%'")
    elif filter_stage == "atp":
        cur.execute("SELECT * FROM projects WHERE LOWER(current_stage) LIKE '%atp%'")
    elif filter_stage == "completed":
        cur.execute("SELECT * FROM projects WHERE LOWER(current_stage) LIKE '%atp%'")
    else:
        cur.execute("SELECT * FROM projects")

    projects = cur.fetchall()
    conn.close()

    for p in projects:
        p["percent"] = stage_to_percent(p["current_stage"])

    return render_template("projects/projects.html", projects=projects, filter_stage=filter_stage)

def stage_to_percent(stage):
    s = stage.strip().lower()

    if "aon" in s:
        return 33
    elif "tob" in s or "tec" in s:
        return 66
    elif "atp" in s:
        return 100
    return 0


@app.route("/add_project", methods=["POST"])
def add_project():
    data = request.form
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO projects (project_name, current_stage, project_cost, project_items, quantity, project_description)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (
        data["project_name"],
        data["current_stage"],
        data["project_cost"],
        data["project_items"],
        data["quantity"],
        data["project_description"]
    ))
    conn.commit()
    conn.close()
    return jsonify({"status": "success"})


@app.route("/update_stage", methods=["POST"])
def update_stage():
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute("""
        UPDATE projects SET current_stage=%s WHERE project_id=%s
    """, (request.form["new_stage"], request.form["project_id"]))

    conn.commit()
    conn.close()
    return jsonify({"status": "success"})


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


if __name__ == '__main__':
    app.run(debug=True, port=1000)