from app.extensions import db
from sqlalchemy.sql import func
from sqlalchemy import ForeignKey


class DoctorRoom(db.Model):
    __tablename__ = "doctor_rooms"

    id = db.Column(db.Integer, primary_key=True)
    doctor_id = db.Column(db.Integer, ForeignKey("doctors.id"), nullable=False)
    room_id = db.Column(db.Integer, ForeignKey("consulting_rooms.id"), nullable=False)
    assigned_date = db.Column(db.DateTime, server_default=func.now())

    doctor = db.relationship("Doctor", back_populates="doctor_rooms")
    consulting_room = db.relationship("ConsultingRoom", back_populates="doctor_rooms")

    def __repr__(self):
        return f"<DoctorRoom Doctor {self.doctor_id} - Room {self.room_id}>"
