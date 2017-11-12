# Este script recorre la colección de proyectos y los clona en un directorio local, verifica que el proyecto aún no haya sido procesado y que el directorio de descarga no exista, este último control se hace por si es neceario reiniciar la descarga en algún momento.
import os
from pymongo import MongoClient

import sklearn

ROOT_PATH = "d:/tfm/tfm_cloned"
CLONE_COMMAND = "git clone {0} {1}"


def get_repository_projects():
    client = MongoClient('localhost', 27017)
    db = client.tfm_data
    return db.projects


os.chdir(ROOT_PATH)
repository_projects = get_repository_projects()

for i in range(0, 1000):
    try:
        for project in repository_projects.find({'pipeline_status': 'INITIAL'}):
            print("Cloning project", project['name'], "...")
            path = ROOT_PATH + "/" + str(project["id"])
            if not os.path.isdir(path):
                os.system(CLONE_COMMAND.format(project["git_url"], project["id"]))
            project['pipeline_status'] = 'CLONED'
            repository_projects.update({'_id': project['_id']}, {"$set": project}, upsert=False)
    except:
        pass
