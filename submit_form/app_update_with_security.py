from flask import Flask, render_template, request, session
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
import yaml
import os
app = Flask(__name__)

db = yaml.load(open('db.yaml'))
app.config["MYSQL_HOST"] = db['mysql_host']
app.config["MYSQL_USER"]= db['mysql_user']
app.config["MYSQL_PASSWORD"]= db['mysql_password']
app.config["MYSQL_DB"] = db['mysql_db']
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
app.config['SECRET_KEY'] = os.urandom(24)
mysql = MySQL(app)


@app.route('/', methods = ['GET', 'POST'])
def index():
    if request.method == "POST":
        form = request.form
        name = form['user_name']
        age  =  form['age']
        name = generate_password_hash(name)
        print("SIZE OF THE DATA",len(name))
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO employee_data(name, age) VALUES(%s, %s)", (name, age))
        mysql.connection.commit()
    return render_template('index.html')

@app.route('/employee', methods = ["GET", "POST"])
def employee():
    cur = mysql.connection.cursor()
    result = cur.execute('SELECT * FROM employee_data')

    if result >0:
        data = cur.fetchall()

    if request.method == "POST":
        encrypted_name = request.form['pwd']
        k = 0
        str1 = 'You already have an account'
        str2 = 'You Dont have account. Please create account'
        k = [ 0 if check_password_hash(data[i]['name'], encrypted_name)==True else 1 for i in range(len(data))]
        k = sum(k)
        if (k == len(data)):
            return str2
        else:
            return str1

    return render_template('employee.html', employees = data )

if __name__ == '__main__':
    app.run(debug=True)
