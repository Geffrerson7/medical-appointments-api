from app.extensions import db

class Patient(db.Model):
    __tablename__ = "patients"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, unique=True)
    
    user = db.relationship("User", back_populates="patient", uselist=False)
    appointments = db.relationship("Appointment", backref="patient", lazy=True)

    def __repr__(self):
        return f"<Patient ID {self.id} - User {self.user_id}>"

