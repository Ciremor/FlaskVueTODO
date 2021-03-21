from flask import request
from flask_restful import Resource, reqparse, abort
from typing import Dict, List, Any

import json
import os
import jwt
from app import config

class TodolistIdTodoResource(Resource):
    def get(self, list_id):
        """ 
        Return todos
        ---
        tags: 
            - Flask API
        parameters:
            - in: path
              name: list_id
              description: The id of the todolist to get
              required: true
              schema:
                type: integer
                minimum: 1
        responses: 
            202:
                description : All elements in todos
            404: 
                description: The list does not exist
        """
        token = request.headers.get('token','')
        auth_token = jwt.decode(token,config.API_KEY,algorithms=["HS256"]).get('pseudo')
        with open('app/services/' + auth_token + '/todolistsService.json', 'r') as fichier:
            TODOLISTS = json.load(fichier)
        if len(TODOLISTS) <= list_id:
            abort(404, message="list_id doesn't exist", data=list_id)        
        response = {
            'status': 200,
            'message': 'Successful GET',
            'data': TODOLISTS[list_id]['list']
        }         
        return response, 200

    def put(self, list_id):
        """
        Add a new task
        ---
        tags: 
          - Flask API
        parameters:
          - in: path
            name: list_id
            description: The id of the todolist to get
            required: true
            schema:
                type: integer
                minimum: 1
          - in: body
            name: attributes
            description: The name, creation date, do state of the task to create
            schema:
                type: object
                required:
                    -name
                    -created_at
                    -do
                properties:
                    name:
                        type: string
                    created_at:
                        type: string
                    do: 
                        type: bool
        responses:
            203:
                description: JSON representing created task
            400:
                decription: The Parameter are missing or not correct
            404:
                description: The list does not exist
        """
        token = request.headers.get('token','')
        auth_token = jwt.decode(token,config.API_KEY,algorithms=["HS256"]).get('pseudo')
        body_parser = reqparse.RequestParser(bundle_errors = True)
        body_parser.add_argument('name', type=str, required = True, help='Missing the name of the task')
        body_parser.add_argument('created_at', type=str, required = True, help='Missing the date of the task')
        body_parser.add_argument('do', type=bool, required = True, help='Missing the state of the task')
        args = body_parser.parse_args(strict=True)
        try:
            with open('app/services/' + auth_token + '/todolistsService.json', 'r') as fichier:
                TODOLISTS = json.load(fichier)
            if len(TODOLISTS) <= list_id:
                abort(404, message="list_id doesn't exist", data=list_id)
            name = args['name']
            created_at = args['created_at']
            do = args['do']
            todo = {'name': name, 'created_at':created_at, 'do':do}
            TODOLISTS[list_id]['list'].append(todo)
            with open('app/services/' + auth_token + '/todolistsService.json', 'w') as fichier:
                json.dump(TODOLISTS, fichier, indent=4)
            response = {
                'status': 201,
                'message': 'Successful PUT',
                'data': todo
            }
            return response, 201
        except:
            abort(400)

