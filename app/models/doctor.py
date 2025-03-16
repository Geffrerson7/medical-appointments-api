from app.extensions import db
from sqlalchemy import ForeignKey


class Doctor(db.Model):
    __tablename__ = "doctors"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey("users.id"), nullable=False)
    specialty = db.Column(db.String(100), nullable=False)
    identification_code = db.Column(db.String(50), unique=True, nullable=False)

    user = db.relationship("User", back_populates="doctor")
    appointments = db.relationship("Appointment", backref="doctor", lazy=True)
    schedules = db.relationship("Schedule", backref="doctor", lazy=True)
    doctor_rooms = db.relationship("DoctorRoom", back_populates="doctor")

    def __repr__(self):
        return (
            f"<Doctor {self.user.first_name} {self.user.last_name} - {self.specialty}>"
        )
