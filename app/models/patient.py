from werkzeug.security import generate_password_hash, check_password_hash
from app.extensions import db
from sqlalchemy.sql import func

class Patient(db.Model):
    __tablename__ = "patients"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    dni = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    date_of_birth = db.Column(db.Date, nullable=True)
    last_login = db.Column(db.DateTime(timezone=True), nullable=True)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, unique=True)

    user = db.relationship("User", back_populates="patient", uselist=False)
    appointments = db.relationship("Appointment", backref="patient", lazy=True)

    def __repr__(self):
        return f"<Patient {self.first_name} {self.last_name} - {self.email}>"

    def set_password(self, password):
        """Genera un hash del password"""
        self.password = generate_password_hash(password)

    def check_password(self, password):
        """Verifica que el password ingresado sea correcto"""
        return check_password_hash(self.password, password)

