from flask import Flask, jsonify, render_template, request,Blueprint,redirect,url_for
import mysql.connector
import re
from middleware import require_login

weight_ms = Blueprint('weight', __name__, url_prefix='/weight_system')
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "password123",
    "database": "weight_management"
}

# --- Helper functions ---
def round_to_nearest_even(n):
    """
    Rounds a number to the nearest even integer.
    """
    rounded = round(n)
    if rounded % 2 != 0:
        if n > rounded:
            rounded += 1
        else:
            rounded -= 1
    return rounded

def get_ideal_weight(age, height_cm, cursor):
    cursor.execute("SELECT age_range, ideal_weight_kg FROM ideal_weights WHERE height_cm = %s", (height_cm,))
    rows = cursor.fetchall()
    for row in rows:
        age_range = row['age_range']
        ideal_weight = row['ideal_weight_kg']
        try:
            lower_age, upper_age = map(int, age_range.split('-'))
            if lower_age <= age <= upper_age:
                return float(ideal_weight)
        except:
            continue
    return None

def compute_authorization(company=None):
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor(dictionary=True)

    if company and company != "All":
        cursor.execute("SELECT army_number, name,`rank`,company, age, height, actual_weight,status_type FROM weight_info WHERE company = %s", (company,))
    else:
        cursor.execute("SELECT army_number, name,`rank`, company, age, height, actual_weight,status_type FROM weight_info")
    
    soldiers = cursor.fetchall()
    
    results = []

    for s in soldiers:
        age = s['age']
        height_cm = round_to_nearest_even(s['height'])
        actual_weight = s['actual_weight']
        name = s['name']
        company = s['company']
        army_number = s['army_number']
        rank = s['rank']
        status_type = s['status_type']

        ideal_weight = get_ideal_weight(age, height_cm, cursor)

        if ideal_weight is None:
            status = "No ideal weight found"
            lower = upper = None
            weight_deviation_percent = None
            weight_deviation_kg = None
        else:
            lower = round(ideal_weight * 0.9, 2)
            upper = round(ideal_weight * 1.1, 2)

            if lower <= actual_weight <= upper:
                status = "Fit"
                weight_deviation_kg = 0
                weight_deviation_percent = 0
            else:
                status = "UnFit"
                if actual_weight < lower:
                    deviation = lower - actual_weight
                    weight_deviation_kg = round(deviation, 1)
                    weight_deviation_percent = round((deviation / lower) * 100, 1)
                else:  # actual_weight > upper
                    deviation = actual_weight - upper
                    weight_deviation_kg = round(deviation, 1)
                    weight_deviation_percent = round((deviation / upper) * 100, 1)

        results.append({
            'army_number': army_number,
            "name": name,
            'rank':rank,
            "company": company,
            "age": age,
            "height_cm": height_cm,
            "actual_weight": actual_weight,
            "ideal_weight": ideal_weight,
            "lower_limit": lower,
            "upper_limit": upper,
            "status": status,
            "weight_deviation_percent": weight_deviation_percent,
            "weight_deviation_kg": weight_deviation_kg,
            "status_type" : status_type
        })

    cursor.close()
    connection.close()
    return results

# --- Validation functions ---
def validate_alpha(value, field_name):
    """Validate that value contains only letters and spaces"""
    if not re.match(r'^[a-zA-Z\s]+$', value):
        return f"{field_name} can only contain letters and spaces"
    return None

def validate_alpha_numeric(value, field_name):
    """Validate that value contains only letters and numbers"""
    if not re.match(r'^[a-zA-Z0-9]+$', value):
        return f"{field_name} can only contain letters and numbers"
    return None

def validate_numeric(value, field_name):
    """Validate that value is a valid number"""
    try:
        float(value)
        return None
    except ValueError:
        return f"{field_name} must be a valid number"

def validate_integer(value, field_name, min_val=None, max_val=None):
    """Validate that value is a valid integer within range"""
    try:
        int_val = int(value)
        if min_val is not None and int_val < min_val:
            return f"{field_name} must be at least {min_val}"
        if max_val is not None and int_val > max_val:
            return f"{field_name} must be at most {max_val}"
        return None
    except ValueError:
        return f"{field_name} must be a whole number"

