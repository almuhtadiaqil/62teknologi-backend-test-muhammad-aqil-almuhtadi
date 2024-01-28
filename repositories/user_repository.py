from schemes.auth_schema import RegisterSchema
from models.user_model import User
from datetime import datetime
from app import db
from repositories.base_repository import BaseRepository

ts = datetime.utcnow()


class UserRepository(BaseRepository):
    def __init__(self) -> None:
        super().__init__(model=User)

    def store(self, schema: RegisterSchema):
        try:
            data = self.model(**schema)
            data.setPassword(schema["password"])
            db.session.add(data)
            db.session.commit()
            return data
        except Exception as e:
            raise Exception({"error": e, "status": 500})
