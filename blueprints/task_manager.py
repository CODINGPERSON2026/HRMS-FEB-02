from imports import *

task_bp = Blueprint('task',__name__,url_prefix='/task_manager')

@task_bp.route('/')
def home():
    return render_template('/task_manager/task.html')

@task_bp.route('/create-task', methods=['POST'])
def update_task():
    data = request.get_json()
    print(data,"this is data")
    task_name = data.get('task_name')
    description = data.get('description')
    priority = data.get('priority')
    assigned_to = data.get('assigned_to')
    due_date = data.get('due_date')
    user = require_login()
    admin = user['role']
    print(admin)

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        query = """
    INSERT INTO tasks (task_name, description, priority, assigned_to, assigned_by, due_date)
    VALUES (%s, %s, %s, %s, %s, %s)
"""

        cursor.execute(query, (
    task_name,
    description,
    priority,
    assigned_to,
    admin,
    due_date
))


        conn.commit()

        return jsonify({"status": "success", "message": "Task updated successfully"})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})



@task_bp.route("/view_task")
def view_task():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT task_name, assigned_to, task_status FROM tasks ORDER BY id DESC")
    tasks = cursor.fetchall()
    return jsonify(tasks)
