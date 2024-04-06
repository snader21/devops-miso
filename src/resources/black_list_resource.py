import os
from flask_restful import Resource
from flask import request
import re
import uuid
from src.models.blacklist_model import Blacklist, BlacklistSchema
from src import db

blacklist_schema = BlacklistSchema()


class BlackListResource(Resource):

    def post(self):

        # 1. Get token from request
        token = request.headers.get('Authorization')
        if token is None:
            return {'status': 'fail', 'msg': 'Por favor provea un token para autenticarse'}, 403

        # 2. Verify token
        if token != f"Bearer {os.getenv('API_KEY')}":
            return {'status': 'fail', 'msg': 'Token inválido'}, 401

        # 3. Validate required fields
        body_data = request.get_json()
        required_fields = ["email", "app_uuid", "blocked_reason"]
        for field in required_fields:
            if field not in body_data:
                return {'status': 'fail', 'msg': f'Campo {field} es requerido'}, 400

        # 4. Validate fields types
        # 4.1 email
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, body_data['email']):
            return {'status': 'fail', 'msg': 'Correo inválido'}, 400

        # 4.2 app_uuid
        try:
            app_uuid_str = uuid.UUID(body_data["app_uuid"])
            if str(app_uuid_str) != body_data["app_uuid"]:
                raise ValueError("Invalid UUID")
        except ValueError:
            return {'status': 'fail', 'msg': 'app_uuid inválido'}, 400

        # 5. Check duplicates
        query = db.session.query(Blacklist).filter(
            Blacklist.email == body_data["email"] and Blacklist.app_uuid == body_data["app_uuid"]).first()
        if query != None:
            return {'status': 'fail', 'msg': 'Este correo ya fue ingresado a la lista negra de esta aplicación'}, 409

        # 6. Save to database
        new_blacklist = Blacklist(
            email=body_data["email"],
            app_uuid=body_data["app_uuid"],
            blocked_reason=body_data["blocked_reason"]
        )
        db.session.add(new_blacklist)
        db.session.commit()

        # 7. Return response
        return {'status': 'success', 'msg': 'Correo agregado a la lista negra', "data": blacklist_schema.dump(new_blacklist)}, 201

    def get(self, email):

        # 1. Get token from request
        token = request.headers.get('Authorization')
        if token is None:
            return {'status': 'fail', 'msg': 'Por favor provea un token para autenticarse'}, 403

        # 2. Verify token
        if token != f"Bearer {os.getenv('API_KEY')}":
            return {'status': 'fail', 'msg': 'Token inválido'}, 401

        # 3. Get blacklist by email
        query = db.session.query(Blacklist).filter(
            Blacklist.email == email).first()

        if query == None:
            return {'status': 'fail', 'data': {'encontrado': False}}, 404
        else:
            return {'status': 'success', 'data': {'encontrado': True, 'blocked_reason': query.blocked_reason}}, 200
