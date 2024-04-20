from sqlalchemy import and_


class DAO:
    def __init__(self, db, model):
        self.db = db
        self.model = model

    def find_one_by_options(self, **kwargs):
        return self.db.session.query(self.model).filter(and_(*[getattr(self.model, k) == v for k, v in kwargs.items()])).first()

    def create(self, data):
        new_instance = self.model(**data)
        self.db.session.add(new_instance)
        self.db.session.commit()
        return new_instance
