from imports import *


inteview_bp = Blueprint('inteview_bp',__name__,url_prefix='/inteview_update')


@inteview_bp.route('/pending_interview_list')
def get_pending_kunba_interviews():
    user = require_login()
    user_company = user['company']
    print("this is adslfjs fdslfj slfjsdalfjdsfj sfjdsfj aff j")
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    user = require_login()
    print(user)

    cursor.execute('select home_state from personnel where army_number = %s',(user['army_number'],))
    result = cursor.fetchone()
    home_state = result['home_state']


    cursor.execute("""
        SELECT id, army_number, `rank`, name,home_state
        FROM personnel
        WHERE interview_status = 0 AND home_state = %s  AND company = %s
    """,(home_state,user_company))
    data = cursor.fetchall()
    print(data,"this is data coming from backend")
    cursor.close()
    return jsonify(data)


@inteview_bp.route('/update_interview_status', methods=['POST'])
def complete_kunba_interview():
    data = request.json
    personnel_id = data['id']
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE personnel
        SET interview_status = 1
        WHERE id = %s
    """, (personnel_id,))
    conn.commit()
    cursor.close()

    return jsonify({"success": True})




@inteview_bp.route('/completed_interview_list', methods=['GET'])
def completed_interview_list():
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        query = """
            SELECT
                id,
                army_number,
                `rank`,
                name,
                home_state,
                updated_at AS completed_on
            FROM personnel
            WHERE interview_status = 1
            ORDER BY updated_at DESC
        """
        cursor.execute(query)
        rows = cursor.fetchall()

        return jsonify(rows)

    except Exception as e:
        print("Completed Interview List Error:", e)
        return jsonify([])

    finally:
        if cursor:
            cursor.close()
