from flask import Flask, request
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)

# In-memory storage for tasks
tasks = [
    {
        "id": 1,
        "title": "Team Meeting Preparation",
        "description": "Prepare the agenda for the team meeting scheduled for Friday.",
        "status": "In Progress"
    },
    {
        "id": 2,
        "title": "Code Review",
        "description": "Review the pull requests submitted by the team and provide feedback.",
        "status": "Pending"
    },
    {
        "id": 3,
        "title": "Update Project Documentation",
        "description": "Update the project documentation with the latest architectural changes.",
        "status": "Completed"
    }
]

class Task(Resource):
    def get(self, task_id):
        # Retrieve a specific task by ID
        task = next((task for task in tasks if task['id'] == task_id), None)
        if task:
            # Return the entire task data as a JSON object
            return {
                'id': task['id'],
                'title': task['title'],
                'description': task['description'],
                'status': task['status']
            }, 200
        return {"message": "Task not found"}, 404

    def put(self, task_id):
        # Update a task by ID
        data = request.get_json()
        task = next((task for task in tasks if task['id'] == task_id), None)
        if task:
            task.update({
                'title': data['title'],
                'description': data.get('description', ''),
                'status': data.get('status', 'Pending')
            })
            return task, 200
        return {"message": "Task not found"}, 404

    def delete(self, task_id):
        # Delete a task by ID
        global tasks
        task = next((task for task in tasks if task['id'] == task_id), None)
        if task:
            tasks = [t for t in tasks if t['id'] != task_id]
            return {"message": "Task deleted"}, 200
        return {"message": "Task not found"}, 404

class TaskList(Resource):
    def get(self):
        # Retrieve all tasks
        return tasks, 200

    def post(self):
        # Create a new task
        data = request.get_json()
        new_task = {
            'id': len(tasks) + 1,  # Simple ID generation
            'title': data['title'],
            'description': data.get('description', ''),
            'status': data.get('status', 'Pending')
        }
        tasks.append(new_task)
        return new_task, 201

# Define API routes
api.add_resource(TaskList, '/tasks')
api.add_resource(Task, '/tasks/<int:task_id>')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
