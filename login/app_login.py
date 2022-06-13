# app.py

# Required imports
import os
#from flask import Flask, request, jsonify
from firebase_admin import credentials, firestore, initialize_app

import flask

import requests

from flask import jsonify

# Initialize Flask app
app = flask.Flask(__name__)

# Initialize Firestore DB
cred = credentials.Certificate('key.json')
default_app = initialize_app(cred)
db = firestore.client()
todo_ref = db.collection('todos')

@app.route('/list', methods=['POST'])
def read():
    """
        read() : Fetches documents from Firestore collection as JSON.
        todo : Return document that matches query ID.
        all_todos : Return all documents.
    """
    try:
        # Check if ID was passed to URL query
        request = flask.request.get_json()
        todo_id = request['id']
        todo_password = request['password']
        #todo_id = flask.request.get('id')
        print (todo_id)
        #todo_password = flask.request.args.get('password')
        if todo_id:
            todo = todo_ref.document(todo_id).get()
            user = todo.to_dict()
            if todo_password == user['password']:
                user['online'] = True
                todo_ref.document(todo_id).set(user)
                #todo_ref.document(id).update(newAfterLogin)
                # all_todos = [doc.to_dict() for doc in todo_ref.stream()]
                # for doc in todo_ref.stream():
                #     if doc.online == True:
                #         online_todos = [doc.to_dict() for doc in todo_ref.stream()]
                # print (online_todos)
                #return jsonify(todo.to_dict()), 200
                return jsonify(todo_ref.document(todo_id).get().to_dict()), 200
        else:
            print("inside else")
            return "invalid", 200
    except Exception as e:
        return f"An Error Occurred: {e}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)