from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(35), unique = True, nullable = True)
    email = db.Column(db.String(65), unique = True, nullable = True)
    password = db.Column(db.String(200))

    @classmethod
    def register(cls, username, email, password, specialty_id):
        user = cls(username=username, email=email, password=password, specialty_id=specialty_id)
        db.session.add(user)
        db.session.commit()
        return user
    
    @classmethod
    def login(cls, username):
        user = cls.query.filter_by(username=username).first()
        # if user and user.password == password:
        #     return user
        # return None
        return user
    
class Patient(User):
        __tablename__ = 'patient'
        
        @classmethod
        def register(cls, username, email, password):
            user = cls(username=username, email=email, password=password)
            db.session.add(user)
            db.session.commit()
            return user

class Doctor(User):
    __tablename__ = 'doctor'
    specialty_id = db.Column(db.Integer, db.ForeignKey('specialty.id'))
    specialty = db.relationship('Specialty')
    
    def serialize(self):
        return {
            'id': self.id,
            'username': self.username
        }

class Specialty(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    specialty = db.Column(db.String(35), unique=True)

class Case(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(500))
    feelings = db.Column(db.String(200))
    location = db.Column(db.String(200))
    severity = db.Column(db.String(200))
    handled = db.Column(db.Boolean)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'))
    patient = db.relationship('Patient')

    @classmethod
    def register(cls, description, feelings, location, severity, handled, patient_id):
        case = cls(description=description, feelings=feelings, location=location, severity=severity, handled=handled, patient_id=patient_id)
        db.session.add(case)
        db.session.commit()
        # return case
    
    def serialize(self):
        return{
            'id': self.id,
            'description': self.description,
            'feelings': self.feelings,
            'location': self.location,
            'severity': self.severity,
            'handled': self.handled,
            'appointment':{
                'datetime':  self.appointments.datetime.isoformat(),
                'doctor': {
                    'username': self.appointments.doctor.username,
                    'specialty': self.appointments.doctor.specialty.specialty,
                }
            }
        }
     

class Appointments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    datetime = db.Column(db.DateTime)
    case_id = db.Column(db.Integer, db.ForeignKey('case.id'), unique=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'))
    case = db.relationship('Case')
    doctor = db.relationship('Doctor')

    def serialize(self):
        return {
            'id': self.id,
            'patient_name': self.case.patient.username,
            'datetime': self.datetime.isoformat(),
            'case_id': self.case_id,
            'doctor_id': self.doctor_id,
            'doctor_name' : self.doctor.username,
            'case': {
                'id': self.case.id,
                'description': self.case.description,
                'feelings': self.case.feelings,
                'location': self.case.location,
                'severity': self.case.severity,
                'handled': self.case.handled
            }
        }
    
    @classmethod
    def register(cls, datetime, case_id, doctor_id):
        case = cls(datetime=datetime, case_id=case_id, doctor_id=doctor_id)
        db.session.add(case)
        db.session.commit()
