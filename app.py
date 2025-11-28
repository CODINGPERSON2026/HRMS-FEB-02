from imports import *

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 31536000  # Cache static files for 1 year (in seconds)
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
    username  =  user['username']
    
    cursor.close()
    conn.close()

    if not user:
        return jsonify({"success": False, "error": "Invalid email or password"}), 401

    # create JWT
    payload = {
        "user_id": user["id"],
        "email": user["email"],
        'username':user['username'],
        "role": user["role"]
    }

    token = jwt.encode(payload, JWT_SECRET, algorithm="HS256")

    # set JWT in cookie
    resp = jsonify({"success": True,"username":username})
    resp.set_cookie("token", token, httponly=True, samesite="Lax")

    return resp

@app.route("/logout")
def logout():
    resp = redirect(url_for("admin_login"))  # change to your login route name
    resp.set_cookie("token", "", expires=0)  # delete cookie
    return resp



@app.route('/')
def dashboard():
    user = require_login()
    print(user)
    if not user:
        return redirect(url_for('admin_login'))
    return render_template('dashboard.html', username = user['username'],role = user['role'])


@app.route('/mt', methods=['GET', 'POST'])
def mt():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # 👉 If form submitted
    if request.method == 'POST':
        vehicle_no = request.form['vehicle_no']
        vtype = request.form['type']
        vclass = request.form['class']
        detailment = request.form['detailment']
        dist_travelled = request.form['dist_travelled']
        quantity = request.form['quantity']
        bullet_proof = request.form.get('bullet_proof', 'N')  # default N

        insert_query = """
            INSERT INTO Vehicle_detail 
            (vehicle_no, type, class, detailment, dist_travelled, quantity, bullet_proof)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(insert_query, (vehicle_no, vtype, vclass, detailment, dist_travelled, quantity, bullet_proof))
        conn.commit()

        cursor.close()
        conn.close()
        return redirect(url_for('mt'))  # reload page after add

    # 👉 Fetch vehicles for display
    cursor.execute("SELECT * FROM Vehicle_detail")
    vehicles = cursor.fetchall()
    cursor.close()
    conn.close()

    # Sample data for now
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
    print("in this app route")
    return render_template('personalInfoView.html')

@app.route('/personal/create', methods=['GET', 'POST'])
def create_personal():
    if request.method == 'POST':
        data = request.form.to_dict()
        print(data)  # For now, simulate saving to DB
        #return redirect(url_for('personal_info'))
    return render_template('personalInfoView.html', form_view='create')

@app.route('/personal/update')
def update_personal():
    return render_template('personalInfoView.html', form_view='update')

@app.route('/personal/view')
def view_personal():
    return render_template('personalInfoView.html', form_view='view')

@app.route('/search_personnel')
def search_personnel():
    query = request.args.get('query', '')
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    print(query)

    cursor.execute("""
        SELECT 
            name, 
            army_number, 
            `rank`, 
            trade, 
            company,
            detachment_status AS det_status,
            posting_status
        FROM personnel
        WHERE army_number = %s
    """, (query,))

    results = cursor.fetchall()
    print(results)
    conn.close()
    return jsonify(results)


# Fetch dropdown locations
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
    print(result['count'])
    cursor.close()
    conn.close()
    return jsonify({'count': result['count']})



# Assign selected personnel
@app.route('/assign_personnel', methods=['POST'])
def assign_personnel():
    data = request.get_json()
    print("data", data)

    personnel_ids = data.get('army_number', [])
    location_id = data.get('det_id')  # Can be det_id or posting branch
    action_type = data.get('action')  # 🔥 New field (det or posting)

    if not personnel_ids or not location_id or not action_type:
        return jsonify({"error": "Missing data"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # ============================
        #  CASE 1: DETACHMENT
        # ============================
        if action_type == "det":

            for pid in personnel_ids:
                cursor.execute("""
                    INSERT INTO assigned_det (army_number, det_id)
                    VALUES (%s, %s)
                """, (pid, location_id))

            cursor.executemany("""
                UPDATE personnel
                SET detachment_status = 1
                WHERE army_number = %s
            """, [(pid,) for pid in personnel_ids])


        # ============================
        #  CASE 2: POSTING
        # ============================
        elif action_type == "posting":

            for pid in personnel_ids:
                cursor.execute("""
                    INSERT INTO posting_details_table (army_number, action_type, posting_date)
                    VALUES (%s, %s, NOW())
                """, (pid, location_id))  # you can change action_type to location_id label if needed

            cursor.executemany("""
                UPDATE personnel
                SET posting_status = 1
                WHERE army_number = %s
            """, [(pid,) for pid in personnel_ids])


        else:
            return jsonify({"error": "Invalid action type"}), 400


        # Commit if no issues
        conn.commit()
        return jsonify({"message": "Personnel assigned successfully!"})

    except Exception as e:
        conn.rollback()
        print("❌ Error:", e)
        return jsonify({"error": "Assignment failed"}), 500

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
    

# Leave Application

@app.route('/apply_leave')
def apply_leave():
    return render_template('apply_leave.html')

@app.route('/daily_running')
def daily_running():
    return render_template('mt/daily_running.html')


@app.route('/get_vehicle_details', methods=['POST'])
def get_vehicle_details():
    vehicle_no = request.form.get('vehicle_no')
    print(vehicle_no)
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT type, class FROM vehicle_detail WHERE vehicle_no=%s", (vehicle_no,))
    result = cursor.fetchone()
    print(result)
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







# // ************************ ALARM FUNCTIONALITY//**************************

@app.route('/api/assigned_alarm')
def assigned_alarm():
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # Fetch all rows where assigned_on > 10 seconds and get det_name
        query = '''SELECT 
    ad.army_number, 
    p.name,
    ad.det_id, 
    d.det_name, 
    ad.assigned_on,
    ad.det_status
FROM assigned_det ad
LEFT JOIN dets d ON ad.det_id = d.det_id
LEFT JOIN personnel p ON ad.army_number = p.army_number
WHERE TIMESTAMPDIFF(SECOND, ad.assigned_on, NOW()) > 10
  AND ad.det_status = 1
ORDER BY ad.assigned_on ASC '''
        cursor.execute(query)
        rows = cursor.fetchall()
        print(rows,"this is rows")

        return jsonify({"status": "success", "rows": rows})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()














if __name__ == '__main__':
    app.run(debug=True, port=1000)


