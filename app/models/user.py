from app.extensions import db
from sqlalchemy.sql import func
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(200), nullable=False)
    last_login = db.Column(db.DateTime(timezone=True), nullable=True)
    first_name = db.Column(db.String(150), nullable=False)
    last_name = db.Column(db.String(150), nullable=False)
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    date_joined = db.Column(db.DateTime(timezone=True), server_default=func.now())
    email = db.Column(db.String(80), unique=True, nullable=False)
    username = db.Column(db.String(45), unique=True, nullable=False)
    date_of_birth = db.Column(db.Date, nullable=True)
    role = db.Column(db.String(20), nullable=False, default="patient")

    doctor = db.relationship("Doctor", back_populates="user", uselist=False)
    patient = db.relationship("Patient", back_populates="user", uselist=False)

    def __repr__(self):
        return f"<User {self.username} ({self.email})>"

    def set_password(self, password):
        """Genera un hash del password"""
        self.password = generate_password_hash(password)

    def check_password(self, password):
        """Verifica que el password ingresado sea correcto"""
        return check_password_hash(self.password, password)
