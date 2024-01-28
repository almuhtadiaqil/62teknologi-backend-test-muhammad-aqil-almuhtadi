from marshmallow import Schema, fields, validate, validates_schema, pre_dump
from common.helper import is_not_string


class BusinessCategoriesSchema(Schema):
    alias = fields.String()
    title = fields.String()


class BusinessLocation(Schema):
    address1 = fields.String()
    address2 = fields.String()
    address3 = fields.String()
    city = fields.String()
    state = fields.String()
    zip_code = fields.String()
    country = fields.String()
    display_address = fields.List(fields.String())


class BusinessSchema(Schema):
    id = fields.UUID()
    alias = fields.String()
    name = fields.String()
    image_url = fields.Url()
    is_closed = fields.Boolean()
    url = fields.Url()
    review_count = fields.Integer()
    categories = fields.List(fields.Nested(BusinessCategoriesSchema))
    rating = fields.Float()
    transactions = fields.List(fields.String())
    location = fields.Nested(BusinessLocation)
    phone = fields.String()
    display_phone = fields.String()
    distance = fields.Float()
    latitude = fields.Float()
    longitude = fields.Float()
    price = fields.String()

    @pre_dump(pass_many=True)
    def preprocess_data(self, data, many):
        if many:
            for record in data:
                location_schema = BusinessLocation()
                location = location_schema.dump(
                    {
                        "address1": record.address1,
                        "address2": record.address2,
                        "address3": record.address3,
                        "city": record.city,
                        "state": record.state,
                        "zip_code": record.zip_code,
                        "country": record.country,
                    }
                )
                display_address = []
                if is_not_string(record.address1):
                    display_address.append(record.address1)
                if is_not_string(record.address2):
                    display_address.append(record.address2)
                if is_not_string(record.address3):
                    display_address.append(record.address3)
                display_address.append(
                    (record.city + ", ") + (record.state + " ") + (record.zip_code),
                )
                location["display_address"] = display_address
                record.location = location
        else:
            location_schema = BusinessLocation()
            location = location_schema.dump(
                {
                    "address1": data["address1"],
                    "address2": data["address2"],
                    "address3": data["address3"],
                    "city": data["city"],
                    "state": data["state"],
                    "zip_code": data["zip_code"],
                    "country": data["country"],
                }
            )
            display_address = []
            if is_not_string(data["address1"]):
                display_address.append(data["address1"])
            if is_not_string(data["address2"]):
                display_address.append(data["address2"])
            if is_not_string(data["address3"]):
                display_address.append(data["address3"])
            display_address.append(
                (data["city"] + ", ") + (data["state"] + " ") + (data["zip_code"]),
            )
            location["display_address"] = display_address
            data["location"] = location
        return data


class BusinessPayloadSchema(BusinessSchema):
    transactions = fields.String()
    address1 = fields.String()
    address2 = fields.String()
    address3 = fields.String()
    city = fields.String()
    state = fields.String()
    zip_code = fields.String(validate=validate.Length(min=5))
    country = fields.String()


class BusinessSearchSchema(Schema):
    location = fields.String()
    latitude = fields.Float()
    longitude = fields.Float()
    radius = fields.Integer(validate=validate.Range(max=40000))
    open_now = fields.Boolean()
    limit = fields.Integer()
    offset = fields.Integer()
    sort_by = fields.String()
    price = fields.String()

    @validates_schema()
    def validate_location_requires_latitude(self, data, partial=False, many=False):
        if (
            "longitude" not in data
            and "latitude" not in data
            and "location" not in data
        ):
            raise Exception(
                {
                    "error": "Your longitude and latitude is empty, please provide your location",
                    "status": 400,
                }
            )

    @validates_schema()
    def validate_latitude_requires_longitude(self, data, partial=False, many=False):
        if (
            "location" not in data
            and "latitude" not in data
            and "longitude" not in data
        ):
            raise Exception(
                {
                    "error": "Your location is empty, please provide your latitude!",
                    "status": 400,
                }
            )
        elif "location" not in data and "latitude" not in data and "longitude" in data:
            raise Exception(
                {
                    "error": "Your longitude is exists, provide your latitude!",
                    "status": 400,
                }
            )

    @validates_schema()
    def validate_longitude_requires_latitude(self, data, partial=False, many=False):
        if (
            "location" not in data
            and "longitude" not in data
            and "latitude" not in data
        ):
            raise Exception(
                {
                    "error": "Your location is empty, please provide your longitude!",
                    "status": 400,
                }
            )
        elif "location" not in data and "longitude" not in data and "latitude" in data:
            raise Exception(
                {
                    "error": "Your latitude is exists, please provide your longitude!",
                    "status": 400,
                }
            )
