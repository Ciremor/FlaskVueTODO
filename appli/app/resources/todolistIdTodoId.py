from flask import request
from flask_restful import Resource, reqparse, abort
from typing import Dict, List, Any
import json
import os
import jwt
from app import config

class TodolistIdTodoIdResource(Resource):
    def get(self, list_id:int, todo_id:int):
        """ 
        Return todolist
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
            - in: path
              name: todo_id
              description: The id of the task to delete
              required: true
              schema:
                type: integer
                minimum: 1
        responses : 
            202:
                description: JSON representing the todos
            404: 
                description: The todolist does not exist
            405: 
                description: The todo does not exist
        """
        token = request.headers.get('token','')
        auth_token = jwt.decode(token,config.API_KEY,algorithms=["HS256"]).get('pseudo')
        with open('app/services/' + auth_token + '/todolistsService.json', 'r') as fichier:
            TODOLISTS = json.load(fichier)
        if len(TODOLISTS) <= list_id:
            abort(404, message="list_id doesn't exist", data=list_id)    
        if len(TODOLISTS[list_id]['list']) <= todo_id:
            abort(405, message="todo_id doesn't exist", data = todo_id)
        response = {
            'status': 200,
            'message': 'Successful get todo',
            'data': TODOLISTS[list_id]['list'][todo_id]
        } 
        return response, 200
    
    def delete(self, list_id: int, todo_id:int):
        """
        Delete a task
        ---
        tags: 
            - Flask API
        parameters:
            - in: path
              name: list_id
              description: The id of the todolist
              required: true
              schema:
                type: integer
                minimum: 1
            - in: path
              name: todo_id
              description: The id of the task to delete
              required: true
              schema:
                type: integer
                minimum: 1
        responses: 
            202:
                description: JSON representing the todos
            404: 
                description: The todolist does not exist
            405: 
                description: The todo does not exist
        """
        token = request.headers.get('token','')
        auth_token = jwt.decode(token,config.API_KEY,algorithms=["HS256"]).get('pseudo')
        with open('app/services/' + auth_token + '/todolistsService.json', 'r') as fichier:
            TODOLISTS = json.load(fichier)
        if len(TODOLISTS) <= list_id:
            abort(404, message="list_id doesn't exist", data=list_id)    
        if len(TODOLISTS[list_id]['list']) <= todo_id:
            abort(405, message="todo_id doesn't exist", data = todo_id)
        del TODOLISTS[list_id]['list'][todo_id]
        with open('app/services/' + auth_token + '/todolistsService.json', 'w') as fichier:
            json.dump(TODOLISTS, fichier, indent=4)
        response = {
            'status': 200,
            'message': 'Successful delete todo',
            'data': TODOLISTS
        }
        return response, 200
    
    def patch(self, list_id:int, todo_id:int):
        """
        Edit a task
        ---
        tags: 
            - Flask API
        parameters:
            - in: path
              name: list_id
              description: The id of the todolist
              required: true
              schema:
                type: integer
                minimum: 1
            - in: path
              name: todo_id
              description: The id of the task to edit
              required: true
              schema:
                type: integer
                minimum: 1
            - in: body
              name: attribute
              description : The edited name of the task
              schema: 
                type: object
                properties: 
                    name: 
                        type: string
                    do: 
                        type: bool
        responses:
            203:
                description: JSON representing edited task
            400: 
                description: The paramaters ars missing or are not correct
            404:
                description: The list does not exist
            405: 
                description: The todo does not exist
        """
        token = request.headers.get('token','')
        auth_token = jwt.decode(token,config.API_KEY,algorithms=["HS256"]).get('pseudo')
        body_parser = reqparse.RequestParser(bundle_errors = True)
        body_parser.add_argument('name', type=str, required = False, help='Missing the name of the task')
        body_parser.add_argument('do', type=bool, required = False, help='Missing the state of the task')
        args = body_parser.parse_args(strict=True)
        try:
            with open('app/services/' + auth_token + '/todolistsService.json', 'r') as fichier:
                TODOLISTS = json.load(fichier)
            if len(TODOLISTS) <= list_id:
                abort(404, message="list_id doesn't exist", data=list_id)  
            if len(TODOLISTS[list_id]['list']) <= todo_id:
                abort(405, message="todo_id doesn't exist", data = todo_id)
            name = args['name']
            do = args['do']
            if name != None:
                TODOLISTS[list_id]['list'][todo_id]['name'] = name
            if do != None:
                TODOLISTS[list_id]['list'][todo_id]['do'] = do
            with open('app/services/' + auth_token + '/todolistsService.json', 'w') as fichier:
                json.dump(TODOLISTS, fichier, indent=4)    
            response = {
                'status': 202,
                'message': 'Successful patch',
                'data': TODOLISTS[list_id]['list'][todo_id]
            }   
            return response, 202
        except:
            abort(400)

