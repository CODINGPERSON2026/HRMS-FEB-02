from flask import Flask, request, jsonify, render_template
import mysql.connector
from mysql.connector import Error
import json
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'yawar@123',
    'database': 'biodata_personnel',
    'autocommit': True
}

def get_db_connection():
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

# Dashboard route
@app.route('/')
def dashboard():
    connection = get_db_connection()
    if not connection:
        return "Database connection failed", 500
    
    cursor = connection.cursor(dictionary=True)
    
    try:
        # Get total personnel
        cursor.execute("SELECT COUNT(*) as total FROM personnel")
        total_personnel = cursor.fetchone()['total']
        
        # Get this month's additions
        cursor.execute("""
            SELECT COUNT(*) as count FROM personnel 
            WHERE MONTH(date_of_enrollment) = MONTH(CURRENT_DATE())
            AND YEAR(date_of_enrollment) = YEAR(CURRENT_DATE())
        """)
        this_month = cursor.fetchone()['count']
        
        # Get total courses
        cursor.execute("SELECT COUNT(*) as count FROM courses")
        total_courses = cursor.fetchone()['count']
        
        # Get medical cases (personnel with med_cat = 'Yes')
        cursor.execute("SELECT COUNT(*) as count FROM personnel WHERE med_cat = 'Yes'")
        medical_cases = cursor.fetchone()['count']
        
        stats = {
            'total_personnel': total_personnel,
            'this_month': this_month,
            'total_courses': total_courses,
            'medical_cases': medical_cases
        }
        
        # Get age distribution
        cursor.execute("""
            SELECT 
                CASE 
                    WHEN TIMESTAMPDIFF(YEAR, date_of_birth, CURDATE()) BETWEEN 18 AND 24 THEN '18-24'
                    WHEN TIMESTAMPDIFF(YEAR, date_of_birth, CURDATE()) BETWEEN 25 AND 30 THEN '25-30'
                    WHEN TIMESTAMPDIFF(YEAR, date_of_birth, CURDATE()) BETWEEN 31 AND 35 THEN '31-35'
                    WHEN TIMESTAMPDIFF(YEAR, date_of_birth, CURDATE()) BETWEEN 36 AND 40 THEN '36-40'
                    WHEN TIMESTAMPDIFF(YEAR, date_of_birth, CURDATE()) BETWEEN 40 AND 50 THEN '40-50'
                    WHEN TIMESTAMPDIFF(YEAR, date_of_birth, CURDATE()) BETWEEN 50 AND 60 THEN '50-60'
                    WHEN TIMESTAMPDIFF(YEAR, date_of_birth, CURDATE()) > 60 THEN '60+'
                    ELSE 'Unknown'
                END as age_range,
                COUNT(*) as count
            FROM personnel
            WHERE date_of_birth IS NOT NULL
            GROUP BY age_range
            ORDER BY age_range
        """)
        age_data = cursor.fetchall()
        
        age_distribution = []
        for row in age_data:
            percentage = round((row['count'] / total_personnel * 100), 1) if total_personnel > 0 else 0
            age_distribution.append({
                'range': row['age_range'],
                'count': row['count'],
                'percentage': percentage
            })
        
        # Get rank distribution
        cursor.execute("""
            SELECT `rank`, COUNT(*) as count 
            FROM personnel 
            GROUP BY `rank`
            ORDER BY count DESC
            LIMIT 10
        """)
        rank_distribution = cursor.fetchall()
        
        # Get recent personnel (last 5)
        cursor.execute("""
            SELECT name, army_number, `rank`, date_of_enrollment
            FROM personnel 
            ORDER BY id DESC 
            LIMIT 5
        """)
        recent_personnel = cursor.fetchall()
        
        return render_template('dashboard.html', 
                             stats=stats, 
                             age_distribution=age_distribution,
                             rank_distribution=rank_distribution,
                             recent_personnel=recent_personnel,
                             active_tab='dashboard')
    
    except Error as e:
        print(f"Database error: {e}")
        return f"Database error: {e}", 500
    finally:
        cursor.close()
        connection.close()

