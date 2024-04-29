import os

def get_collections(project_dir):
    result = []
    for f in os.listdir(project_dir):
        if f.endswith('.json'):
            result.append(f[:-5])
    return result