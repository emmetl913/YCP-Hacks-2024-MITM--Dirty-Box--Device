from flask import Flask, render_template, request, send_from_directory, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from datetime import timedelta
import os

from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import redirect

# Setup app and config
app = Flask(__name__)
app.secret_key = os.urandom(24)
app.permanent_session_lifetime = timedelta(minutes=10)

# Setup Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///uploads.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'uploads'
db = SQLAlchemy(app)
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)


# Secret shhhhh don't tell nobody
USERNAME = "admin"
PASSWORD = "password123"

class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(50), nullable=False)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    if 'logged_in' in session:
        image_extensions = {'jpg', 'jpeg', 'png', 'gif', 'bmp', 'webp'}
        files = File.query.filter_by(username=USERNAME).all()
        all_usernames = get_all_usernames()

        # Prepare a list of dictionaries with file info
        file_data = [
            {
                'name': file.filename,
                #'is_image': file.split('.')[-1].lower() in image_extensions
            }
            for file in files
        ]
        return render_template('index.html', files=files, usernames=all_usernames)
    else:
        return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        print("Debug username & password: ", request.form['username'], "  ", request.form['password'])
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

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory('uploads', filename, as_attachment=True)

@app.route('/files_by_user', methods=['POST'])
def files_by_user():
    if 'logged_in' not in session:
        return redirect(url_for('login'))

    selected_username = request.form.get('username')
    if selected_username:
        files = get_files_by_username(selected_username)
    else:
        files = []

    # Render the index page with the selected user's files
    all_usernames = get_all_usernames()  # Get all usernames for the dropdown
    return render_template('index.html', files=files, usernames=all_usernames, selected_user=selected_username)

def get_files_by_username(username):
    try:
        files = File.query.filter_by(username=username).all()  # Query files by username
        filenames = [file.filename for file in files]  # Extract filenames from the query result
        return filenames
    except Exception as e:
        print("Error retrieving files:", e)
        return []
def get_all_usernames():
    try:
        usernames = db.session.query(File.username).distinct().all()
        return [username[0] for username in usernames]  # Extract usernames from the query result
    except Exception as e:
        print("Error retrieving usernames:", e)
        return []

@app.route('/clear')
def clear_database():
    try:
        db.session.query(File).delete()  # Delete all rows in the File table
        db.session.commit()  # Commit the changes to the database
        print("Database cleared successfully.")
    except Exception as e:
        db.session.rollback()  # Rollback in case of error
        print("Error clearing database:", e)
    return redirect(url_for('index'))

@app.route('/file_scrape_info', methods=['POST'])
def get_scrape_info():
    type = request.form['file_type_selector']
    number = request.form['file_number_selector']
    number = int(number)
    type = validate_filetype(type)
    print(f"PI set to scrape {number} files of type {type}")
    return redirect(url_for('index'))


def validate_filetype(text):
    valid_extensions = {
        '.txt', '.pdf', '.doc', '.docx', '.xls', '.xlsx', '.png', '.jpg', '.jpeg', '.gif',
        '.bmp', '.csv', '.zip', '.tar', '.gz', '.mp3', '.mp4', '.avi', '.mkv', '.html',
        '.css', '.js', '.json', '.xml', '.py', '.java', '.c', '.cpp', '.rb', '.go', '.php'
    }

    text = text.lower()
    if not text.startswith('.'):
        text = f'.{text}'
    return text


@app.route('/upload', methods=['GET','POST'])
def upload_file():
    if 'logged_in' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        file = request.files['file']
        if file:
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            # Save file info to the database
            new_file = File(filename=filename, username=USERNAME)
            db.session.add(new_file)
            db.session.commit()

            flash('File uploaded successfully.')
            return redirect(url_for('index'))

    return render_template('upload.html')


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
