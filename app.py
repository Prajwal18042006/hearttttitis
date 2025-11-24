from flask import Flask, request, render_template, session, redirect, url_for, flash
import numpy as np
import pandas as pd
import os
import json
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps

from src.pipeline.predict_pipeline import CustomData, PredictPipeline

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production-12345')

# User storage file
USERS_FILE = 'users.json'

def load_users():
    """Load users from JSON file"""
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_users(users):
    """Save users to JSON file"""
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f, indent=2)

def is_logged_in():
    """Check if user is logged in"""
    return 'user_id' in session

def login_required(f):
    """Decorator to require login for certain routes"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not is_logged_in():
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


# ==========================
# MAIN WEBSITE PAGES ROUTES
# ==========================

@app.route("/")
def home():
    return render_template("index.html", active_page="home", logged_in=is_logged_in(), username=session.get('username'))


@app.route("/what-is-heart-disease")
def what_is_heart_disease():
    return render_template("what-is-heart-disease.html", active_page="what-is-heart-disease", logged_in=is_logged_in(), username=session.get('username'))


@app.route("/symptoms-causes")
def symptoms_causes():
    return render_template("symptoms-causes.html", active_page="symptoms-causes", logged_in=is_logged_in(), username=session.get('username'))


@app.route("/diagnosis-tests")
def diagnosis_tests():
    return render_template("diagnosis-tests.html", active_page="diagnosis-tests", logged_in=is_logged_in(), username=session.get('username'))


@app.route("/treatment-management")
def treatment_management():
    return render_template("treatment-management.html", active_page="treatment-management", logged_in=is_logged_in(), username=session.get('username'))


@app.route("/prevention")
def prevention():
    return render_template("prevention.html", active_page="prevention", logged_in=is_logged_in(), username=session.get('username'))


@app.route("/when-to-see-doctor")
def when_to_see_doctor():
    return render_template("when-to-see-doctor.html", active_page="when-to-see-doctor", logged_in=is_logged_in(), username=session.get('username'))


@app.route("/outlook-prognosis")
def outlook_prognosis():
    return render_template("outlook-prognosis.html", active_page="outlook-prognosis", logged_in=is_logged_in(), username=session.get('username'))


@app.route("/contact")
def contact():
    return render_template("contact.html", active_page="contact", logged_in=is_logged_in(), username=session.get('username'))



# ==========================
# HEART DISEASE PREDICT FORM
# ==========================

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = CustomData(
            age=float(request.form['age']),
            sex=float(request.form['sex']),
            cp=float(request.form['cp']),
            trestbps=float(request.form['trestbps']),
            chol=float(request.form['chol']),
            fbs=float(request.form['fbs']),
            restecg=float(request.form['restecg']),
            thalach=float(request.form['thalach']),
            exang=float(request.form['exang']),
            oldpeak=float(request.form['oldpeak']),
            slope=float(request.form['slope']),
            ca=float(request.form['ca']),
            thal=float(request.form['thal'])
        )

        final_df = data.get_data_as_dataframe()

        pipeline = PredictPipeline()
        prediction = pipeline.predict(final_df)[0]

        result = "Heart Disease Yes" if prediction == 1 else "Heart Disease No"

        return render_template("index.html", active_page="home", prediction_text=result, logged_in=is_logged_in(), username=session.get('username'))

    except Exception as e:
        return str(e)



# ==========================
# AUTHENTICATION ROUTES
# ==========================

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')

        # Validation
        if not username or not email or not password:
            flash('All fields are required.', 'error')
            return render_template("register.html", active_page="register", logged_in=is_logged_in())

        if password != confirm_password:
            flash('Passwords do not match.', 'error')
            return render_template("register.html", active_page="register", logged_in=is_logged_in())

        if len(password) < 6:
            flash('Password must be at least 6 characters long.', 'error')
            return render_template("register.html", active_page="register", logged_in=is_logged_in())

        users = load_users()

        # Check if username already exists
        if username in users:
            flash('Username already exists. Please choose another.', 'error')
            return render_template("register.html", active_page="register", logged_in=is_logged_in())

        # Check if email already exists
        for user_data in users.values():
            if user_data.get('email') == email:
                flash('Email already registered. Please use a different email.', 'error')
                return render_template("register.html", active_page="register", logged_in=is_logged_in())

        # Create new user
        users[username] = {
            'email': email,
            'password': generate_password_hash(password)
        }
        save_users(users)

        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))

    return render_template("register.html", active_page="register", logged_in=is_logged_in())


@app.route("/login", methods=["GET", "POST"])
def login():
    if is_logged_in():
        return redirect(url_for('home'))

    if request.method == "POST":
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')

        if not username or not password:
            flash('Please enter both username and password.', 'error')
            return render_template("login.html", active_page="login", logged_in=is_logged_in())

        users = load_users()

        if username not in users:
            flash('Invalid username or password.', 'error')
            return render_template("login.html", active_page="login", logged_in=is_logged_in())

        if check_password_hash(users[username]['password'], password):
            session['user_id'] = username
            session['username'] = username
            flash(f'Welcome back, {username}!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password.', 'error')
            return render_template("login.html", active_page="login", logged_in=is_logged_in())

    return render_template("login.html", active_page="login", logged_in=is_logged_in())


@app.route("/logout")
def logout():
    if is_logged_in():
        username = session.get('username', 'User')
        session.clear()
        flash(f'You have been logged out. Goodbye, {username}!', 'info')
    return redirect(url_for('home'))


# ==========================
# RUN APP FOR RAILWAY
# ==========================

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    debug_mode = os.environ.get("FLASK_DEBUG", "False").lower() == "true"
    
    print("\n" + "="*50)
    print("Heart Disease Detection App")
    print("="*50)
    print(f"Server running on: http://0.0.0.0:{port}")
    print(f"Local access: http://127.0.0.1:{port}")
    print(f"Debug mode: {debug_mode}")
    print("="*50 + "\n")
    
    app.run(host="0.0.0.0", port=port, debug=debug_mode)
