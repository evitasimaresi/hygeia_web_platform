from functools import wraps
from flask import session, redirect, url_for, request
from flask import flash, render_template, url_for, redirect, request, session
from app import app, db
from app.models import Patient, Doctor
from werkzeug.security import check_password_hash, generate_password_hash

from config import Config
from bardapi import Bard
import requests
import os
from datetime import datetime
import pytz

def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/3.0.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("name") is None:
            return redirect(url_for('index', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

def handle_user(form, action, template):
    user = None
    if form.validate():
        user_type = form.user_type.data
        username = form.username.data
        password = form.password.data
        confirm_password = form.confirm_password.data
        email = form.email.data
        validate = form.validate_email(email)
        if form.is_register_form() and form.validate_email(email):
            if not username:
                return apology("Missing username")
            if user_type != 'doctor' and user_type != 'patient':
                return apology("Missing user type")
                flash('Wrong user type') #error handling
            if confirm_password == password:
                hash = generate_password_hash(password)
                if user_type == 'patient':
                    user = Patient.register(username,email, hash)
                elif user_type == 'doctor':
                    specialty_id = form.specialty.data.id
                    user = Doctor.register(username,email, hash, specialty_id)
            else:
                return apology("Passwords do not match")
        elif form.is_register_form() and not form.validate_email(email):
            return apology("Wrong Email")
        if action == 'login':
            if user_type == 'patient':
                user = Patient.login(username)
            elif user_type == 'doctor':
                user = Doctor.login(username)
                print(user.username)
            if user and not check_password_hash(user.password, password):
                user = None 
            if request.method == "POST" and user is None:
                return apology("Wrong credentials")
            # flash('Wrong credentials---') #error handling
        if user is not None:
            session["name"] = username
            session["user_type"] = user_type.capitalize() 
            if user_type == 'patient':
                user = Patient.query.filter_by(username=username).first()
            else:
                user = Doctor.query.filter_by(username=username).first()
            session["user_id"] = user.id
            return redirect(url_for('index'))
    return render_template(template, title=action.capitalize(), form=form)

def get_doctor_by_specialty(specialty_id):
    doctors = Doctor.query.filter_by(specialty_id=specialty_id).all()
    return doctors

def convertUTC (date_time):
    return datetime.strptime(date_time, '%Y-%m-%dT%H:%M:%S%z')

def apology(message, code=400):
    """Render message as an apology to user."""

    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [
            ("-", "--"),
            (" ", "-"),
            ("_", "__"),
            ("?", "~q"),
            ("%", "~p"),
            ("#", "~h"),
            ("/", "~s"),
            ('"', "''"),
        ]:
            s = s.replace(old, new)
        return s

    return render_template("apology.html", top=code, bottom=escape(message)), code

# Bard chat
def initialize_session():
    session = requests.Session()
    session.headers = {
    "Host": Config.BARD_HOST,
    "X-Same-Domain": "1",
    "User-Agent": Config.BARD_USER_AGENT,
    "Content-Type": Config.BARD_CONTENT_TYPE,
    "Origin": Config.BARD_ORIGIN,
    "Referer": Config.BARD_REFERER,
    }
    session.cookies.set("__Secure-1PSID", Config.BARD_API_KEY)
    return session

def get_response(promt, bard):
    response = bard.get_answer(promt)["content"]
    return response

def sugest_doctor(symptoms):
    session = initialize_session()
    bard = Bard(token=Config.BARD_API_KEY, session=session, timeout=30)

    promt = f"""You are a medical advisor. You have knowledge about types of doctors, health symptoms, and other relevant information. Always answer with the goal of suggest a relevant medical specialist related to the symptoms described. The answer should be no more than 100 words.
    Respond to the following:

    "{symptoms}" """

    print(f'\U0001F4E3 You: {promt}')
    print('-'*100, "\n")

    response = get_response(promt, bard)
    print(f'\U0001F4E5 Bot: {response}')
    print('-'*100, "\n")

    response_doctor = get_response("Return the type of doctor suggested, no more words. If more than one return them separated by coma.", bard)
    print(f'\U0001F4E5 Bot: {response_doctor}')

    response_tips = get_response("Give some tips for preparing before the appointment. The answer should be no more than 100 words.", bard)
    print(f'\U0001F4E5 Bot: {response_tips}')
