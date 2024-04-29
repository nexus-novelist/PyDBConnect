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

# Returns collections of specified project
@app.get('/get/{project}')
def get_project(project: str):
    project_dir = os.getcwd() + '/../data/' + project + '/'
    if os.path.exists(project_dir):
        return os.listdir(project_dir)
    else:
        return {'Data': None, 'ErrorMsg': 'Project not found!', 'ErrorCode': 404}

#returns specified collection of project.
@app.get('/get/{project}/{collection}')
def get_collection(project: str, collection: str):
    project_dir = os.getcwd() + '/../data/' + project + '/'
    if os.path.exists(project_dir) and os.path.exists(project_dir + collection + '.json'):
        return json.load(open(project_dir + collection + '.json'))
        
    return {'Data': None, 'ErrorMsg': 'Project or Collection not found!', 'ErrorCode': 404}

#returns specified document of collection.
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
    
#creates a new document in specified collection
@app.post('/create-document/{project}/{collection}/{document_id}')
def create_document(project: str, collection: str, document_id: str, document: dict):
    project_dir = os.getcwd() + '/../data/' + project + '/'
    if os.path.exists(project_dir) and os.path.exists(project_dir + collection + '.json'):
        current_collection = json.load(open(project_dir + collection + '.json'))
        
        if document_id in current_collection:
            return {'Data': None, 'ErrorMsg': 'Document with the same document_id already exists in collection!', 'ErrorCode': 409}

        current_collection[document_id] = document

        with open(project_dir + collection + '.json', 'w') as file:
            json.dump(current_collection, file, indent=4)

        return current_collection[document_id]
    else:
        return {'Data': None, 'ErrorMsg': 'Project or Collection not found!', 'ErrorCode': 404}

@app.put('/update-document/{project}/{collection}/{document_id}')
def update_document(project: str, collection: str, document_id: str, document: dict):
    project_dir = os.getcwd() + '/../data/' + project + '/'
    if os.path.exists(project_dir) and os.path.exists(project_dir + collection + '.json'):
        current_collection = json.load(open(project_dir + collection + '.json'))

        if not document_id in current_collection:
            return {'Data': None, 'ErrorMsg': 'specified document_id not found in collection!', 'ErrorCode': 404}

        current_collection[document_id] = document

        with open(project_dir + collection + '.json', 'w') as file:
            json.dump(current_collection, file, indent=4)

        return current_collection[document_id]
    else:
        return {'Data': None, 'ErrorMsg': 'Project or Collection not found!', 'ErrorCode': 404}

@app.delete('/delete-document/{project}/{collection}/{document_id}')
def delete_document(project: str, collection: str, document_id: str):
    project_dir = os.getcwd() + '/../data/' + project + '/'
    if os.path.exists(project_dir) and os.path.exists(project_dir + collection + '.json'):
        current_collection = json.load(open(project_dir + collection + '.json'))

        if not document_id in current_collection:
            return {'Data': None, 'ErrorMsg': 'specified document_id not found in collection!', 'ErrorCode': 404}

        del current_collection[document_id]

        with open(project_dir + collection + '.json', 'w') as file:
            json.dump(current_collection, file, indent=4)

        return {'ReturnMsg': 'Document deleted successfully!', 'ReturnCode': 200}
    else:
        return {'Data': None, 'ErrorMsg': 'Project or Collection not found!', 'ErrorCode': 404}