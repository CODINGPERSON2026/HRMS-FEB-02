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
    cursor.execute("SELECT id,task_name, assigned_to, task_status FROM tasks ORDER BY id DESC")
    tasks = cursor.fetchall()
    return jsonify(tasks)


@task_bp.route("/get_task/<int:id>")
def get_task_details(id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    print(id,"this is id")
    cursor.execute("SELECT * FROM tasks WHERE id=%s", (id,))
    task = cursor.fetchone()
    print(task)
    cursor.close()
    conn.close()

    return jsonify(task)

@task_bp.route('delete_task/<int:id>',methods = ['DELETE'])
def delete_task(id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        query = 'DELETE FROM tasks where id = %s'
        cursor.execute(query,(id,))
    except Exception as e:
        print('Exception',str(e))
    return jsonify({'message': f'{id} deleted'}),200



@task_bp.route('/get_task_update/<int:task_id>')
def get_task(task_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM tasks WHERE id=%s", (task_id,))
    task = cursor.fetchone()
    print(task)
    cursor.close()
    conn.close()
    
    if task:
        # Format date as yyyy-mm-dd for input[type=date]
        task['due_date'] = task['due_date'].strftime('%Y-%m-%d') if task['due_date'] else ''
        return jsonify(task)
    else:
        return jsonify({"error": "Task not found"}), 404





# the below route is for updating the task
@task_bp.route('/update_task/<int:task_id>', methods=['POST'])
def edit_task(task_id):
    try:
        data = request.form  
        print(data,"this is data from form")

        task_name = data.get("task_name")
        description = data.get("description")
        priority = data.get("priority")
        assigned_to = data.get("assigned_to")
        due_date = data.get("due_date")

        conn = get_db_connection()
        cursor = conn.cursor()

        query = """
            UPDATE tasks
            SET task_name=%s, description=%s, priority=%s,
                assigned_to=%s, due_date=%s
            WHERE id=%s
        """

        cursor.execute(query, (task_name, description, priority, assigned_to, due_date, task_id))
        conn.commit()

        cursor.close()
        conn.close()

        return jsonify({"status": "success", "message": "Task updated successfully"}), 200

    except Exception as e:
        print("Update Task Error:", e)
        return jsonify({"status": "error", "message": "Failed to update task"}), 500