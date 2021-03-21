from app import api

from app.resources.login import LoginResource
from app.resources.account import AccountResource
from app.resources.todolists import TodolistsResource
from app.resources.todolistId import TodolistIdResource
from app.resources.todolistIdTodo import TodolistIdTodoResource
from app.resources.todolistIdTodoId import TodolistIdTodoIdResource


# Account
api.add_resource(AccountResource, '/api/account')

# Login
api.add_resource(LoginResource, '/api/login')

# Todos app
api.add_resource(TodolistsResource, '/api/lists')
api.add_resource(TodolistIdResource, '/api/lists/<int:list_id>')
api.add_resource(TodolistIdTodoResource, '/api/lists/todos/<int:list_id>')
api.add_resource(TodolistIdTodoIdResource, '/api/lists/todos/<int:list_id>/<int:todo_id>')

