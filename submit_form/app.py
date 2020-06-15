from flask import Flask, render_template, request
from flask_mysqldb import MySQL
import yaml
app = Flask(__name__)

db = yaml.load(open('db.yaml'))
app.config["MYSQL_HOST"] = db['mysql_host']
app.config["MYSQL_USER"]= db['mysql_user']
app.config["MYSQL_PASSWORD"]= db['mysql_password']
app.config["MYSQL_DB"] = db['mysql_db']
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)


@app.route('/', methods = ['GET', 'POST'])
def index():
    if request.method == "POST":
        name = request.form['user_name']
        age = request.form['age']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO employee_data(name, age) VALUES(%s, %s)", (name, age))
        mysql.connection.commit()
    return render_template('index.html')

@app.route('/employee')
def employee():
    cur = mysql.connection.cursor()
    result = cur.execute('SELECT * FROM employee_data')
    if result >0:
        data = cur.fetchall()
        return render_template('employee.html', employees = data )
if __name__ == '__main__':
    app.run(debug=True)
