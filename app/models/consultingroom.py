from app.extensions import db


class ConsultingRoom(db.Model):
    __tablename__ = "consulting_rooms"

    id = db.Column(db.Integer, primary_key=True)
    room_number = db.Column(db.String(20), nullable=False)  # Número o código del consultorio
    location = db.Column(db.String(250), nullable=False)  # Dirección o sede de la clínica

    # Relationships
    doctor_rooms = db.relationship("DoctorRoom", back_populates="consulting_room")

    def __repr__(self):
        return f"<ConsultingRoom {self.room_number} - {self.location}>"
