import uuid
import datetime

from sqlalchemy.dialects.postgresql import UUID
from marshmallow import fields, Schema

from src import db


class Blacklist(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = db.Column(db.String(140), unique=True)
    app_uuid = db.Column(UUID(as_uuid=True), unique=True)
    blocked_reason = db.Column(db.String(140))
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)


class BlacklistSchema(Schema):
    id = fields.UUID()
    email = fields.Str()
    app_uuid = fields.UUID()
    blocked_reason = fields.Str()
    created_at = fields.DateTime()
