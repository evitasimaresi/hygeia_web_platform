from flask import (
    flash,
    render_template,
    url_for,
    redirect,
    request,
    session,
    jsonify,
    make_response,
)
from app import app, db
from datetime import datetime
import pytz
from app.forms import UserForm, Symptoms, Appointment
from app.models import Patient, Doctor, Case, Specialty, Appointments

from .helpers import (
    login_required,
    handle_user,
    sugest_doctor,
    get_doctor_by_specialty,
    convertUTC,
    apology
)


@app.route("/")
def index():
    """Show upcoming appointments"""
    if not session.get("name"):
        return redirect(url_for("authuser"))
    session_data = dict(session)
    # return apology("Good", 321)
    return render_template("index.html", user=session["name"], session_data=session_data)


@app.route("/authuser", methods=["GET"])
def authuser():
    """Authenticate user"""
    return render_template("authuser.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register"""
    form = UserForm()
    if form.validate_on_submit():
        return handle_user(form, "register", "register.html")  # <--------------
    return render_template("register.html", title="Register", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log in"""
    form = UserForm()
    return handle_user(form, "login", "login.html")  # <--------------


@app.route("/logout")
@login_required
def logout():
    """Logout"""
    session.clear()
    # print(session['name'])
    flash("You've been logged out")
    return redirect(url_for("index"))


@app.route("/chat", methods=["GET", "POST"])
@login_required
def chat():
    """Chat"""
    form = Symptoms()
    if form.validate_on_submit():
        description = request.form.get("description")
        feelings = request.form.get("feelings")
        location = request.form.get("location")
        severity = request.form.get("severity")
        handled = False
        patient_id = session["user_id"]
        if not description or not feelings or not location:
            return apology("Fill in the form")
        Case.register(description, feelings, location, severity, handled, patient_id)
        return redirect(url_for("appointments"))
    return render_template("chat.html", user=session["name"], form=form)


@app.route("/appointments", methods=["GET", "POST"])
@login_required
def appointments():
    """Appointments"""
    form = Appointment()
    specialties = Specialty.query.all()
    patient_id = session["user_id"]
    cases = Case.query.filter_by(patient_id=patient_id, handled=False).all()
    doctors = []
    if "appointment" not in session:
        session["appointment"] = {}
    appointment = session["appointment"]
    if request.method == "POST":
        data = request.get_json()
        action = data.get("action")
        if action == "associate":
            appointment["case_id"] = data.get("case_id")
            appointment["doctor_id"] = data.get("doctor_id")
            return jsonify({"message": "Case and doctor associated successfully"}), 200
        elif action == "book":
            start = data.get("start_time")
            date_time = convertUTC(start)
            Appointments.register(
                date_time, appointment["case_id"], appointment["doctor_id"]
            )
            case = Case.query.get(appointment["case_id"])
            case.handled = True
            db.session.commit()
            session["appointment"] = {}
            return jsonify({"message": "Appointment booked successfully"}), 200
    return render_template(
        "appointments.html",
        user=session["name"],
        cases=cases,
        form=form,
        specialties=specialties,
        doctors=doctors,
    )


@app.route("/history", methods=["GET"])
@login_required
def history():
    user_id = session.get("user_id")
    if session["user_type"] == "Patient":
        all_cases = Case.query.filter(Case.patient_id == user_id).all()
                            
    return render_template("history.html", cases=all_cases)


# make query get datime, doctor, specialty for handled cases
@app.route("/get_info_handled_cases", methods=["GET"])
def get_info_handled_cases():
    case_id = request.args.get("case_id", type=int)
    case = (
            Appointments.query.join(Case, Appointments.case_id == Case.id)
            .join(Doctor, Appointments.doctor_id == Doctor.id)
            .join(Specialty, Doctor.specialty_id == Specialty.id)
            .filter(Case.id == case_id)
            .first()
        )
    if case:
        case_info = {
            'datetime': case.datetime,
            'doctor': {
                'username': case.doctor.username,
                'specialty': case.doctor.specialty.specialty
                }
        }
        return jsonify(case_info)
    else:
        return jsonify({'error': 'Case not found'}),  404

# mamke the query to get doctors by specialty
@app.route("/get_doctor_by_specialty", methods=["GET"])
def get_doctor_by_specialty():
    specialty_id = request.args.get("specialty_id", type=int)
    doctors = Doctor.query.filter_by(specialty_id=specialty_id).all()
    return jsonify([doctor.serialize() for doctor in doctors])


# make the query for appointments for the selected doctor
@app.route("/get_appointments_by_doctor", methods=["GET"])
def get_appointments_by_doctor():
    doctor_id = request.args.get("doctor_id", type=int)
    appointments = Appointments.query.filter_by(doctor_id=doctor_id).all()
    return jsonify([appointment.serialize() for appointment in appointments])


# make the query for booked appointments in index
@app.route("/get_booked_appointments", methods=["GET"])
def get_booked_appointments():
    user_id = session.get("user_id")
    try:
        if session["user_type"] == "Patient":
            appointments = (
                Appointments.query.join(Case, Appointments.case_id == Case.id)
                .join(Doctor, Appointments.doctor_id == Doctor.id)
                .join(Patient, Case.patient_id == Patient.id)
                .filter(Case.patient_id == user_id)
                .all()
            )
        else:
            appointments = (
                Appointments.query.join(Case, Appointments.case_id == Case.id)
                .join(Doctor, Appointments.doctor_id == Doctor.id)
                .join(Patient, Case.patient_id == Patient.id)
                .filter(Appointments.doctor_id == user_id)
                .all()
            )
        final_appointments = [appointment.serialize() for appointment in appointments]
        return jsonify(final_appointments)
    except Exception as e:
        return apology("An error occurred while fetching appointments", 500)