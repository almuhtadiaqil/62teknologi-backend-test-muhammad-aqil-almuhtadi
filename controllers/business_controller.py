from flask import Blueprint, request, jsonify
from datetime import datetime
from flask_jwt_extended import *
from schemes.business_schema import (
    BusinessSchema,
    BusinessPayloadSchema,
    BusinessCategoriesSchema,
    BusinessLocation,
    BusinessSearchSchema,
)
from repositories.business_repository import BusinessRepository
from common.base_response import BaseResponse, BaseResponseSingle
from common.helper import is_not_string

business_api = Blueprint("business_api", __name__)
ts = datetime.utcnow()


@business_api.route("/search", methods=["GET"])
@jwt_required()
def search():
    args = request.args
    query_params = BusinessSearchSchema()

    repo = BusinessRepository()
    schema = BusinessSchema(many=True)
    res = BaseResponse(data=None, message="", page=1, limit=10, status=200, total=0)
    try:
        query_params = query_params.load(args)
        business, total = repo.get_pagination(query_params)
        res_payload = schema.dump(obj=business)
        res.data = res_payload
        res.message = "data successfully retrieved!"
        if "limit" in query_params:
            res.limit = query_params["limit"]
        if "offset" in query_params:
            res.page = query_params["offset"]
        res.total = total
        res.status = 200
        return jsonify(res.serialize()), res.status
    except Exception as e:
        if len(e.args) > 0 and "error" in e.args[0]:
            print(e.args)
            res.message = str(e.args[0]["error"])
        else:
            res.message = str(e)
        if len(e.args) > 0 and "status" in e.args[0]:
            res.status = e.args[0]["status"]
        else:
            res.status = 400
        return jsonify(res.serialize()), res.status


@business_api.route("", methods=["POST"])
@jwt_required()
def store():
    json = request.json
    payload_schema = BusinessPayloadSchema()
    location_schema = BusinessLocation()
    categories_schema = BusinessCategoriesSchema(many=True)
    schema = BusinessSchema()
    res = BaseResponseSingle(data=None, exception="", status=200)
    display_address = []
    repo = BusinessRepository()
    try:
        payload = payload_schema.load(json)
        categories = categories_schema.load(json["categories"])
        payload.pop("categories")
        business = repo.store(payload, categories)
        transactions = business.transactions.split(",")
        location = location_schema.dump(
            {
                "address1": business.address1,
                "address2": business.address2,
                "address3": business.address3,
                "city": business.city,
                "state": business.state,
                "zip_code": business.zip_code,
                "country": business.country,
            }
        )
        if is_not_string(business.address1):
            display_address.append(business.address1)
        if is_not_string(business.address2):
            display_address.append(business.address2)
        if is_not_string(business.address3):
            display_address.append(business.address3)
        display_address.append(
            (business.city + ", ") + (business.state + " ") + (business.zip_code),
        )
        location["display_address"] = display_address
        res_payload = schema.dump(payload)
        res_payload["transactions"] = transactions
        res_payload["location"] = location
        res_payload["categories"] = categories
        res.data = res_payload
        res.message = "created successfully!"
        res.status = 201
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


@business_api.route("/<uuid:id>", methods=["PUT"])
@jwt_required()
def put(id):
    json = request.json
    payload_schema = BusinessPayloadSchema()
    location_schema = BusinessLocation()
    categories_schema = BusinessCategoriesSchema(many=True)
    schema = BusinessSchema()
    res = BaseResponseSingle(data=None, exception="", status=200)
    display_address = []
    repo = BusinessRepository()
    try:
        payload = payload_schema.load(json)
        categories = categories_schema.load(json["categories"])
        payload.pop("categories")
        business = repo.update("id", id, payload, categories)
        transactions = business.transactions.split(",")
        location = location_schema.dump(
            {
                "address1": business.address1,
                "address2": business.address2,
                "address3": business.address3,
                "city": business.city,
                "state": business.state,
                "zip_code": business.zip_code,
                "country": business.country,
            }
        )
        if is_not_string(business.address1):
            display_address.append(business.address1)
        if is_not_string(business.address2):
            display_address.append(business.address2)
        if is_not_string(business.address3):
            display_address.append(business.address3)
        display_address.append(
            (business.city + ", ") + (business.state + " ") + (business.zip_code),
        )
        location["display_address"] = display_address
        res_payload = schema.dump(payload)
        res_payload["transactions"] = transactions
        res_payload["location"] = location
        res_payload["categories"] = categories
        res.data = res_payload
        res.message = "created successfully!"
        res.status = 201
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


@business_api.route("/<uuid:id>", methods=["DELETE"])
@jwt_required()
def delete(id):
    res = BaseResponseSingle(
        data=None, exception="record deleted successfull!", status=200
    )
    repo = BusinessRepository()
    try:
        repo.delete("id", id)
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
