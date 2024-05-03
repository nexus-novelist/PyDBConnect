import os
import json

from dotenv import load_dotenv, find_dotenv

from fastapi import FastAPI, HTTPException, status

from encryption import *
from utils import *

print(find_dotenv())
#load_dotenv(find_dotenv())
load_dotenv(os.path.abspath(os.getcwd() + os.sep + os.pardir + os.sep + '.env'))

print(os.path.abspath(os.getcwd() + os.sep + os.pardir + os.sep + '.env'))
os.path.abspath

app = FastAPI()

def check_password(input):
    if decrypt('../auth.bin') == input:
        return True
    return False

@app.get('/')
def is_online():
    raise HTTPException(status_code=status.HTTP_200_OK, detail='PyDBConnect Database Server is online!')

# Returns collections of specified project
@app.get('/get/{project}/{password}')
def get_project(project: str, password: str):
    if not check_password(password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Incorrect password!")
    project_dir = os.getcwd() + '/../data/' + project + '/'
    if os.path.exists(project_dir):
        return get_collections(project_dir)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Project not found!')

#returns specified collection of project.
@app.get('/get/{project}/{collection}/{password}')
def get_collection(project: str, collection: str, password: str):
    if not check_password(password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Incorrect password!")
    project_dir = os.getcwd() + '/../data/' + project + '/'
    if os.path.exists(project_dir) and os.path.exists(project_dir + collection + '.json'):
        return json.load(open(project_dir + collection + '.json'))
        
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Project or collection not found!')

#returns specified document of collection.
@app.get('/get/{project}/{collection}/{document}/{password}')
def get_document(project: str, collection: str, document: str, password: str):
    if not check_password(password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Incorrect password!")
    project_dir = os.getcwd() + '/../data/' + project + '/'
    if os.path.exists(project_dir) and os.path.exists(project_dir + collection + '.json'):
        data = json.load(open(project_dir + collection + '.json'))
        if document in data:
            return data[document]
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Document not found in collection!')
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Project or collection not found!')
    
#creates a new document in specified collection
@app.post('/create-document/{project}/{collection}/{document_id}/{password}')
def create_document(project: str, collection: str, document_id: str, document: dict, password: str):
    if not check_password(password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Incorrect password!")
    project_dir = os.getcwd() + '/../data/' + project + '/'
    if os.path.exists(project_dir) and os.path.exists(project_dir + collection + '.json'):
        current_collection = json.load(open(project_dir + collection + '.json'))
        
        if document_id in current_collection:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='specified document_id not found in collection!')

        current_collection[document_id] = document

        with open(project_dir + collection + '.json', 'w') as file:
            json.dump(current_collection, file, indent=4)

        return current_collection[document_id]
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Project or collection not found!')

@app.put('/update-document/{project}/{collection}/{document_id}/{password}')
def update_document(project: str, collection: str, document_id: str, document: dict, password: str):
    if not check_password(password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Incorrect password!")
    project_dir = os.getcwd() + '/../data/' + project + '/'
    if os.path.exists(project_dir) and os.path.exists(project_dir + collection + '.json'):
        current_collection = json.load(open(project_dir + collection + '.json'))

        if not document_id in current_collection:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='specified document_id not found in collection!')

        current_collection[document_id] = document

        with open(project_dir + collection + '.json', 'w') as file:
            json.dump(current_collection, file, indent=4)

        return current_collection[document_id]
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Project or collection not found!')
    
@app.delete('/delete-document/{project}/{collection}/{document_id}/{password}')
def delete_document(project: str, collection: str, document_id: str, password: str):
    if not check_password(password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Incorrect password!")
    project_dir = os.getcwd() + '/../data/' + project + '/'
    if os.path.exists(project_dir) and os.path.exists(project_dir + collection + '.json'):
        current_collection = json.load(open(project_dir + collection + '.json'))

        if not document_id in current_collection:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='specified document_id not found in collection!')

        del current_collection[document_id]

        with open(project_dir + collection + '.json', 'w') as file:
            json.dump(current_collection, file, indent=4)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Project or collection not found!')

@app.post('/create-collection/{project}/{collection}/{password}')
def create_collection(project: str, collection: str, password: str):
    if not check_password(password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Incorrect password!")
    project_dir = os.getcwd() + '/../data/' + project + '/'
    if os.path.exists(project_dir):
        if os.path.exists(project_dir + collection + '.json'):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Collection already exists!')
        
        with open(project_dir + collection + '.json', 'w') as file:
            json.dump({}, file, indent=4)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Project not found!')

@app.delete('/delete-collection/{project}/{collection}/{password}')
def delete_collection(project: str, collection: str, password: str):
    if not check_password(password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Incorrect password!")
    project_dir = os.getcwd() + '/../data/' + project + '/'
    if os.path.exists(project_dir) and os.path.exists(project_dir + collection + '.json'):
        os.remove(project_dir + collection + '.json')
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Project or collection not found!')