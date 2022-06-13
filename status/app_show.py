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

@app.route('/show', methods=['POST'])
def read():
    """
        read() : Fetches documents from Firestore collection as JSON.
        todo : Return document that matches query ID.
        all_todos : Return all documents.
    """
    try:
        # Check if ID was passed to URL query
        request = flask.request.get_json()
        todo_current = request['id']
        # if todo_id:
        #     todo = todo_ref.document(todo_id).get()
        #     return jsonify(todo.to_dict()), 200

        alll_todos = [doc.to_dict() for doc in todo_ref.stream()]
        print (alll_todos)
        all_todos = []
        for doc in todo_ref.stream():
            print (doc.id)
            if(doc.id == todo_current):
                continue
            if(doc.to_dict()['online'] == True):
                all_todos.append(doc.to_dict())
        return jsonify(all_todos), 200
    except Exception as e:
        return f"An Error Occurred: {e}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)