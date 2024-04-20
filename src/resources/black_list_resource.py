import os
from flask_restful import Resource
from flask import request
import re
import uuid
from src.models.blacklist_model import Blacklist, BlacklistSchema
from src import db
from src.infrastructure.dao import DAO

blacklist_schema = BlacklistSchema()


class BlackListResource(Resource):

    def post(self):

        # 0. Get ip from request
        ip_address = request.headers.get(
            'X-Forwarded-For', request.remote_addr).split(',')[0]
        # 1. Get token from request
        token = request.headers.get('Authorization')
        if token is None:
            return {'status': 'fail', 'msg': 'Por favor provea un token para autenticarse'}, 403

        # 2. Verify token
        if token != f"Bearer {os.getenv('API_KEY')}":
            return {'status': 'fail', 'msg': 'Token inválido'}, 401

        # 3. Validate required fields
        body_data = request.get_json()
        required_fields = ["email", "app_uuid"]
        for field in required_fields:
            if field not in body_data:
                return {'status': 'fail', 'msg': f'Campo {field} es requerido'}, 400

        # 4. Validate fields types
        # 4.1 email
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, body_data.get('email')):
            return {'status': 'fail', 'msg': 'Correo inválido'}, 400

        # 4.2 app_uuid
        try:
            app_uuid_str = uuid.UUID(body_data.get("app_uuid"))
            if str(app_uuid_str) != body_data.get("app_uuid"):
                raise ValueError("Invalid UUID")
        except ValueError:
            return {'status': 'fail', 'msg': 'app_uuid inválido'}, 400

        black_list_dao = DAO(db, Blacklist)

        # 5. Check duplicates
        blacklist_entry = black_list_dao.find_one_by_options(
            email=body_data.get("email"), app_uuid=body_data.get("app_uuid"))

        if blacklist_entry != None:
            return {'status': 'fail', 'msg': 'Este correo ya fue ingresado a la lista negra de esta aplicación'}, 409

        # 6. Save to database
        new_blacklist = black_list_dao.create({
            "email": body_data.get("email"),
            "ip_address": ip_address,
            "app_uuid": body_data.get("app_uuid"),
            "blocked_reason": body_data.get("blocked_reason")
        })

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
        black_list_dao = DAO(db, Blacklist)
        blacklist_record = black_list_dao.find_one_by_options(email=email)

        if blacklist_record == None:
            return {'status': 'fail', 'data': {'encontrado': False}}, 404
        else:
            return {'status': 'success', 'data': {'encontrado': True, 'blocked_reason': blacklist_record.blocked_reason}}, 200


class BlackListHealthResource(Resource):
    def get(self):
        return 'pong', 200