# View Data route - Lists personnel with med_cat = 'Yes'
@app.route('/personnel')
def view_personnel():
    connection = get_db_connection()
    if not connection:
        return "Database connection failed", 500
    
    cursor = connection.cursor(dictionary=True)
    
    try:
        # Get total medical cases
        cursor.execute("SELECT COUNT(*) as total FROM personnel WHERE med_cat = 'Yes'")
        total_medical = cursor.fetchone()['total']
        
        # Get company-wise distribution
        cursor.execute("""
            SELECT company, COUNT(*) as count 
            FROM personnel 
            WHERE med_cat = 'Yes'
            GROUP BY company
            ORDER BY company
        """)
        company_distribution = cursor.fetchall()
        
        # Get list of medical personnel
        cursor.execute("""
            SELECT id, name, army_number, date_of_birth, `rank`, trade, date_of_enrollment, med_cat, company
            FROM personnel 
            WHERE med_cat = 'Yes'
            ORDER BY company, id DESC
        """)
        medical_personnel = cursor.fetchall()
        
        return render_template('personnel.html', 
                             total_medical=total_medical,
                             medical_personnel=medical_personnel,
                             company_distribution=company_distribution,
                             active_tab='view-data')
    
    except Error as e:
        print(f"Database error: {e}")
        return f"Database error: {e}", 500
    finally:
        cursor.close()
        connection.close()

