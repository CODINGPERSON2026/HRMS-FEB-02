from imports import *

accounts_bp = Blueprint('account',__name__,url_prefix='/account')

@accounts_bp.route('/')
def accounts():
    return render_template('account_management/account.html')