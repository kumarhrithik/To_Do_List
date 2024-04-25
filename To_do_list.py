from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from bson import ObjectId, json_util
import pymongo

app = Flask(__name__)
mongo_client = pymongo.MongoClient("mongo-URI")
db = mongo_client.get_database("to-do-list")
tasks = db.get_collection("to-do-items")

# List Tasks (GET /tasks)
@app.route('/view_all_task', methods=['GET'])
def view_all_task():
    all_tasks = tasks.find()
    items = []
    for data in all_tasks:
        data['_id'] = str(data['_id'])
        items.append(data)
    return jsonify(json_util.dumps(items))

# View Task Details (GET /tasks/<task_id>)
@app.route('/view_task/<string:task_id>', methods=['GET'])
def view_task(task_id):
    task = tasks.find_one({"_id": ObjectId(task_id)})
    if task:
        task['_id'] = str(task['_id'])
        return jsonify(json_util.dumps(task))
    else:
        return jsonify({'message': 'Task not found'})

# Add Task (POST /tasks)
@app.route('/add_task', methods=['POST'])
def add_task():
    data = request.json
    result = tasks.insert_one(data)
    new_task = tasks.find_one({"_id": result.inserted_id})
    new_task['_id'] = str(new_task['_id'])
    return jsonify(json_util.dumps(new_task))

@app.route('/update_task/<string:task_id>', methods=['PUT'])
def update_task(task_id):
    data = request.json
    
    result = tasks.update_one({"_id": ObjectId(task_id)}, {"$set": data})
    if result.modified_count >= 1:
        update_task = tasks.find_one({"_id": ObjectId(task_id)})
        update_task['_id'] = str(update_task['_id'])
        return jsonify(json_util.dumps(update_task))
    else:
        return jsonify({'message': 'Task not found'})
    

@app.route('/delete_task/<string:task_id>', methods=['DELETE'])
def delete_task(task_id):
    result = tasks.delete_one({"_id": ObjectId(task_id)})
    if result.deleted_count >= 1:
        return jsonify({'message': 'Task deleted successfully'})
    else:
        return jsonify({'message': 'Task not found'})

if __name__ == '__main__':
    app.run(debug=True)