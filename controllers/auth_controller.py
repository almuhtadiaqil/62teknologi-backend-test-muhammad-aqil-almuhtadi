from flask import Blueprint, request, jsonify
from schemes.auth_schema import LoginSchema, RegisterSchema, LoginResponseSchema
from schemes.user_schema import UserSchema
from common.base_response import BaseResponseSingle
from repositories.user_repository import UserRepository
from flask_jwt_extended import *
from datetime import datetime

auth_api = Blueprint("auth_api", __name__)
ts = datetime.utcnow()


@auth_api.route("/login", methods=["POST"])
def login():
    json = request.json
    schema = LoginSchema()
    user_schema = UserSchema()
    res = BaseResponseSingle(data=None, exception="", status=200)
    login_response = LoginResponseSchema()
    repo = UserRepository()
    try:
        payload = schema.load(json)
        user = repo.get_by_field("email", payload["email"])
        if user is None:
            raise Exception({"error": "credential missmatch!", "status": 400})
        if user.checkPassword(payload["password"]) is False:
            raise Exception({"error": "credential missmatchs!", "status": 400})
        jwt_payload = user_schema.dump(user)
        access_token = create_access_token(identity=jwt_payload)
        token_info = decode_token(access_token)
        expiration_time = token_info["exp"]
        login_response = login_response.dump(
            {
                "access_token": access_token,
                "expiration_time": datetime.fromtimestamp(expiration_time),
            }
        )
        res.data = login_response
        res.message = "login successfull!"
        return jsonify(res.serialize()), res.status
    except Exception as e:
        if len(e.args) > 0 and "error" in e.args[0]:
            res.message = str(e.args[0]["error"])
        else:
            res.message = str(e)
        if len(e.args) > 0 and "status" in e.args[0]:
            res.status = e.args[0]["status"]
        else:
            res.status = 400
        return jsonify(res.serialize()), res.status


@auth_api.route("/register", methods=["POST"])
def register():
    json = request.json
    schema = RegisterSchema()
    user_schema = UserSchema()
    res = BaseResponseSingle(data=None, exception="", status=200)
    repo = UserRepository()
    try:
        schema = schema.load(json)
        check = repo.get_by_field("email", schema["email"])
        if check:
            raise Exception({"error": "email already exists!", "status": 400})
        user = repo.store(schema)
        res_payload = user_schema.dump(user)
        res.data = res_payload
        res.message = "register successfully!"
        res.status = 201
        return jsonify(res.serialize(), res.status)
    except Exception as e:
        if len(e.args) > 0 and "error" in e.args[0]:
            res.message = str(e.args[0]["error"])
        else:
            res.message = str(e)
        if len(e.args) > 0 and "status" in e.args[0]:
            res.status = e.args[0]["status"]
        else:
            res.status = 400
        return jsonify(res.serialize()), res.status
