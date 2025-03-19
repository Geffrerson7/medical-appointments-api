from flask import Blueprint, request
from app.services.user_service import (
    create_user,
    get_users,
    login_user,
    patch_user,
    put_user,
    refresh_access_token,
    get_user_by_id,
)
from flask_jwt_extended import jwt_required

user_bp = Blueprint("user_bp", __name__, url_prefix="/users")


@user_bp.route("/", methods=["GET"])
def list_users():
    return get_users()


@user_bp.route("/register", methods=["POST"])
def new_user():
    data = request.get_json()
    return create_user(data)


@user_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    return login_user(data)


@user_bp.route("/<int:user_id>", methods=["GET"])
@jwt_required()
def get_user(user_id):
    return get_user_by_id(user_id)


@user_bp.route("/<int:id>", methods=["PATCH"])
@jwt_required()
def patch(id):
    data = request.get_json()
    return patch_user(id, data)


@user_bp.route("/<int:id>", methods=["PUT"])
@jwt_required()
def put(id):
    data = request.get_json()
    return put_user(id, data)


@user_bp.route("/token-refresh", methods=["POST"])
def refresh():
    data = request.get_json()
    refresh_token = data.get("refresh")
    return refresh_access_token(refresh_token)
