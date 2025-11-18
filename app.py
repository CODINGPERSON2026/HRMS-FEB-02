from flask import Flask, jsonify, redirect,flash, render_template, request, url_for
import mysql
from blueprints.personal_information import personnel_info
from blueprints.weight_ms import weight_ms
import pandas as pd
import os


app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 31536000  # Cache static files for 1 year (in seconds)
app.secret_key = os.urandom(24)

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
    

    # Stores code

@app.route('/stores')
def stores_dashboard():
    """Show overview of stores, and options to add store or view store details."""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT s.store_id,
            s.store_name,
            s.place,
            s.incharge_name,
            IFNULL(si.count_items, 0) AS total_items
        FROM stores s
        LEFT JOIN (
            SELECT store_id, COUNT(*) AS count_items
            FROM store_items
            GROUP BY store_id
        ) si ON s.store_id = si.store_id
        ORDER BY s.store_name
    """)
    stores = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('stores.html', stores=stores)

@app.route('/stores/add', methods=['POST'])
def add_store():
    store_name = request.form.get('store_name')
    place = request.form.get('place')
    incharge_name = request.form.get('incharge_name')

    if not store_name:
        flash("Store name is required", "danger")
        return redirect(url_for('stores_dashboard'))

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO stores (store_name, place, incharge_name) VALUES (%s, %s, %s)",
        (store_name, place, incharge_name)
    )
    conn.commit()
    cursor.close()
    conn.close()
    flash("Store added successfully", "success")
    return redirect(url_for('stores_dashboard'))

@app.route('/stores/<int:store_id>')
def view_store(store_id):
    """View individual store items and add new item form."""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # fetch store info
    cursor.execute("SELECT * FROM stores WHERE store_id = %s", (store_id,))
    store = cursor.fetchone()
    if not store:
        cursor.close()
        conn.close()
        flash("Store not found", "danger")
        return redirect(url_for('stores_dashboard'))

    # fetch items for this store
# fetch items for this store
    cursor.execute("""
        SELECT item_id, qlp_no, slp_no, NOMENCLATURE, AU, Quantity
        FROM store_items
        WHERE store_id = %s
    """, (store_id,))
    items = cursor.fetchall()


    cursor.close()
    conn.close()
    return render_template('store_view.html', store=store, items=items)

@app.route('/stores/<int:store_id>/add_item', methods=['POST'])
def add_item(store_id):
    qlp_no = request.form.get('qlp_no')
    slp_no = request.form.get('slp_no')
    NOMENCLATURE = request.form.get('NOMENCLATURE')
    AU = request.form.get('AU')
    Quantity = request.form.get('Quantity', '0')

    # basic validation
    if not NOMENCLATURE:
        flash("Nomenclature is required", "danger")
        return redirect(url_for('view_store', store_id=store_id))

    # normalize numeric quantity
    try:
        qty = float(Quantity)
    except ValueError:
        qty = 0.0

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO store_items (store_id, qlp_no, slp_no, NOMENCLATURE, AU, Quantity)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (store_id, qlp_no, slp_no, NOMENCLATURE, AU, qty))
    conn.commit()
    cursor.close()
    conn.close()
    flash("Item added to store", "success")
    return redirect(url_for('view_store', store_id=store_id))

# optional: delete item
@app.route('/stores/<int:store_id>/delete_item/<int:item_id>', methods=['POST'])
def delete_item(store_id, item_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM store_items WHERE item_id = %s AND store_id = %s", (item_id, store_id))
    conn.commit()
    cursor.close()
    conn.close()
    flash("Item deleted", "info")
    return redirect(url_for('view_store', store_id=store_id))

@app.route('/stores/delete/<int:store_id>', methods=['POST'])
def delete_store(store_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    # First delete all items inside the store (to avoid foreign key errors)
    cursor.execute("DELETE FROM store_items WHERE store_id = %s", (store_id,))

    # Now delete the store itself
    cursor.execute("DELETE FROM stores WHERE store_id = %s", (store_id,))
    conn.commit()

    cursor.close()
    conn.close()

    flash("Store deleted successfully", "info")
    return redirect(url_for('stores_dashboard'))

# Leave Application

@app.route('/apply_leave')
def apply_leave():
    return render_template('apply_leave.html')



if __name__ == '__main__':
    app.run(debug=True, port=1000)


