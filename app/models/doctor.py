from app.extensions import db


class Doctor(db.Model):
    __tablename__ = "doctors"

    id = db.Column(db.Integer, primary_key=True)
    specialty = db.Column(db.String(100), nullable=False)
    identification_code = db.Column(db.String(50), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, unique=True)

    user = db.relationship("User", back_populates="doctor", uselist=False)
    appointments = db.relationship("Appointment", backref="doctor", lazy=True)
    schedules = db.relationship("Schedule", backref="doctor", lazy=True)
    doctor_rooms = db.relationship("DoctorRoom", back_populates="doctor")

    def __repr__(self):
        first_name = self.user.first_name if self.user else "Unknown"
        last_name = self.user.last_name if self.user else "Unknown"
        return f"<Doctor {first_name} {last_name} - {self.specialty}>"