# --- Existing Endpoints ---
@weight_ms.route('/api/add-user', methods=['POST'])
def add_user():
    try:
        # Get JSON data from request
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400

        # Extract fields
        name = data.get('name', '').strip()
        army_number = data.get('army_number', '').strip()
        age = data.get('age')
        rank = data.get('rank')
        height_cm = data.get('height_cm')
        actual_weight = data.get('actual_weight')
        company = data.get('company', '').strip()
        status_type = data.get('status_type', 'safe').strip()
        category_type = data.get('category_type')  # Can be None
        restrictions = data.get('restrictions')   # Can be None

        # Validate required fields
        required_fields = {
            'name': name,
            'army_number': army_number,
            'age': age,
            'rank': rank,
            'height_cm': height_cm,
            'actual_weight': actual_weight,
            'company': company,
            'status_type': status_type
        }
        
        for field, value in required_fields.items():
            if not value and value != 0:
                return jsonify({'error': f'{field.replace("_", " ").title()} is required'}), 400

        # Validate field formats
        validation_errors = []
        
        # Name validation (only letters and spaces)
        name_error = validate_alpha(name, 'Name')
        if name_error:
            validation_errors.append(name_error)
        
        # Army number validation (alphanumeric)
        army_number_error = validate_alpha_numeric(army_number, 'Army number')
        if army_number_error:
            validation_errors.append(army_number_error)
        
        # Age validation (integer between 18 and 60)
        age_error = validate_integer(age, 'Age', 18, 60)
        if age_error:
            validation_errors.append(age_error)
        
        # Height validation (integer between 100 and 250, convert to float for DB)
        height_error = validate_integer(height_cm, 'Height', 100, 250)
        if height_error:
            validation_errors.append(height_error)
        
        # Weight validation (numeric between 30 and 200)
        weight_error = validate_numeric(str(actual_weight), 'Weight')
        if weight_error:
            validation_errors.append(weight_error)
        else:
            weight_val = float(actual_weight)
            if weight_val < 30 or weight_val > 200:
                validation_errors.append('Weight must be between 30kg and 200kg')

        # Validate status_type
        if status_type not in ['safe', 'category']:
            validation_errors.append('Status type must be either "safe" or "category"')

        # Validate category_type and restrictions if status_type is 'category'
        if status_type == 'category':
            if category_type not in ['permanent', 'temporary']:
                validation_errors.append('Category type must be either "permanent" or "temporary"')
            if restrictions is None or not restrictions.strip():
                validation_errors.append('Restrictions are required when status type is "category"')

        if validation_errors:
            return jsonify({'error': '; '.join(validation_errors)}), 400

        # Convert to proper types
        age = int(age)
        height_cm = float(height_cm)
        actual_weight = float(actual_weight)

        # Check if army_number already exists
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor(dictionary=True)
        
        cursor.execute("SELECT army_number FROM weight_info WHERE army_number = %s", (army_number,))
        existing_user = cursor.fetchone()
        
        if existing_user:
            cursor.close()
            connection.close()
            return jsonify({'error': 'Army number already exists'}), 400

        # Calculate ideal weight using your existing function
        rounded_height = round_to_nearest_even(height_cm)
        ideal_weight = get_ideal_weight(age, rounded_height, cursor)

        if ideal_weight is None:
            cursor.close()
            connection.close()
            return jsonify({'error': 'Could not determine ideal weight for the given age and height'}), 400

        # Calculate limits and status
        lower_limit = round(ideal_weight * 0.9, 2)
        upper_limit = round(ideal_weight * 1.1, 2)

        if lower_limit <= actual_weight <= upper_limit:
            status = "Fit"
            weight_deviation_kg = 0
            weight_deviation_percent = 0
        else:
            status = "UnFit"
            if actual_weight < lower_limit:
                deviation = lower_limit - actual_weight
                weight_deviation_kg = round(deviation, 1)
                weight_deviation_percent = round((deviation / lower_limit) * 100, 1)
            else:
                deviation = actual_weight - upper_limit
                weight_deviation_kg = round(deviation, 1)
                weight_deviation_percent = round((deviation / upper_limit) * 100, 1)

        # Prepare and log the INSERT query
        query = "INSERT INTO weight_info (`name`, `army_number`, `age`, `rank`, `height`, `actual_weight`, `company`, `status_type`, `category_type`, `restrictions`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        # Log the exact query with values (for debugging)
        formatted_query = query % (f"'{name}'", f"'{army_number}'", age, f"'{rank}'", height_cm, actual_weight, f"'{company}'", f"'{status_type}'", f"'{category_type or 'NULL'}'", f"'{restrictions or 'NULL'}'")
        # Execute with parameterized values
        cursor.execute(query, (name, army_number, age, rank, height_cm, actual_weight, company, status_type, category_type, restrictions))

        connection.commit()
        
        # Get the inserted user's ID
        user_id = cursor.lastrowid
        
        cursor.close()
        connection.close()

        # Return success response
        return jsonify({
            'message': 'User added successfully',
            'user': {
                'id': user_id,
                'name': name,
                'army_number': army_number,
                'age': age,
                'rank': rank,
                'height_cm': height_cm,
                'actual_weight': actual_weight,
                'company': company,
                'status_type': status_type,
                'category_type': category_type,
                'restrictions': restrictions,
                'ideal_weight': ideal_weight,
                'lower_limit': lower_limit,
                'upper_limit': upper_limit,
                'status': status,
                'weight_deviation_kg': weight_deviation_kg,
                'weight_deviation_percent': weight_deviation_percent
            }
        }), 201

    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        if 'connection' in locals():
            connection.rollback()
            connection.close()
        return jsonify({'error': 'Database error occurred'}), 500

