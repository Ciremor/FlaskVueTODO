from flask import request
from flask_restful import Resource, reqparse, abort
import json
from datetime import datetime, timedelta
import jwt
from app import config

class LoginResource(Resource):
    def post(self):
        """
        Login to an account
        ---
        tags: 
            - Flask API
        parameters:
            - in: body
              name: attribute
              description : The username and the hashed password of the user
              schema: 
                type: object
                required:
                    -pseudo
                    -password
                properties: 
                    pseudo: 
                        type: string
                    password:
                        type: string
        responses:
            200:
                description: Account successfully logged in
            400: 
                description: Missing or wrong parameters
            404:
                description: No user file to be found
        """

        body_parser = reqparse.RequestParser()
        body_parser.add_argument('pseudo', type=str, required=True, help="Missing the login of the user")
        body_parser.add_argument('password', type=str, required=True, help="Missing the password associated to the user login")
        args = body_parser.parse_args(strict=True) # Accepted only if these two parameters are strictly declared in body else raise exception

        try:
            pseudo = args['pseudo']
            password_hash = args['password']
            with open('app/services/todosService.json', 'r') as fichier:
                USERS = json.load(fichier)

            for user in USERS:
                if(pseudo == user['pseudo'] and password_hash == user['password']):
                    #token toto : eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwc2V1ZG8iOiJ0b3RvIn0.CUIaDKAVeXRtWvdFdQOT_Sy8icflYoD0CC_--mssJtk
                    token=jwt.encode({"pseudo":pseudo},config.API_KEY,algorithm="HS256")
                    response = {
                        'status': 200,
                        'message': 'Successful authentification',
                        'data': token
                    }
                    return(response, 200)

        except (OSError, IOError, Exception) as e:
            abort(404, message = 'Error No user files to be found', data = '')
            print(e)
        else:
            abort(400, message = 'Account Login Failed', data = '')
            print(e)













