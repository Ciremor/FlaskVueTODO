from flask import request
from flask_restful import Resource, reqparse, abort
from typing import Dict, List, Any
import json

import jwt
import os
from app import config


class TodolistsResource(Resource):
    def get(self):
        """ 
        Return all todolists
        ---
        tags: 
            - Flask API
        responses : 
            200:
                description : todolists
        """
        token = request.headers.get('token','')
        auth_token = jwt.decode(token,config.API_KEY,algorithms=["HS256"]).get('pseudo')
        
        with open('app/services/' + auth_token + '/todolistsService.json', 'r') as fichier:
            TODOLISTS = json.load(fichier)

        response = {
            'status': 200,
            'message': 'Successful get TODOLISTS',
            'data': TODOLISTS
        }
        return response, 200

    def put(self):
        """
        Add a new list
        ---
        tags: 
          - Flask API
        parameters:
          - in: body
            name: attributes
            description: The name and creation date of the list to create
            schema:
                type: object
                required:
                    -name
                    -created_at
                properties:
                    name:
                        type: string
                    created_at:
                        type: string
        responses:
            201:
                description: JSON representing created todolist
            400:
                decription: The Parameter are missing or not correct
        """
        token = request.headers.get('token','')
        auth_token = jwt.decode(token,config.API_KEY,algorithms=["HS256"]).get('pseudo')

        body_parser = reqparse.RequestParser(bundle_errors = True)
        body_parser.add_argument('name', type=str, required = True, help='Missing the name of the list')
        body_parser.add_argument('created_at', type=str, required = True, help='Missing the date of the list')
        args = body_parser.parse_args(strict=True)
        try:
            name = args['name']
            created_at = args['created_at']
            todolist = {'name': name, 'created_at':created_at, 'list':[]}
            with open('app/services/' + auth_token + '/todolistsService.json', 'r') as fichier:
                TODOLISTS = json.load(fichier)
            TODOLISTS.append(todolist)
            with open('app/services/' + auth_token + '/todolistsService.json', 'w') as fichier:
                json.dump(TODOLISTS, fichier, indent=4)
            response = {
                'status': 201,
                'message': 'Successful put TODOLISTS',
                'data': TODOLISTS
            }
            return response, 201
        except:
            abort(400)
