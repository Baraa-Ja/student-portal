# app.py
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from database import db
from Models import Student, Course, Enrollment
from ajax.enroll import ajax
from api import api
import os



app = Flask(__name__)

app.register_blueprint(ajax)
app.register_blueprint(api)

app.secret_key = 'your_secret_key_here'
app.config['SQLALCHEMY_DATABASE_URI'] = (
    "mssql+pyodbc://sa:sa123456@localhost/student_portal"
    "?driver=ODBC+Driver+17+for+SQL+Server"
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

if not os.path.exists('db.sqlite3'):
    with app.app_context():
        db.create_all()

# ---------------------- ROUTES ---------------------- #

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        if Student.query.filter_by(email=email).first():
            return 'Email already exists.'

        hashed_pw = generate_password_hash(password)
        new_user = Student(name=name, email=email, password_hash=hashed_pw)
        db.session.add(new_user)
        db.session.commit()

        return redirect('/login')

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = Student.query.filter_by(email=email).first()

        if user and check_password_hash(user.password_hash, password):
            session['id'] = user.id
            return redirect('/dashboard')
        return 'Invalid credentials'

    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'id' not in session:
        return redirect('/login')
    student = Student.query.get(session['id'])
    enrolled = db.session.query(Course).join(Enrollment).filter(Enrollment.student_id == student.id).all()
    return render_template('dashboard.html', student=student, enrolled=enrolled)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/courses')
def courses():
    return render_template('courses.html')

@app.route('/api/courses')
def api_courses():
    courses = Course.query.all()
    return jsonify([{'id': c.id, 'title': c.title, 'description': c.description} for c in courses])

@app.route('/ajax/enroll', methods=['POST'])
def ajax_enroll():
    if 'id' not in session:
        return jsonify({'success': False, 'message': 'Not logged in'})

    data = request.get_json()
    course_id = data.get('course_id')
    exists = Enrollment.query.filter_by(student_id=session['id'], course_id=course_id).first()
    if exists:
        return jsonify({'success': False, 'message': 'Already enrolled'})

    enrollment = Enrollment(student_id=session['id'], course_id=course_id)
    db.session.add(enrollment)
    db.session.commit()
    return jsonify({'success': True})


@app.route('/admin')
def admin_panel():
    if 'id' not in session:
        return redirect('/login')

    students = Student.query.all()
    courses = Course.query.all()

    return render_template('admin.html', students=students, courses=courses)


@app.route('/profile')
def profile():
    id = session.get('id')
    if not id:
        return redirect(url_for('login'))

    user = Student.query.get(id)
    enrollments = Enrollment.query.filter_by(student_id=id).all()

    courses = [e.course for e in enrollments]

    return render_template('profile.html', user=user, courses=courses)

@app.route('/profile/edit', methods=['GET', 'POST'])
def edit_profile():
    id = session.get('id')
    user = Student.query.get(id)

    if request.method == 'POST':
        user.username = request.form['username']
        user.email = request.form['email']
        db.session.commit()
        return redirect(url_for('profile'))

    return render_template('edit_profile.html', user=user)


from flask_login import LoginManager, login_required, current_user

login_manager = LoginManager()
login_manager.init_app(app)

# User loader callback for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return Student.query.get(int(user_id))


@app.route('/api/user/enrollments')
@login_required
def user_enrollments_api():
    enrollments = Enrollment.query.filter_by(student_id=current_user.id).all()
    courses = [e.course for e in enrollments]
    return jsonify([{'id': c.id, 'title': c.title, 'description': c.description} for c in courses])

if __name__ == '__main__':
    app.run(debug=True, port=5001)

