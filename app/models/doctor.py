from werkzeug.security import generate_password_hash, check_password_hash
from app.extensions import db


class Doctor(db.Model):
    __tablename__ = "doctors"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    dni = db.Column(db.String(20), unique=True, nullable=False)
    specialty = db.Column(db.String(100), nullable=False)
    identification_code = db.Column(db.String(50), unique=True, nullable=False)

    appointments = db.relationship("Appointment", backref="doctor", lazy=True)

    schedules = db.relationship("Schedule", backref="doctor", lazy=True)

    def __repr__(self):
        return f"<Doctor {self.name} - {self.specialty}>"

    def set_password(self, password):
        """Genera un hash del password"""
        self.password = generate_password_hash(password)

    def check_password(self, password):
        """Verifica que el password ingresado sea correcto"""
        return check_password_hash(self.password, password)