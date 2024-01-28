from models.business_model import Business
from repositories.base_repository import BaseRepository
from schemes.business_schema import (
    BusinessPayloadSchema,
    BusinessCategoriesSchema,
    BusinessSearchSchema,
)
from app import db
from uuid import uuid4
from models.business_categories_model import BusinessCategories
from sqlalchemy import cast, String, text
from math import radians, sin, cos, acos


class BusinessRepository(BaseRepository):
    def __init__(self) -> None:
        super().__init__(Business)

    def store(
        self, payload: BusinessPayloadSchema, categories: BusinessCategoriesSchema
    ):
        try:
            business = self.model(**payload, id=uuid4())
            db.session.add(business)
            db.session.add_all(
                BusinessCategories(**category, business_id=business.id, id=uuid4())
                for category in categories
            )
            db.session.commit()
            return business
        except Exception as e:
            db.session.rollback()
            raise Exception({"error": e, "status": 500})

    def update(
        self,
        field,
        value,
        payload: BusinessPayloadSchema,
        categories: BusinessCategoriesSchema,
    ):
        try:
            data = self.model.query.filter(self.model.id == value).first()
            if data is None:
                raise Exception({"error": "record not found", "status": 500})
            for key, value in payload.items():
                value = value if callable(value) else value
                setattr(data, key, value)
            if len(categories) > 0:
                BusinessCategories.query.filter(
                    text("business_id = '{}'".format(data.id))
                ).delete()

            db.session.add_all(
                BusinessCategories(**category, business_id=data.id, id=uuid4())
                for category in categories
            )
            db.session.commit()
            return data
        except Exception as e:
            db.session.rollback()
            raise Exception({"error": e, "status": 500})

    def get_pagination(self, request: BusinessSearchSchema):
        query = self.model.query
        offset = 0
        limit = 10
        if "offset" in request:
            offset = request["offset"]
        if "limit" in request:
            limit = request["limit"]

        if "location" in request:
            location = request["location"].lower()
            query = query.filter(
                self.model.address1.ilike("%" + location + "%")
                | self.model.address2.ilike("%" + location + "%")
                | self.model.address3.ilike("%" + location + "%")
                | self.model.city.ilike("%" + location + "%")
                | self.model.state.ilike("%" + location + "%")
                | self.model.country.ilike("%" + location + "%")
                | self.model.zip_code.ilike("%" + location + "%")
            )
        if "latitude" in request:
            latitude = str(request["latitude"])
            query = query.filter(
                cast(self.model.latitude, String()).like(f"%{latitude}%")
            )
        if "longitude" in request:
            longitude = str(request["longitude"])
            query = query.filter(
                cast(self.model.longitude, String()).like(f"%{longitude}%")
            )
        if "radius" in request:
            radius = request["radius"]
            radius_clause = f"""                
            (
                    6371
                    * acos(
                        cos(radians(business.latitude))
                        * cos(radians({latitude}))
                        * cos(radians({longitude}) - radians(business.longitude))
                        + sin(radians(business.latitude)) * sin(radians({latitude}))
                    )
                    * 1000
                )
                <= {radius}
            """
            query = query.filter(text(radius_clause))
        if "open_now" in request:
            open_now = request["open_now"]
            query = query.filter(self.model.is_closed == open_now)

        total = len(query.all())
        query = query.limit(limit)
        query = query.offset(offset * limit)
        # query = query.paginate(page=offse t, per_page=limit)
        query = query.all()
        return query, total
