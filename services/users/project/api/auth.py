# services/users/project/api/auth.py

from flask_restful import Resource, Api
from flask import Blueprint, request

from project.api.models import User
from project import db


auth_blueprint = Blueprint('auth', __name__)
api = Api(auth_blueprint)


class Auth(Resource):
    """
    User Registration Resource
    """
    def post(self):
        # get the post data
        post_data = request.get_json()
        response_object = {
            'status': 'fail',
            'message': 'Invalid payload.'
        }
        if not post_data.get('username'):
            return response_object, 400
        if not post_data.get('email'):
            return response_object, 400
        if not post_data.get('password'):
            return response_object, 400

        # check if user already exists
        user = User.query.filter_by(email=post_data.get('email')).first()
        un = User.query.filter_by(username=post_data.get('username')).first()
        if not user and not un:
            try:
                user = User(
                    username=post_data.get('username'),
                    email=post_data.get('email'),
                    password=post_data.get('password')
                )
                # insert the user
                db.session.add(user)
                db.session.commit()
                # generate the auth token
                auth_token = user.encode_auth_token(user.id)
                responseObject = {
                    'status': 'success',
                    'message': 'Successfully registered.',
                    'auth_token': auth_token.decode()
                }
                return responseObject, 201
            except ValueError:
                responseObject = {
                    'status': 'fail',
                    'message': 'Some error occurred. Please try again.'
                }
                return responseObject, 401
        else:
            responseObject = {
                'status': 'fail',
                'message': 'Sorry. That user already exists.',
            }
            return responseObject, 400


api.add_resource(Auth, '/auth/register')