@weight_ms.route('/api/summary')
def api_summary():
    company = request.args.get('company', 'All')
    data = compute_authorization(company)
    total = len(data)
    unFit = sum(1 for d in data if d['status'] == "UnFit")
    Fit = sum(1 for d in data if d['status'] == "Fit")
    return jsonify({
        "total": total, 
        "unFit": unFit, 
        "Fit": Fit,
        "company": company
    })

@weight_ms.route('/api/unauthorized')
def api_unFit():
    company = request.args.get('company', 'All')
    data = compute_authorization(company)
    unFit = [d for d in data if d['status'] == "UnFit"]
    return jsonify({"count": len(unFit), "rows": unFit})

@weight_ms.route('/api/authorized')
def api_Fit():
    company = request.args.get('company', 'All')
    data = compute_authorization(company)
    Fit = [d for d in data if d['status'] == "Fit"]
    return jsonify({"count": len(Fit), "rows": Fit})

@weight_ms.route('/api/companies')
def api_companies():
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()
    cursor.execute("SELECT DISTINCT company FROM weight_info ORDER BY company")
    companies = [row[0] for row in cursor.fetchall()]
    
    cursor.close()
    connection.close()
    return jsonify({"companies": companies})

@weight_ms.route('/')
def dashboard():
    user = require_login()
    print(user)
    if not user:
        return redirect(url_for('admin_login'))
    return render_template('weight_system/home.html')

@weight_ms.route('/api/status-summary')
def api_status_summary():
    company = request.args.get('company', 'All')
    
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor(dictionary=True)
    
    try:
        if company and company != "All":
            cursor.execute("""
                SELECT 
                    status_type,
                    COUNT(*) as count
                FROM weight_info 
                WHERE company = %s
                GROUP BY status_type
            """, (company,))
        else:
            cursor.execute("""
                SELECT 
                    status_type,
                    COUNT(*) as count
                FROM weight_info 
                GROUP BY status_type
            """)
        
        status_counts = cursor.fetchall()
        
        # Initialize counts
        safe_count = 0
        category_count = 0
        
        # Extract counts from query results
        for row in status_counts:
            if row['status_type'] == 'safe':
                safe_count = row['count']
            elif row['status_type'] == 'category':
                category_count = row['count']
        
        return jsonify({
            "safe_count": safe_count,
            "category_count": category_count,
            "company": company
        })
        
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return jsonify({'error': 'Database error occurred'}), 500
    finally:
        cursor.close()
        connection.close()

@weight_ms.route('/api/status-data')
def api_status_data():
    status_type = request.args.get('status_type')
    company = request.args.get('company', 'All')
    
    if not status_type:
        return jsonify({'error': 'status_type parameter is required'}), 400
    
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor(dictionary=True)
    
    try:
        if company and company != "All":
            cursor.execute("""
                SELECT 
                    army_number, name, company,`rank`, age, height as height_cm, 
                    actual_weight, status_type, category_type, restrictions
                FROM weight_info 
                WHERE status_type = %s AND company = %s
                ORDER BY name
            """, (status_type, company))
        else:
            cursor.execute("""
                SELECT 
                    army_number, name, company,`rank`, age, height as height_cm, 
                    actual_weight, status_type, category_type, restrictions
                FROM weight_info 
                WHERE status_type = %s
                ORDER BY name
            """, (status_type,))
        
        users = cursor.fetchall()
        
        # Calculate fitness status for each user
        results = []
        for user in users:
            age = user['age']
            height_cm = round_to_nearest_even(user['height_cm'])
            actual_weight = user['actual_weight']
            
            ideal_weight = get_ideal_weight(age, height_cm, cursor)
            
            if ideal_weight is None:
                status = "No ideal weight found"
                lower = upper = None
                weight_deviation_percent = None
                weight_deviation_kg = None
            else:
                lower = round(ideal_weight * 0.9, 2)
                upper = round(ideal_weight * 1.1, 2)

                if lower <= actual_weight <= upper:
                    status = "Fit"
                    weight_deviation_kg = 0
                    weight_deviation_percent = 0
                else:
                    status = "UnFit"
                    if actual_weight < lower:
                        deviation = lower - actual_weight
                        weight_deviation_kg = round(deviation, 1)
                        weight_deviation_percent = round((deviation / lower) * 100, 1)
                    else:
                        deviation = actual_weight - upper
                        weight_deviation_kg = round(deviation, 1)
                        weight_deviation_percent = round((deviation / upper) * 100, 1)

            results.append({
                'army_number': user['army_number'],
                "name": user['name'],
                "company": user['company'],
                'rank':user['rank'],
                "age": user['age'],
                "height_cm": user['height_cm'],
                "actual_weight": user['actual_weight'],
                "status_type": user['status_type'],
                "category_type": user['category_type'],
                "restrictions": user['restrictions'],
                "ideal_weight": ideal_weight,
                "lower_limit": lower,
                "upper_limit": upper,
                "status": status,
                "weight_deviation_percent": weight_deviation_percent,
                "weight_deviation_kg": weight_deviation_kg
            })
        
        return jsonify({
            "count": len(results),
            "rows": results,
            "status_type": status_type,
            "company": company
        })
        
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return jsonify({'error': 'Database error occurred'}), 500
    finally:
        cursor.close()
        connection.close()
