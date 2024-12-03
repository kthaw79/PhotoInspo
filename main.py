from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        # Here, add your logic to verify the email and password
        return 'Login Successful'  # Redirect or respond based on your verification
    return render_template('login.html')

#Handling User Registration
from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for session management and flash messages

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row  # This enables column access by name: row['column_name']
    return conn

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute("INSERT INTO users (email, password) VALUES (?, ?)", (email, password))
        db.commit()
        db.close()
        return redirect(url_for('login'))
    return render_template('register.html')

#Update the login route to check user credentials against the database
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        db = get_db_connection()
        user = db.execute('SELECT * FROM users WHERE email = ? AND password = ?', (email, password)).fetchone()
        db.close()
        if user:
            return 'Login Successful'
        else:
            flash('Invalid credentials')
    return render_template('login.html')