# API endpoint to get medical personnel details
@app.route('/api/medical-personnel')
def api_medical_personnel():
    connection = get_db_connection()
    if not connection:
        return jsonify({'success': False, 'message': 'Database connection failed'}), 500
    
    cursor = connection.cursor(dictionary=True)
    
    try:
        # Get total medical cases
        cursor.execute("SELECT COUNT(*) as total FROM personnel WHERE med_cat = 'Yes'")
        total_medical = cursor.fetchone()['total']
        
        # Get company-wise distribution
        cursor.execute("""
            SELECT company, COUNT(*) as count 
            FROM personnel 
            WHERE med_cat = 'Yes'
            GROUP BY company
            ORDER BY company
        """)
        company_distribution = cursor.fetchall()
        
        # Get list of medical personnel
        cursor.execute("""
            SELECT id, name, army_number, `rank`, trade, date_of_enrollment, med_cat, company
            FROM personnel 
            WHERE med_cat = 'Yes'
            ORDER BY id DESC
        """)
        medical_personnel = cursor.fetchall()
        
        # Convert date objects to strings for JSON serialization
        for person in medical_personnel:
            if person['date_of_enrollment']:
                person['date_of_enrollment'] = person['date_of_enrollment'].strftime('%Y-%m-%d')
        
        return jsonify({
            'success': True,
            'total_medical': total_medical,
            'company_distribution': company_distribution,
            'medical_personnel': medical_personnel
        })
    
    except Error as e:
        print(f"Database error: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500
    finally:
        cursor.close()
        connection.close()

# Personnel Details route
@app.route('/personnel/<int:personnel_id>')
def personnel_details(personnel_id):
    connection = get_db_connection()
    if not connection:
        return "Database connection failed", 500
    
    cursor = connection.cursor(dictionary=True)
    
    try:
        # Get main personnel details
        cursor.execute("""
            SELECT * FROM personnel WHERE id = %s
        """, (personnel_id,))
        personnel = cursor.fetchone()
        
        if not personnel:
            return "Personnel not found", 404
        
        # Fetch related data
        cursor.execute("""
            SELECT * FROM courses WHERE personnel_id = %s ORDER BY sr_no
        """, (personnel_id,))
        courses = cursor.fetchall()
        
        cursor.execute("""
            SELECT * FROM family_members WHERE personnel_id = %s
        """, (personnel_id,))
        family = cursor.fetchall()
        
        cursor.execute("""
            SELECT * FROM children WHERE personnel_id = %s ORDER BY sr_no
        """, (personnel_id,))
        children = cursor.fetchall()
        
        return render_template('personnel_details.html',
                             personnel=personnel,
                             courses=courses,
                             family=family,
                             children=children,
                             active_tab='view-data')
    
    except Error as e:
        print(f"Database error: {e}")
        return f"Database error: {e}", 500
    finally:
        cursor.close()
        connection.close()

# Add personnel page route
@app.route('/add-personnel')
def add_personnel_page():
    return render_template('index.html', active_tab='add-personnel')

# API endpoint for creating personnel
@app.route('/api/personnel', methods=['POST'])
def create_personnel():
    connection = get_db_connection()
    if not connection:
        return jsonify({'success': False, 'message': 'Database connection failed'}), 500

    cursor = connection.cursor()

    try:
        data = request.get_json()
        print("Received data:", json.dumps(data, indent=2))
        
        def get_value(key, default=None):
            value = data.get(key, default)
            return None if value == '' else value
        
        def get_date(key):
            value = data.get(key)
            return value if value and value != '' else None
        
        def get_float(key):
            value = data.get(key)
            try:
                return float(value) if value and value != '' else None
            except (ValueError, TypeError):
                return None
        
        def get_int(key):
            value = data.get(key)
            try:
                return int(value) if value and value != '' else None
            except (ValueError, TypeError):
                return None

        personnel_query = """
        INSERT INTO personnel (
            name, army_number, `rank`, trade, date_of_enrollment, date_of_birth, date_of_tos, date_of_tors,
            blood_group, religion, food_preference, drinker, company, civ_qualifications, decoration_awards,
            lacking_qualifications, willing_promotions, i_card_no, i_card_date, i_card_issued_by,
            bpet_grading, ppt_grading, bpet_date, clothing_card, pan_card_no, pan_part_ii,
            aadhar_card_no, aadhar_part_ii, joint_account_no, joint_account_bank, joint_account_ifsc,
            home_house_no, home_village, home_phone, home_to, home_po, home_ps, home_teh,
            home_nrs, home_nmh, home_district, home_state, border_area, distance_from_ib,
            height, weight, chest, identification_marks, court_cases, loan, total_leaves_encashed,
            participation_activities, present_family_location, prior_station, prior_station_date,
            worked_it, worked_unit_tenure, med_cat, last_recat_bd_date, last_recat_bd_at,
            next_recat_due, medical_problem, restrictions, computer_knowledge, it_literature,
            kin_name, kin_relation, kin_marriage_date, kin_account_no, kin_bank, kin_ifsc,
            kin_part_ii, vehicle_reg_no, vehicle_model, vehicle_purchase_date, vehicle_agif,
            driving_license_no, license_issue_date, license_expiry_date, disability_child,
            marital_discord, counselling, folder_prepared_on, folder_checked_by, bring_family,
            domestic_issues, other_requests, family_medical_issues, quality_points, strengths,
            weaknesses, detailed_course
        ) VALUES (
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
        )
        """
        
        personnel_values = (
            get_value('name'),
            get_value('armyNumber'),
            get_value('rank'),
            get_value('trade'),
            get_date('dateOfEnrollment'),
            get_date('dateOfBirth'),
            get_date('dateOfTOS'),
            get_date('dateOfTORS'),
            get_value('bloodGroup'),
            get_value('religion'),
            get_value('foodPreference'),
            get_value('drinker'),
            get_value('company'),
            get_value('civQualifications'),
            get_value('decorationAwards'),
            get_value('lackingQualifications'),
            get_value('willingPromotions'),
            get_value('iCardNo'),
            get_date('iCardDate'),
            get_value('iCardIssuedBy'),
            get_value('bpetGrading'),
            get_value('pptGrading'),
            get_date('bpetDate'),
            get_value('clothingCard'),
            get_value('panCardNo'),
            get_value('panPartII'),
            get_value('aadharCardNo'),
            get_value('aadharPartII'),
            get_value('jointAccountNo'),
            get_value('jointAccountBank'),
            get_value('jointAccountIFSC'),
            get_value('homeHouseNo'),
            get_value('homeVillage'),
            get_value('homePhone'),
            get_value('homeTO'),
            get_value('homePO'),
            get_value('homePS'),
            get_value('homeTeh'),
            get_value('homeNRS'),
            get_value('homeNMH'),
            get_value('homeDistrict'),
            get_value('homeState'),
            get_value('borderArea'),
            get_float('distanceFromIB'),
            get_float('height'),
            get_float('weight'),
            get_float('chest'),
            get_value('identificationMarks'),
            get_value('courtCases'),
            get_value('loan'),
            get_int('totalLeavesEncashed'),
            get_value('participationActivities'),
            get_value('presentFamilyLocation'),
            get_value('priorStation'),
            get_date('priorStationDate'),
            get_value('workedIT'),
            get_value('workedUnitTenure'),
            get_value('medCat'),
            get_date('lastRecatBDDate'),
            get_value('lastRecatBDAt'),
            get_date('nextRecatDue'),
            get_value('medicalProblem'),
            get_value('restrictions'),
            get_value('computerKnowledge'),
            get_value('itLiterature'),
            get_value('kinName'),
            get_value('kinRelation'),
            get_date('kinMarriageDate'),
            get_value('kinAccountNo'),
            get_value('kinBank'),
            get_value('kinIFSC'),
            get_value('kinPartII'),
            get_value('vehicleRegNo'),
            get_value('vehicleModel'),
            get_date('vehiclePurchaseDate'),
            get_value('vehicleAGIF'),
            get_value('drivingLicenseNo'),
            get_date('licenseIssueDate'),
            get_date('licenseExpiryDate'),
            get_value('disabilityChild'),
            get_value('maritalDiscord'),
            get_value('counselling'),
            get_date('folderPreparedOn'),
            get_value('folderCheckedBy'),
            get_value('bringFamily'),
            get_value('domesticIssues'),
            get_value('otherRequests'),
            get_value('familyMedicalIssues'),
            get_value('qualityPoints'),
            get_value('strengths'),
            get_value('weaknesses'),
            get_value('detailedCourse')
        )

        cursor.execute(personnel_query, personnel_values)
        personnel_id = cursor.lastrowid
        army_number = data.get('armyNumber', '')

        insert_dynamic_data(cursor, personnel_id, army_number, data)

        connection.commit()
        return jsonify({'success': True, 'personnel_id': personnel_id}), 201

    except Error as e:
        connection.rollback()
        print(f"Database error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'message': str(e)}), 500
    except Exception as e:
        connection.rollback()
        print(f"General error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'message': str(e)}), 500
    finally:
        cursor.close()
        connection.close()

def insert_dynamic_data(cursor, personnel_id, army_number, data):
    for idx, course in enumerate(data.get('courses', []), 1):
        if any(course.values()):
            cursor.execute("""
                INSERT INTO courses (personnel_id, army_number, sr_no, course, from_date, to_date, institute, grading, remarks)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                personnel_id, army_number, idx,
                course.get('course', ''),
                course.get('courseFrom', None),
                course.get('courseTo', None),
                course.get('courseInstitute', ''),
                course.get('courseGrading', ''),
                course.get('courseRemarks', '')
            ))

    for idx, unit in enumerate(data.get('units', []), 1):
        if any(unit.values()):
            cursor.execute("""
                INSERT INTO units_served (personnel_id, army_number, sr_no, unit, from_date, to_date, duty_performed)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (
                personnel_id, army_number, idx,
                unit.get('unit', ''),
                unit.get('unitFrom', None),
                unit.get('unitTo', None),
                unit.get('unitDuty', '')
            ))

    for idx, loan in enumerate(data.get('loans', []), 1):
        if any(loan.values()):
            cursor.execute("""
                INSERT INTO loans (personnel_id, army_number, sr_no, loan_type, total_amount, bank_details, emi_per_month, pending, remarks)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                personnel_id, army_number, idx,
                loan.get('loanType', ''),
                float(loan.get('loanAmount', 0)) if loan.get('loanAmount') else None,
                loan.get('loanBank', ''),
                float(loan.get('loanEMI', 0)) if loan.get('loanEMI') else None,
                float(loan.get('loanPending', 0)) if loan.get('loanPending') else None,
                loan.get('loanRemarks', '')
            ))

    for idx, punishment in enumerate(data.get('punishments', []), 1):
        if any(punishment.values()):
            cursor.execute("""
                INSERT INTO punishments (personnel_id, army_number, sr_no, punishment_date, punishment, aa_sec, remarks)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (
                personnel_id, army_number, idx,
                punishment.get('punishmentDate', None),
                punishment.get('punishment', ''),
                punishment.get('punishmentAASec', ''),
                punishment.get('punishmentRemarks', '')
            ))

    for idx, detailed in enumerate(data.get('detailedCourses', []), 1):
        if any(detailed.values()):
            cursor.execute("""
                INSERT INTO detailed_courses (personnel_id, army_number, sr_no, course_name, from_date, to_date, remarks)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (
                personnel_id, army_number, idx,
                detailed.get('detailedCourseName', ''),
                detailed.get('detailedCourseFrom', None),
                detailed.get('detailedCourseTo', None),
                detailed.get('detailedCourseRemarks', '')
            ))

    for idx, leave in enumerate(data.get('leaves', []), 1):
        if any(leave.values()):
            cursor.execute("""
                INSERT INTO leave_details (personnel_id, army_number, sr_no, year, al_days, cl_days, aal_days, total_days, remarks)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                personnel_id, army_number, idx,
                leave.get('leaveYear', ''),
                int(leave.get('leaveAL', 0)) if leave.get('leaveAL') else None,
                int(leave.get('leaveCL', 0)) if leave.get('leaveCL') else None,
                int(leave.get('leaveAAL', 0)) if leave.get('leaveAAL') else None,
                int(leave.get('leaveTotal', 0)) if leave.get('leaveTotal') else None,
                leave.get('leaveRemarks', '')
            ))

    for idx, family in enumerate(data.get('family', []), 1):
        if any(family.values()):
            cursor.execute("""
                INSERT INTO family_members (personnel_id, army_number, relation, name, date_of_birth, uid_no, part_ii_order)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (
                personnel_id, army_number,
                family.get('familyRelation', ''),
                family.get('familyName', ''),
                family.get('familyDOB', None),
                family.get('familyUID', ''),
                family.get('familyPartII', '')
            ))

    for idx, child in enumerate(data.get('children', []), 1):
        if any(child.values()):
            cursor.execute("""
                INSERT INTO children (personnel_id, army_number, sr_no, name, date_of_birth, class, part_ii_order, uid_no)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                personnel_id, army_number, idx,
                child.get('childName', ''),
                child.get('childDOB', None),
                child.get('childClass', ''),
                child.get('childPartII', ''),
                child.get('childUID', '')
            ))

    for idx, mobile in enumerate(data.get('mobiles', []), 1):
        if any(mobile.values()):
            cursor.execute("""
                INSERT INTO mobile_phones (personnel_id, army_number, sr_no, type, number, service_provider, remarks)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (
                personnel_id, army_number, idx,
                mobile.get('mobileType', ''),
                mobile.get('mobileNumber', ''),
                mobile.get('mobileProvider', ''),
                mobile.get('mobileRemarks', '')
            ))

    for idx, discord in enumerate(data.get('discordCases', []), 1):
        if any(discord.values()):
            cursor.execute("""
                INSERT INTO marital_discord_cases (personnel_id, army_number, sr_no, case_no, amount_to_pay, sanction_letter_no)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (
                personnel_id, army_number, idx,
                discord.get('discordCaseNo', ''),
                float(discord.get('discordAmount', 0)) if discord.get('discordAmount') else None,
                discord.get('discordSanction', '')
            ))

@app.route('/api/test', methods=['GET'])
def test_connection():
    connection = get_db_connection()
    if connection:
        connection.close()
        return jsonify({'success': True, 'message': 'Database connected'})
    return jsonify({'success': False, 'message': 'Connection failed'})


# API endpoint to get all personnel data
@app.route('/api/all-personnel')
def api_all_personnel():
    connection = get_db_connection()
    if not connection:
        return jsonify({'success': False, 'message': 'Database connection failed'}), 500
    
    cursor = connection.cursor(dictionary=True)
    
    try:
        # Get list of all personnel
        cursor.execute("""
            SELECT id, name, army_number, `rank`, trade, date_of_enrollment, med_cat, company
            FROM personnel 
            ORDER BY company, name
        """)
        all_personnel = cursor.fetchall()
        
        # Convert date objects to strings for JSON serialization
        for person in all_personnel:
            if person['date_of_enrollment']:
                person['date_of_enrollment'] = person['date_of_enrollment'].strftime('%Y-%m-%d')
            # Ensure med_cat has a value
            if person['med_cat'] is None:
                person['med_cat'] = 'No'
        
        return jsonify({
            'success': True,
            'personnel': all_personnel
        })
    
    except Error as e:
        print(f"Database error: {e}")
        return jsonify({'success': False, 'message': str(e)}), 500
    finally:
        cursor.close()
        connection.close()

if __name__ == '__main__':
    app.run(debug=True, port=3500)