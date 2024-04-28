import os
import json

from fastapi import FastAPI

app = FastAPI()
#Types of APIs
#GET: returns information
#POST: creates something new
#PUT: updates something
#DELETE: deletes something

@app.get('/')
def is_online():
    return {'online': True}

@app.get('/get/{project}/{collection}')
def get_collection(project: str, collection: str):
    project_dir = os.getcwd() + '/../data/' + project + '/'
    if os.path.exists(project_dir) and os.path.exists(project_dir + collection + '.json'):
        return json.load(open(project_dir + collection + '.json'))
        
    return {'Data': None, 'ErrorMsg': 'Project or Collection not found!', 'ErrorCode': 404}

@app.get('/get/{project}/{collection}/{document}')
def get_document(project: str, collection: str, document: str):
    project_dir = os.getcwd() + '/../data/' + project + '/'
    if os.path.exists(project_dir) and os.path.exists(project_dir + collection + '.json'):
        data = json.load(open(project_dir + collection + '.json'))
        if document in data:
            return data[document]
        else:
            return {'Data': None, 'ErrorMsg': 'Document not found!', 'ErrorCode': 404}
    else:
        return {'Data': None, 'ErrorMsg': 'Project or Collection not found!', 'ErrorCode': 404}