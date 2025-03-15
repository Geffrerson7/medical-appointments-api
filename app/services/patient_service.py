from app.models import Patient
from app.extensions import db
from flask import jsonify
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    decode_token,
)
from datetime import datetime


def get_patients():
    try:
        patients = Patient.query.all()
        if not patients:
            return jsonify({"message": "No patients found"}), 404
        return [
            {
                "id": p.id,
                "first_name": p.first_name,
                "last_name": p.last_name,
                "email": p.email,
                "dni": p.dni,
                "phone": p.phone,
                "date_of_birth": p.date_of_birth,
            }
            for p in patients
        ]
    except Exception as e:
        return jsonify({"message": "An error occurred", "error": str(e)}), 500


def create_patient(data):
    try:
        if Patient.query.filter_by(email=data["email"]).first():
            return jsonify({"message": "Email already registered"}), 400
        new_patient = Patient(
            first_name=data["first_name"],
            last_name=data["last_name"],
            email=data["email"],
            dni=data["dni"],
        )
        new_patient.set_password(data["password"])
        db.session.add(new_patient)
        db.session.commit()
        return {"message": "Patient created"}, 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "An error occurred", "error": str(e)}), 500


def login_user(data):
    try:
        patient = Patient.query.filter_by(email=data["email"]).first()
        if not patient or not patient.check_password(data["password"]):
            return jsonify({"message": "Invalid credentials"}), 401

        access_token = create_access_token(identity=str(patient.id))
        refresh_token = create_refresh_token(identity=str(patient.id))
        # Decodificar el token para obtener la fecha de expiración
        decoded_token = decode_token(access_token)
        expires_at = datetime.fromtimestamp(decoded_token["exp"]).strftime(
            "%Y-%m-%dT%H:%M:%S"
        )

        patient.last_login = datetime.now()
        db.session.commit()

        return jsonify(
            {
                "access_token": access_token,
                "refresh_token": refresh_token,
                "expires_at": expires_at,
            }
        )
    except Exception as e:
        return (
            jsonify(
                {
                    "message": "An error occurred during patient login",
                    "error": str(e),
                }
            ),
            500,
        )


def patch_patient(id, data):
    try:
        patient = Patient.query.get(str(id))
        if not patient:
            return jsonify({"message": "Patient not found"}), 404

        # Actualización parcial: Solo modifica los campos proporcionados
        patient.first_name = data.get("first_name", patient.first_name)
        patient.last_name = data.get("last_name", patient.last_name)
        patient.phone = data.get("phone", patient.phone)
        patient.email = data.get("email", patient.email)
        patient.dni = data.get("dni", patient.dni)
        if "password" in data:
            patient.set_password(data["password"])

        db.session.commit()

        return (
            jsonify(
                {
                    "message": "Patient updated successfully",
                    "patient": {
                        "id": patient.id,
                        "first_name": patient.first_name,
                        "last_name": patient.last_name,
                        "email": patient.email,
                        "dni": patient.dni,
                        "phone": patient.phone,
                    },
                }
            ),
            200,
        )
    except Exception as e:
        return (
            jsonify(
                {
                    "message": "An error occurred while updating the patient",
                    "error": str(e),
                }
            ),
            500,
        )
