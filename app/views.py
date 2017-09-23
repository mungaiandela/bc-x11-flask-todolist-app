from flask import jsonfiy, request
from flask_restful import Resource

from ..models import {
    db, User, Todo
}

class TasksResource(Resource):

    def get(self):
        tasks = Todo.query.filter_by(title=task_name)


    def post(self):

        task = request.get_json()
        search_task = Todo.query_filter_by(title=task.get('task_name')).first()
