from flask import Flask, jsonify, redirect, render_template, request, url_for
import sqlite3

import mysql
from blueprints.personal_information import personnel_info
from blueprints.weight_ms import weight_ms
app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 31536000  # Cache static files for 1 year (in seconds)


app.register_blueprint(personnel_info)
app.register_blueprint(weight_ms)




def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",                # 
        password="qaz123QAZ!@#",   # 🔹 your MySQL password
        database="army_personnel_db"       # 🔹 the database you created
    )

@app.route('/')
def dashboard():
    return render_template('dashboard.html')


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

    return render_template('mtView.html', vehicles=vehicles, drivers=drivers, maintenance=maintenance)
    
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
    cursor.execute("""
        SELECT name, army_number, `rank`, trade, company
        FROM personnel
        WHERE name LIKE %s OR trade LIKE %s
    """, (f"%{query}%", f"%{query}%"))
    results = cursor.fetchall()
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
    cursor.execute("SELECT COUNT(*) AS count FROM dets")
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return jsonify({'count': result['count']})



# Assign selected personnel
@app.route('/assign_personnel', methods=['POST'])
def assign_personnel():
    data = request.get_json()
    print("data", data)
    personnel_ids = data.get('army_number', [])
    location_id = data.get('det_id')

    if not personnel_ids or not location_id:
        return jsonify({"error": "Missing data"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    for pid in personnel_ids:
        cursor.execute("""
            INSERT INTO assigned_det (army_number, det_id)
            VALUES (%s, %s)
        """, (pid, location_id))
    conn.commit()
    conn.close()
    return jsonify({"message": "Personnel assigned successfully"})


if __name__ == '__main__':
    app.run(debug=True, port=1000)


