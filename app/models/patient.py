from app.extensions import db
from sqlalchemy import ForeignKey


class Patient(db.Model):
    __tablename__ = "patients"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey("users.id"), nullable=False)
    dni = db.Column(db.String(20), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=True)

    user = db.relationship("User", back_populates="patient")
    appointments = db.relationship("Appointment", backref="patient", lazy=True)

    def __repr__(self):
        return f"<Patient {self.user.first_name} {self.user.last_name} - {self.user.email}>"
