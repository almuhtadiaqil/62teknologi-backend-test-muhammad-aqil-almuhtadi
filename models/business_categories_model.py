from app import db
import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import ForeignKey


class BusinessCategories(db.Model):
    __tablename__ = "business_categories"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4())
    business_id = db.Column(
        UUID(as_uuid=True),
        ForeignKey("business.id", ondelete="CASCADE", onupdate="CASCADE"),
    )
    alias = db.Column(db.String(255))
    title = db.Column(db.String(255))
    # business = db.relationship("Business", back_populates="business_categories")

    def __init__(self, id, business_id, alias, title) -> None:
        self.id = id
        self.business_id = business_id
        self.alias = alias
        self.title = title
