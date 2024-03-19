from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    SubmitField,
    RadioField,
    PasswordField,
    BooleanField,
    ValidationError,
)
from wtforms.validators import DataRequired, Length, Email, EqualTo
from wtforms_sqlalchemy.fields import QuerySelectField
from app.commands import get_specialties


class UserForm(FlaskForm):
    username = StringField(
        "Username",
        validators=[DataRequired("Username required"), Length(min=2, max=20)],
    )
    email = StringField("E-mail", validators=[Email("Invalid email address.")])
    password = PasswordField(
        "Password"
    )  #  validators=[DataRequired("Password required")]
    confirm_password = PasswordField(
        "Confirm Password", validators=[EqualTo("password")]
    )
    remember = BooleanField("Remember me")
    submit = SubmitField("Connect")
    user_type = RadioField(
        "Type of user: ",
        choices=[("patient", "Patient"), ("doctor", "Doctor")],
        validators=[DataRequired()],
    )
    specialty = QuerySelectField(
        "Specialty",
        query_factory=get_specialties,
        get_label="specialty",
        # allow_blank=True,
        # blank_text="Select specialty",
    )
    
    def is_register_form(self):
        return self.confirm_password.data is not None

    def validate(self, extra_validators=None):
        if self.is_register_form():
            if not self.confirm_password.data:
                self.confirm_password.errors.append("Confirm Password required")
                return False

            if self.user_type.data == "doctor":
                if not self.specialty.data:
                    self.specialty.errors.append("Specialty required for doctors")
                    return False
            # elif self.user_type.data == 'patient':
            # self.patient.errors = []
        # if not self.user_type.data:
        #     self.user_type.errors.append('Field required')
        #     return False
        return True

    def validate_email(self, email):
        if self.is_register_form() and not email:
            self.email.errors.append("E-mail reuired")
            return False
        elif email:
            email_validator = Email(email)
            if not email_validator:
                self.email.errors.append("Invalid email address.")
                return False
        if self.is_register_form() and ('@' not in email):
                return False
        return True


def validate(self, extra_validators=None):
    if not self.is_register_form():
        self.confirm_password.errors = []
        del self._fields["confirm_password"]

    # Now call the parent class's validate method to run standard validations
    if not super(UserForm, self).validate(extra_validators=extra_validators):
        return False

    # Custom validation logic for registration
    if self.is_register_form():
        if self.password.data != self.confirm_password.data:
            self.confirm_password.errors.append("Field must be equal to password.")
            return False

    return True


class Symptoms(FlaskForm):
    description = StringField("Description")
    feelings = StringField("Feelings")
    location = StringField("Location")
    severity = StringField("Severity")


class Appointment(FlaskForm):
    specialty = QuerySelectField(
        "Specialty",
        query_factory=get_specialties,
        get_label="specialty",
        allow_blank=True,
        blank_text="--select specialty--",
    )
    availabledoctors = QuerySelectField(
        "Doctors",
        query_factory=get_specialties,
        get_label="doctor",
        allow_blank=True,
        blank_text="--select doctor--",
    )