@weight_ms.route('/api/bar-graph-data')
def api_bar_graph_data():
    company = request.args.get('company', 'All')
    fit_unfit_filter = request.args.get('fitUnfitFilter', 'Fit')
    safe_category_filter = request.args.get('safeCategoryFilter', 'safe')  # 'safe' or 'category'
    
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor(dictionary=True)
    
    try:
        # === 1. Fit / Unfit counts (unchanged) ===
        data = compute_authorization(company)
        fit_count = sum(1 for d in data if d['status'] == "Fit")
        unfit_count = sum(1 for d in data if d['status'] == "UnFit")
        
        # === 2. JCO / OR counts for selected Fit/Unfit (unchanged) ===
        jco_status_count = sum(1 for d in data if d['status'] == fit_unfit_filter and d['rank'] == "JCO")
        or_status_count = sum(1 for d in data if d['status'] == fit_unfit_filter and d['rank'] != "JCO")
        
        # === 3. Total Safe & Category counts (unchanged) ===
        if company != "All":
            cursor.execute("SELECT COUNT(*) as count FROM weight_info WHERE company = %s AND status_type = 'safe'", (company,))
        else:
            cursor.execute("SELECT COUNT(*) as count FROM weight_info WHERE status_type = 'safe'")
        total_safe_count = cursor.fetchone()['count'] or 0
        
        if company != "All":
            cursor.execute("SELECT COUNT(*) as count FROM weight_info WHERE company = %s AND status_type = 'category'", (company,))
        else:
            cursor.execute("SELECT COUNT(*) as count FROM weight_info WHERE status_type = 'category'")
        total_category_count = cursor.fetchone()['count'] or 0


        # === 4. jcoSafeOrCategory – SMART LOGIC BASED ON FILTER ===
        if safe_category_filter == 'safe':
            # For "safe" → no temporary/permanent → just show total JCO vs OR
            if company != "All":
                cursor.execute("""
                    SELECT COUNT(*) as count FROM weight_info 
                    WHERE company = %s AND status_type = 'safe' AND `rank` = 'JCO'
                """, (company,))
            else:
                cursor.execute("SELECT COUNT(*) as count FROM weight_info WHERE status_type = 'safe' AND `rank` = 'JCO'")
            jco_val = cursor.fetchone()['count'] or 0

            if company != "All":
                cursor.execute("""
                    SELECT COUNT(*) as count FROM weight_info 
                    WHERE company = %s AND status_type = 'safe' AND `rank` != 'JCO'
                """, (company,))
            else:
                cursor.execute("SELECT COUNT(*) as count FROM weight_info WHERE status_type = 'safe' AND `rank` != 'JCO'")
            or_val = cursor.fetchone()['count'] or 0

            jcoSafeOrCategory = {
                "labels": ["JCO Safe", "OR Safe"],
                "data": [jco_val, or_val],
                
            }

        else:  # safe_category_filter == 'category'
            # For "category" → split into Temporary & Permanent
            query = """
                SELECT `rank`,
                       COALESCE(LOWER(TRIM(category_type)), 'unknown') AS cat_type,
                       COUNT(*) AS cnt
                FROM weight_info 
                WHERE status_type = 'category'
            """
            params = []
            if company != "All":
                query += " AND company = %s"
                params.append(company)
            query += " GROUP BY `rank`, category_type"

            cursor.execute(query, params)
            results = cursor.fetchall()
            print(results,"these are results")

            jco_temp = jco_perm = or_temp = or_perm = 0

            for row in results:
                rank = row['rank']
                cat_type = row['cat_type']
                cnt = row['cnt']

                if rank == 'JCO':
                    if cat_type in ('temporary', 'temp'):
                        jco_temp += cnt
                    elif cat_type in ('permanent', 'perm'):
                        jco_perm += cnt
                else:
                    # All other ranks = OR (including AGNIVEER, Havaldar, MAJOR, etc.)
                    if cat_type in ('temporary', 'temp'):
                        or_temp += cnt
                    elif cat_type in ('permanent', 'perm'):
                        or_perm += cnt

            print(jco_temp, jco_perm, or_temp, or_perm)

            jcoSafeOrCategory = {
                "labels": ["JCO Temporary", "JCO Permanent", "OR Temporary", "OR Permanent"],
                "data": [jco_temp, jco_perm, or_temp, or_perm],
                
            }


        print(total_safe_count, total_category_count, "→ bar graph")
        print(jco_status_count, or_status_count, "→ donut graph (fit)")

        return jsonify({
            "fitUnfit": {
                "labels": ["Fit", "Unfit"],
                "data": [fit_count, unfit_count]
            },
            "safeCategory": {
                "labels": ["Safe", "Category"],
                "data": [total_safe_count, total_category_count]
            },
            "jcoOrFit": {
                "labels": [f"JCO {fit_unfit_filter}", f"OR {fit_unfit_filter}"],
                "data": [jco_status_count, or_status_count]
            },
            "jcoSafeOrCategory": jcoSafeOrCategory   # ← Smart response
        })
        
    except mysql.connector.Error as err:
        print(f"DB Error: {err}")
        return jsonify({'error': 'Database error occurred'}), 500
    finally:
        cursor.close()
        connection.close()

