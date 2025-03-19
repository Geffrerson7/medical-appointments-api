from app.models import User
from app.extensions import db
from flask import jsonify
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    decode_token,
)
from datetime import datetime
import traceback

def get_users():
    try:
        users = User.query.all()
        if not users:
            return jsonify({"message": "No users found"}), 404
        users_list = [
            {
                "id": user.id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
                "username": user.username,
                "date_of_birth": (
                    user.date_of_birth.strftime("%Y-%m-%d")
                    if user.date_of_birth
                    else None
                ),
                "role": user.role,
            }
            for user in users
        ]
        return jsonify(users_list), 200
    except Exception as e:
        return jsonify({"message": "An error occurred", "error": str(e)}), 500


def create_user(data):
    try:
        if User.query.filter_by(email=data["email"]).first():
            return jsonify({"message": "Email already registered"}), 400
        new_user = User(
            first_name=data["first_name"],
            last_name=data["last_name"],
            email=data["email"],
            username=data["username"],
            role=data["role"],
        )
        new_user.set_password(data["password"])
        db.session.add(new_user)
        db.session.commit()
        return {"message": "User created"}, 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "An error occurred", "error": str(e)}), 500


def login_user(data):
    try:
        user = User.query.filter_by(email=data["email"]).first()
        if not user or not user.check_password(data["password"]):
            return jsonify({"message": "Invalid credentials"}), 401

        access_token = create_access_token(identity=str(user.id))
        refresh_token = create_refresh_token(identity=str(user.id))
        # Decodificar el token para obtener la fecha de expiración
        decoded_token = decode_token(access_token)
        expires_at = datetime.fromtimestamp(decoded_token["exp"]).strftime(
            "%Y-%m-%dT%H:%M:%S"
        )

        user.last_login = datetime.now()
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
                    "message": "An error occurred during user login",
                    "error": str(e),
                }
            ),
            500,
        )


def patch_user(id, data):
    try:
        user = User.query.get(str(id))
        if not user:
            return jsonify({"message": "User not found"}), 404

        updated_fields = []

        # Actualización parcial: Solo modifica los campos proporcionados
        if "first_name" in data:
            user.first_name = data["first_name"]
            updated_fields.append("First Name")

        if "last_name" in data:
            user.last_name = data["last_name"]
            updated_fields.append("Last Name")

        if "email" in data:
            user.email = data["email"]
            updated_fields.append("Email")

        if "password" in data:
            user.set_password(data["password"])
            updated_fields.append("Password")

        if "date_of_birth" in data:
            user.date_of_birth = data["date_of_birth"]
            updated_fields.append("Date of Birth")

        if "username" in data:
            user.username = data["username"]
            updated_fields.append("Username")

        db.session.commit()

        message = "User updated successfully"
        if updated_fields:
            message += f". Fields updated: {', '.join(updated_fields)}"

        return (
            jsonify(
                {
                    "message": message,
                    "user": {
                        "id": user.id,
                        "first_name": user.first_name,
                        "last_name": user.last_name,
                        "email": user.email,
                        "username": user.username,
                        "date_of_birth": (
                            user.date_of_birth.strftime("%Y-%m-%d")
                            if user.date_of_birth
                            else None
                        ),
                    },
                }
            ),
            200,
        )
    except Exception as e:
        return (
            jsonify(
                {
                    "message": "An error occurred while updating the user",
                    "error": str(e),
                }
            ),
            500,
        )


def put_user(id, data):
    try:
        user = User.query.get(id)
        if not user:
            return jsonify({"message": "User not found"}), 404

        required_fields = [
            "first_name",
            "last_name",
            "email",
            "role",
            "password",
            "date_of_birth",
        ]
        missing_fields = [field for field in required_fields if field not in data]

        if missing_fields:
            return (
                jsonify(
                    {"message": f"Missing required fields: {', '.join(missing_fields)}"}
                ),
                400,
            )

        existing_user = User.query.filter_by(email=data["email"]).first()
        if existing_user and existing_user.id != user.id:
            return jsonify({"message": "Email already in use"}), 400

        user.first_name = data["first_name"]
        user.last_name = data["last_name"]
        user.email = data["email"]
        user.role = data["role"]
        user.set_password(data["password"])

        if data["date_of_birth"]:
            user.date_of_birth = datetime.strptime(
                data["date_of_birth"], "%Y-%m-%d"
            ).date()

        if "username" in data:
            existing_username = User.query.filter_by(username=data["username"]).first()
            if existing_username and existing_username.id != user.id:
                return jsonify({"message": "Username already in use"}), 400
            user.username = data["username"]

        if "is_active" in data:
            user.is_active = data["is_active"]

        db.session.commit()

        return (
            jsonify(
                {
                    "message": "User updated successfully",
                    "user": {
                        "id": user.id,
                        "first_name": user.first_name,
                        "last_name": user.last_name,
                        "email": user.email,
                        "role": user.role,
                        "date_of_birth": (
                            user.date_of_birth.strftime("%Y-%m-%d")
                            if user.date_of_birth
                            else None
                        ),
                        "username": user.username,
                        "is_active": user.is_active,
                    },
                }
            ),
            200,
        )

    except Exception as e:
        db.session.rollback()
        return (
            jsonify(
                {
                    "message": "An error occurred while updating the user",
                    "error": str(e),
                }
            ),
            500,
        )


def refresh_access_token(refresh_token):
    if not refresh_token:
        return jsonify({"msg": "Missing refresh token"}), 400

    try:
        decoded = decode_token(refresh_token)
        identity = decoded.get("sub")
        exp_timestamp = decoded.get("exp")

        if datetime.now() > datetime.fromtimestamp(exp_timestamp):
            return jsonify({"msg": "Refresh token expired"}), 401

        new_access_token = create_access_token(identity=identity)
        decoded_access = decode_token(new_access_token)
        access_expiration = datetime.fromtimestamp(decoded_access['exp'])

        return jsonify({
            "access_token": new_access_token,
            "access_token_expiration": access_expiration.isoformat()
        }), 200

    except Exception as e:
        traceback_str = traceback.format_exc()
        return jsonify({
            "msg": f"Internal Server Error: {str(e)}",
            "traceback": traceback_str
        }), 500