from flask import json, request
from flask_restful import Resource, reqparse, abort
from typing import Dict, List, Any
import os
from os import listdir,path
from os.path import isfile, join
import json

class AccountResource(Resource):
    def post(self):
        """
        Create an account
        ---
        tags: 
            - Flask API
        parameters:
            - in: body
              name: attribute
              description : The pseudo and the hashed password of the user
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
            201:
                description: Account successfully created
            400: 
                description: Missing or wrong parameters
            404:
                description: No user file to be found
        """
        body_parser = reqparse.RequestParser()
        body_parser.add_argument('pseudo', type = str, required = True, help='Missing the pseudo of the user')
        body_parser.add_argument('password', type = str, required = True, help='Missing the password of the user')
        args= body_parser.parse_args(strict=True)
        try:
            pseudo = args['pseudo']
            password_hash= args['password']

            with open('app/services/todosService.json', 'r') as fichier:
                USERS = json.load(fichier)
                fichier.close

            for user in USERS:
                if(pseudo == user['pseudo'] and password_hash == user['password']):
                    abort(400, message = 'Account already exists', data = pseudo)

            USERS.append({'pseudo': pseudo, 'password': password_hash})

            with open('app/services/todosService.json', 'w') as fichier:
                json.dump(USERS, fichier, indent=4)
                fichier.close

            if not os.path.exists('app/services/' + pseudo):
                os.makedirs('app/services/' + pseudo)

            with open('app/services/' + pseudo + '/todolistsService.json', 'x') as fichier:
                json.dump([], fichier, indent = 4)
                fichier.close

            response = {
                'status': 201,
                'message': 'Successful account creation',
                'data': pseudo
            }
            return (response, 201)

        except (OSError,IOError):
            abort(404, message = 'User files not found', data='')
        else:
            abort(400, message = 'Account Creation Procedure is dead and you killed it', data='')
