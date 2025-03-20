from app.extensions import db
from flask import jsonify
from app.models import Patient, User


def create_patient(data):
    try:
        user_id = data.get("user_id")
        user = User.query.get(user_id)
        if not user:
            return jsonify({"message": "User not found"}), 404

        existing_patient = Patient.query.filter_by(user_id=user_id).first()
        if existing_patient:
            return jsonify({"message": "Patient already exists for this user"}), 400

        patient = Patient(**data)
        db.session.add(patient)
        db.session.commit()
        return jsonify({"message": "Patient created successfully"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "An error occurred", "error": str(e)}), 500


def get_patients():
    try:
        patients = Patient.query.all()
        if not patients:
            return jsonify({"message": "No patients found"}), 404
        patients_list = []
        for patient in patients:
            user = patient.user
            patients_list.append(
                {
                    "id": patient.id,
                    "user_id": patient.user_id,
                    "user": {
                        "first_name": user.first_name,
                        "last_name": user.last_name,
                        "dni": user.dni,
                        "email": user.email,
                        "username": user.username,
                        "phone": user.phone,
                        "city": user.city,
                        "country": user.country,
                        "date_of_birth": (
                            user.date_of_birth.strftime("%Y-%m-%d")
                            if user.date_of_birth
                            else None
                        ),
                        "address": user.address,
                        "role": user.role,
                        "is_active": user.is_active,
                        "date_joined": (
                            user.date_joined.strftime("%Y-%m-%d %H:%M:%S")
                            if user.date_joined
                            else None
                        ),
                    },
                }
            )
        return jsonify(patients_list), 200
    except Exception as e:
        return jsonify({"message": "An error occurred", "error": str(e)}), 500
