from app import db
import uuid
from sqlalchemy.dialects.postgresql import UUID
from models.business_categories_model import BusinessCategories
from sqlalchemy import event


class Business(db.Model):
    __tablename__ = "business"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4())
    alias = db.Column(db.String(255))
    name = db.Column(db.String(255))
    image_url = db.Column(db.Text())
    is_closed = db.Column(db.Boolean(), default=False)
    url = db.Column(db.Text())
    review_count = db.Column(db.Integer())
    rating = db.Column(db.Float())
    latitude = db.Column(db.Double())
    longitude = db.Column(db.Double())
    transactions = db.Column(db.Text())
    price = db.Column(db.String(255))
    address1 = db.Column(db.String(255))
    address2 = db.Column(db.String(255))
    address3 = db.Column(db.String(255))
    city = db.Column(db.String(100))
    zip_code = db.Column(db.String(6))
    country = db.Column(db.String(100))
    state = db.Column(db.String(10))
    phone = db.Column(db.String(20))
    display_phone = db.Column(db.String(20))
    distance = db.Column(db.Double())
    categories = db.relationship(BusinessCategories, backref="business", uselist=True)

    def __init__(
        self,
        id,
        alias,
        name,
        image_url,
        is_closed,
        url,
        review_count,
        rating,
        latitude,
        longitude,
        transactions,
        price,
        address1,
        address2,
        address3,
        city,
        zip_code,
        country,
        state,
        phone,
        display_phone,
        distance,
    ):
        self.id = id
        self.alias = alias
        self.name = name
        self.image_url = image_url
        self.is_closed = is_closed
        self.url = url
        self.review_count = review_count
        self.rating = rating
        self.latitude = (latitude,)
        self.longitude = (longitude,)
        self.transactions = transactions
        self.price = price
        self.address1 = address1
        self.address2 = address2
        self.address3 = address3
        self.city = city
        self.zip_code = zip_code
        self.country = country
        self.state = state
        self.phone = phone
        self.display_phone = display_phone
        self.distance = distance
        # self.categories = categories


@event.listens_for(Business, "load")
def load_listener(target, context):
    target.transactions = target.transactions.split(",")
