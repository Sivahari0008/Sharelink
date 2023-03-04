# Store this code in 'app.py' file

from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
from flask_socketio import SocketIO, emit
from plyer import notification
import json


app = Flask(__name__)


app.secret_key = 'your secret key'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'userdatabase'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)
socketio = SocketIO(app)




@app.route('/')
def home():
	return render_template('home.html')

@app.route('/login', methods =['GET', 'POST'])
def login():
	msg = ''
	if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
		username = request.form['username']
		password = request.form['password']
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM accounts WHERE username = % s AND password = % s', (username, password, ))
		account = cursor.fetchone()
		if account:
			session['loggedin'] = True
			session['id'] = account['id']
			session['username'] = account['username']
			msg = 'Logged in successfully !'
			return render_template('index.html', msg = msg)
		else:
			msg = 'Incorrect username / password !'
	return render_template('login.html', msg = msg)



@app.route('/logout')
def logout():
	session.pop('loggedin', None)
	session.pop('id', None)
	session.pop('username', None)
	return redirect(url_for('login'))

@app.route('/register', methods =['GET', 'POST'])
def register():
	msg = ''
	if request.method == 'POST' and 'username' in request.form and 'mobile' in request.form and 'email' in request.form and 'password' in request.form :
		username = request.form['username']
		mobile = request.form['mobile']
		email = request.form['email']
		password = request.form['password']
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM accounts WHERE username = % s', (username, ))
		account = cursor.fetchone()
		if account:
			msg = 'Account already exists !'
		elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
			msg = 'Invalid email address !'
		elif not re.match(r'[A-Za-z0-9]+', username):
			msg = 'Username must contain only characters and numbers !'
		elif not username or not password or not mobile or not email:
			msg = 'Please fill out the form !'
		else:
			cursor.execute('INSERT INTO accounts VALUES (NULL, % s, % s, % s, %s)', (username,mobile,email,password, ))
			mysql.connection.commit()
			msg = 'You have successfully registered !'
	elif request.method == 'POST':
		msg = 'Please fill out the form !'
	return render_template('register.html', msg = msg)

@app.route("/ajaxlivesearch",methods=["POST","GET"])
def ajaxlivesearch():
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if request.method == 'POST':
        search_word = request.form['query']
        print(search_word)
        if search_word == '':
            query = "SELECT * from accounts ORDER BY id"
            cur.execute(query)
            employee = cur.fetchall()
        else:    
            query = "SELECT * from accounts WHERE username LIKE '%{}%' ".format(search_word)
            cur.execute(query)
            numrows = int(cur.rowcount)
            users = cur.fetchall()
            print(numrows)
    return jsonify({'htmlresponse': render_template('response.html', users=users, numrows=numrows)})

@app.route('/camera', methods=['GET', 'POST'])
def camera():
    return render_template('camera.html')

@app.route('/iphone', methods=['GET', 'POST'])
def iphone():
    return render_template('iphone.html')

@app.route('/tshirt', methods=['GET', 'POST'])

def tshirt():
    return render_template('tshirt.html')

@app.route('/phone', methods=['GET', 'POST'])

def phone():
    return render_template('phone.html')

@app.route('/tops', methods=['GET', 'POST'])
def tops():
    return render_template('tops.html')
@app.route('/laptop', methods=['GET', 'POST'])
def laptop():
    return render_template('laptop.html')
@app.route('/shoe', methods=['GET', 'POST'])
def shoe():
    return render_template('shoe.html')
@app.route('/heels', methods=['GET', 'POST'])
def heels():
    return render_template('heels.html')

@app.route('/message', methods=['GET', 'POST'])
def message():
    return render_template('message.html')

@app.route('/send_message', methods=['POST'])
def send_message():
    message = request.form['message']
    recipient = request.form['recipient']
    sender = request.form['sender']
    # Insert the message into the MySQL database
    cursor = mysql.connection.cursor()
    sql = "INSERT INTO messages (message, recipient, sender) VALUES (%s, %s, %s)"
    val = (message, recipient, sender)
    cursor.execute(sql, val)
    mysql.connection.commit()
    # Send the message to the recipient's browser using SocketIO
    socketio.emit('new_message', {'message': message, 'sender': sender}, room=recipient)
    return render_template('index.html')

@app.route('/message/')
def display_messages():
    # Query the database for all messages between the sender and recipient
    user_id = session.get("username")
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM messages WHERE recipient = %s order by ID DESC limit 1", [user_id])
    messages = cur.fetchall()
    sender = messages[0]['sender']
    message = messages[0]['message']
        # Render the template with the list of messages
    return render_template('message.html', sender=sender,message=message)

if __name__ == '__main__':
    app.run(debug = True)



