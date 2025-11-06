from flask import Flask, render_template, request
import sqlite3
from blueprints.personal_information import personnel_info
app = Flask(__name__)

app.register_blueprint(personnel_info)

# @app.route('/')
# def baseView():
#     return render_template('baseView.html')

@app.route('/')
def dashboard():
    return render_template('dashboard.html')
    
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


if __name__ == '__main__':
    app.run(debug=True)


