from sqlalchemy import and_
from src.models.blacklist_model import BlacklistSchema

blacklist_schema = BlacklistSchema()


class DAO:
    def __init__(self, db, model):
        self.db = db
        self.model = model

    def find_one_by_options(self, **kwargs):
        record = self.db.session.query(self.model).filter(
            and_(*[getattr(self.model, k) == v for k, v in kwargs.items()])).first()
        return blacklist_schema.dump(record) if record else None

    def create(self, data):
        new_instance = self.model(**data)
        self.db.session.add(new_instance)
        self.db.session.commit()
        return blacklist_schema.dump(new_instance)
