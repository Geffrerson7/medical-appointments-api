from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from app.services.patient_service import get_patients, create_patient

patient_bp = Blueprint("patient_bp", __name__, url_prefix="/patients")


@patient_bp.route("/", methods=["GET"])
@jwt_required()
def list_patients():
    return get_patients()


@patient_bp.route("/register", methods=["POST"])
@jwt_required()
def new_patient():
    data = request.get_json()
    return create_patient(data)
