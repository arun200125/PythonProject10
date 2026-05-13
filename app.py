import os
import cv2
import threading
import time
import numpy as np
from flask import Flask, render_template, request, redirect, url_for, session, jsonify, Response
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from deepface import DeepFace

# ------------------ Flask Setup ------------------
app = Flask(__name__)
app.secret_key = "supersecretkey"

# ------------------ Database Config ------------------
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///wellness.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

# ------------------ Database Model ------------------
class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    emp_id = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    contact = db.Column(db.String(15))
    age = db.Column(db.Integer)
    height = db.Column(db.Float)
    weight = db.Column(db.Float)
    password = db.Column(db.String(200), nullable=False)

    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

with app.app_context():
    db.create_all()

# ------------------ Camera & Emotion Setup ------------------
camera = cv2.VideoCapture(0)
lock = threading.Lock()
running = False
start_time = None
current_emotions = {}
session_data = []

def analyze_frame():
    """Continuously analyze camera frames for emotions"""
    global running, current_emotions, session_data
    while running:
        with lock:
            ret, frame = camera.read()
        if not ret:
            continue
        try:
            result = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)
            emotions = result[0]['emotion'] if isinstance(result, list) else result['emotion']
            current_emotions = emotions
            session_data.append(emotions)
        except Exception:
            continue
        time.sleep(2)

def generate_frames():
    """Send video frames to frontend"""
    global running
    while True:
        if running:
            with lock:
                success, frame = camera.read()
            if not success:
                break
            frame = cv2.flip(frame, 1)
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        else:
            time.sleep(0.1)

# ------------------ Routes ------------------

@app.route('/')
def home():
    return redirect(url_for('login'))

# ----------- Register -----------
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        emp_id = request.form['emp_id']
        name = request.form['name']
        email = request.form['email']
        contact = request.form['contact']
        age = request.form['age']
        height = request.form['height']
        weight = request.form['weight']
        password = request.form['password']
        confirm = request.form['confirm']

        if password != confirm:
            return render_template('register.html', message="Passwords do not match")

        if Employee.query.filter_by(email=email).first():
            return render_template('register.html', message="Email already registered")

        emp = Employee(emp_id=emp_id, name=name, email=email,
                       contact=contact, age=age, height=height, weight=weight)
        emp.set_password(password)
        db.session.add(emp)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html')

# ----------- Login -----------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        emp = Employee.query.filter_by(email=email).first()
        if emp and emp.check_password(password):
            session['employee'] = emp.id
            session['employee_name'] = emp.name
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', message="Invalid credentials")
    return render_template('login.html')

# ----------- Forgot Password -----------
@app.route('/forgot', methods=['GET', 'POST'])
def forgot():
    if request.method == 'POST':
        email = request.form['email']
        emp = Employee.query.filter_by(email=email).first()
        if emp:
            return render_template('forgot.html', message=f"Password reset link sent to {email} (mock)")
        else:
            return render_template('forgot.html', message="Email not found")
    return render_template('forgot.html')

# ----------- Dashboard -----------
@app.route('/dashboard')
def dashboard():
    if 'employee' not in session:
        return redirect(url_for('login'))
    emp = Employee.query.get(session['employee'])
    return render_template('dashboard.html', emp=emp)

# ----------- Start / Stop / Analyze -----------
@app.route('/start')
def start_camera():
    global running, start_time
    if not running:
        running = True
        start_time = time.time()
        threading.Thread(target=analyze_frame, daemon=True).start()
    return jsonify({'status': 'started'})

@app.route('/stop')
def stop_camera():
    global running
    running = False
    return jsonify({'status': 'stopped'})

@app.route('/video_feed')
def video_feed():
    """Return MJPEG stream to frontend"""
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/analyze')
def analyze():
    """Return live emotion data"""
    return jsonify(current_emotions)

@app.route('/report')
def report():
    """Return average emotion and employee info"""
    if not session_data:
        return jsonify({'message': 'No data recorded yet'})
    avg = {k: np.mean([d[k] for d in session_data]) for k in session_data[0]}
    duration = int(time.time() - start_time) if start_time else 0
    emp = Employee.query.get(session['employee'])
    return jsonify({
        'employee': {
            'ID': emp.emp_id,
            'Name': emp.name,
            'Email': emp.email,
            'Contact': emp.contact,
            'Age': emp.age,
            'Height': emp.height,
            'Weight': emp.weight
        },
        'average': avg,
        'duration': duration
    })

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# ------------------ Run ------------------
if __name__ == '__main__':
    app.run(debug=True)
