import json
from app.models import db, Specialty, Patient, Doctor, Case, Appointments
from datetime import datetime

def import_specialties():
    with open('instance/doctor_speciality.json', 'r') as file:
        specialities = json.load(file)

    if Specialty.query.first() is None:
        for item in specialities:
            specialty = Specialty(specialty=item['specialty'])
            db.session.add(specialty)
        db.session.commit()
        print('------ * Specialties have benn imported. * ------')
    else:
        print('------ * Specialties already filled. * ------')

def get_specialties():
    return Specialty.query.all()


# Import backup data in DB
def import_data(model, data):
    if data:
        # instances = [model(**item) for item in data]
        instances = []
        for item in data:
            if 'datetime' in item:
                item['datetime'] = datetime.strptime(item['datetime'], '%Y-%m-%dT%H:%M:%S')
            instances.append(model(**item))
        db.session.bulk_save_objects(instances)
        print(f"Imported {len(instances)} instances of {model.__name__}.")
    else:
        print(f"-----* {model.__name__} is empty *-----")

def reimport_db():
    with open("backup/dbbackup.json", "r") as file:
        backup = json.load(file)

    try:
        
        import_data(Patient, backup.get("Patient", []))
        import_data(Doctor, backup.get("Doctor", []))
        import_data(Case, backup.get("Case", []))
        import_data(Appointments, backup.get("Appointments", []))
        db.session.commit()
        print("DB reimported successfully.")

    except Exception as e:
        db.session.rollback()
        print(f"An error occured during the import: {e}")
        import traceback
        traceback.print_exc()