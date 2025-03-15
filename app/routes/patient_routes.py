from flask import Blueprint, request, jsonify
from app.services.patient_service import (
    create_patient,
    get_patients,
    login_user,
    patch_patient,
)
from flask_jwt_extended import jwt_required

patient_bp = Blueprint("patient_bp", __name__, url_prefix="/patients")


@patient_bp.route("/", methods=["GET"])
def list_patients():
    return jsonify(get_patients())


@patient_bp.route("/", methods=["POST"])
def new_patient():
    data = request.get_json()
    return create_patient(data)


@patient_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    return login_user(data)


@patient_bp.route("/<int:id>", methods=["PATCH"])
@jwt_required()
def patch(id):
    data = request.get_json()
    return patch_patient(id, data)
