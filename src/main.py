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

@app.get('/get/{project}/{cluster}')
def get_cluster(project: str, cluster: str):
    project_dir = os.getcwd() + '/../data/' + project + '/'
    if os.path.exists(project_dir) and os.path.exists(project_dir + cluster + '.json'):
        return json.load(open(project_dir + cluster + '.json'))
        
    return {'Data': None, 'ErrorMsg': 'Project or Cluster not found!', 'ErrorCode': 404}
