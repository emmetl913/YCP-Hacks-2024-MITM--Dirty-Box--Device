from flask import Flask, render_template, request, send_from_directory, redirect, url_for, session, flash
from flask_httpauth import HTTPBasicAuth
from datetime import timedelta
import os

from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import redirect

app = Flask(__name__)
auth = HTTPBasicAuth()
app.secret_key = os.urandom(24)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

app.permanent_session_lifetime = timedelta(minutes=10)

USERNAME = "admin"
PASSWORD = "password123"


@app.route('/')
def index():
    if 'logged_in' in session:
        return render_template('index.html')
    else:
        return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username == USERNAME and password == PASSWORD:
            session.permanent = True
            session['logged_in'] = True
            return redirect(url_for('index'))
        else:
            flash('Stop trying to log into our website dude, your not supposed to be here')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You have been logged out successfully.')
    return redirect(url_for('login'))


@app.route('/submit', methods=['POST'])
def submit():
    text = request.form['text_field']
    return f"Received text: {text}"

@app.route('/file_type', methods=['POST'])
def set_filetype():
    text = request.form['file_type_selector']
    text = validate_filetype(text)
    if not text:
        text = '.txt'
    print(text)
    return redirect(url_for('index'))

@app.route('/file_number', methods=['POST'])
def set_filenum():
    text = request.form['file_number_selector']
    text = int(text)
    print("New Desired Files: ", text)
    return redirect( url_for('index'))

def validate_filetype(text):
    valid_extensions = {
        '.txt', '.pdf', '.doc', '.docx', '.xls', '.xlsx', '.png', '.jpg', '.jpeg', '.gif',
        '.bmp', '.csv', '.zip', '.tar', '.gz', '.mp3', '.mp4', '.avi', '.mkv', '.html',
        '.css', '.js', '.json', '.xml', '.py', '.java', '.c', '.cpp', '.rb', '.go', '.php'
    }

    text = text.lower()
    if not text.startswith('.'):
        text = f'.{text}'
    return text in valid_extensions


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file was part of this request"
    file = request.files['file']
    if file.filename == '':
        return "Error parsing filename"
    if file:
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
        return redirect(url_for('uploaded_file', filename=file.filename))

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
