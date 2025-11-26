from imports import *

task_bp = Blueprint('task',__name__,url_prefix='/task_manager')

@task_bp.route('/')
def home():
    return render_template('/task_manager/task.html')