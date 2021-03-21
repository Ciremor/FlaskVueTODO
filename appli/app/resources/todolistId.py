from flask import request
from flask_restful import Resource, reqparse, abort
from typing import Dict, List, Any


import json
import os
import jwt
from app import config

class TodolistIdResource(Resource):
    def get(self, list_id:int):
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
        responses : 
            201:
                description : All elements in todolist
            404: 
                description: The todolist does not exist
        """
        token = request.headers.get('token','')
        auth_token = jwt.decode(token,config.API_KEY,algorithms=["HS256"]).get('pseudo')
        with open('app/services/' + auth_token + '/todolistsService.json', 'r') as fichier:
            TODOLISTS = json.load(fichier)
        if len(TODOLISTS) <= list_id:
            abort(404, message="list_id doesn't exist", data=list_id)
        response = {
            'status' : 200,
            'message':'Get successful',
            'data':TODOLISTS[list_id]
        }              
        return response
    
    def delete(self, list_id: int):
        """
        Delete a todolist
        ---
        tags: 
            - Flask API
        parameters:
            - in: path
              name: list_id
              description: The id of the todolist to delete
              required: true
              schema:
                type: integer
                minimum: 1
        responses:
            200:
                description: JSON representing the todolists
            404: 
                description: The todolist does not exist
        """
        token = request.headers.get('token','')
        auth_token = jwt.decode(token,config.API_KEY,algorithms=["HS256"]).get('pseudo')
        with open('app/services/' + auth_token + '/todolistsService.json', 'r') as fichier:
            TODOLISTS = json.load(fichier)
        if len(TODOLISTS) <= list_id:
            abort(404, message="list_id doesn't exist", data=list_id)
        del TODOLISTS[list_id]
        with open('app/services/' + auth_token + '/todolistsService.json', 'w') as fichier:
            json.dump(TODOLISTS, fichier, indent=4)  
        response = {
            'status' : 200,
            'message':'Delete successful',
            'data':TODOLISTS
        } 
        return response

    def patch(self, list_id:int):
        """
        Edit a todolist
        ---
        tags: 
            - Flask API
        parameters:
            - in: path
              name: list_id
              description: The id of the list to edit
              required: true
              schema:
                type: integer
                minimum: 1
            - in: body
              name: attribute
              description : The edited name of the todolist
              schema: 
                type: object
                properties: 
                    name: 
                        type: string
        responses:
            201:
                description: JSON representing edited todolist
            400: 
                description: The paramaters ars missing or are not correct
            404:
                description: The list does not exist
        """
        token = request.headers.get('token','')
        auth_token = jwt.decode(token,config.API_KEY,algorithms=["HS256"]).get('pseudo')

        body_parser = reqparse.RequestParser(bundle_errors = True)
        body_parser.add_argument('name', type = str, required = True, help='Missing the name of the list')
        args = body_parser.parse_args(strict=True)
        try:
            with open('app/services/' + auth_token + '/todolistsService.json', 'r') as fichier:
                TODOLISTS = json.load(fichier)
            if len(TODOLISTS) <= list_id:
                abort(404, message="list_id doesn't exist", data=list_id)
            name = args['name']
            TODOLISTS[list_id]['name'] = name
            with open('app/services/' + auth_token + '/todolistsService.json', 'w') as fichier:
                json.dump(TODOLISTS, fichier, indent=4)   
            response = {
                'status' : 202,
                'message':'Patch successful',
                'data':TODOLISTS[list_id]
            }            
            return response
        except:
            abort(400, message = 'Error patch list', data = '')