# API Route to Get User by Army Number
@weight_ms.route('/api/user/<army_number>', methods=['GET'])
def get_user(army_number):
    connection = mysql.connector.connect(**db_config)
    if not connection:
        return jsonify({'error': 'Database connection failed'}), 500

    cursor = connection.cursor(dictionary=True)
    try:
        query = "SELECT * FROM weight_info WHERE army_number = %s"
        cursor.execute(query, (army_number,))
        
        user = cursor.fetchone()

        if not user:
            return jsonify({'error': 'User not found'}), 404

        return jsonify({
            'name': user['name'],
            'army_number': user['army_number'],
            'rank': user['rank'],
            'age': user['age'],
            'height_cm': user['height'],
            'actual_weight': user['actual_weight'],
            'company': user['company'],
            'status_type': user['status_type'],
            'category_type': user['category_type'],
            'restrictions': user['restrictions']
        })
    except mysql.connector.Error as e:
        print(f"Error fetching user: {e}")
        return jsonify({'error': 'Error fetching user'}), 500
    finally:
        cursor.close()
        connection.close()

# API Route to Update User
@weight_ms.route('/api/update-user', methods=['PUT'])
def update_user():
    connection = mysql.connector.connect(**db_config)
    if not connection:
        return jsonify({'error': 'Da;tabase connection failed'}), 500

    cursor = connection.cursor()
    data = request.get_json();
    army_number = data.get('army_number')

    try:
        # Check if user exists
        check_query = "SELECT COUNT(*) FROM weight_info WHERE army_number = %s"
        cursor.execute(check_query, (army_number,))
        if cursor.fetchone()[0] == 0:
            return jsonify({'error': 'User not found'}), 404

        # Update user data
        update_query = """
            UPDATE weight_info 
            SET name = %s, `rank`= %s, age = %s, height = %s, actual_weight = %s, 
                company = %s, status_type = %s, category_type = %s, restrictions = %s
            WHERE army_number = %s
        """
        cursor.execute(update_query, (
            data.get('name'),
            data.get('rank'),
            data.get('age'),
           data.get('height_cm'),
            data.get('actual_weight'),
            data.get('company'),
            data.get('status_type'),
            data.get('category_type'),
            data.get('restrictions'),
            army_number
        ))
        connection.commit()
        return jsonify({'message': 'User updated successfully'}), 200
    except mysql.connector.Error as e:
        connection.rollback()
        print(f"Error updating user: {e}")
        return jsonify({'error': 'Error updating user'}), 500
    finally:
        cursor.close()
        connection.close()
@weight_ms.route('/api/about-page')
def about():
    return render_template('/weight_system/about.html')
