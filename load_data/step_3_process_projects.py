import os
from pymongo import MongoClient
import re
import sys

ROOT_PATH = "d:/tfm/tfm_process"

LIBRARY_PATTERN = '(?m)^(?:from[ ]+(\S+)[ ]+)?import[ ]+(\S+)(?:[ ]+as[ ]+\S+)?[ ]*$'
FILE_LANGUAGE_EXTENSION = ".py"


def get_repository_projects():
    client = MongoClient('localhost', 27017)
    # db = client.github_t5
    db = client.tfm_data
    return db.projects


def process_python_file(project, file_path):
    def process_expression(item):
        def insert(lib):
            lib = lib.strip()
            if '.' in lib:
                # Solo nos quedamos con el paquete principal
                lib = lib.split('.')[0]
            if not lib in library:
                library.append(lib)

        if not item.startswith('.'):
            if ',' in item:
                [insert(lib) for lib in item.split(',')]
            elif " as " in item:
                insert(item.split(" as ")[0])
            else:
                insert(item)

    library = project['library']
    library_lines = project['library_lines']

    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            match = re.search(LIBRARY_PATTERN, line)
            if match:
                library_lines.append(line)
                if match.group(1) != None:
                    process_expression(match.group(1))
                else:
                    process_expression(match.group(2))

    project['library'] = library
    project['library_lines'] = library_lines


def process_readme_file(project, file_path):
    with open(file_path, 'r') as f:
        project['readme_txt'] = f.read()


repository_projects = get_repository_projects()

if not os.path.isdir(ROOT_PATH):
    print("Root path does not exist")
    exit(0)

for project in repository_projects.find({'pipeline_status': 'CLONED'}):
    try:
        path = ROOT_PATH + "/" + str(project["id"])
        if os.path.isdir(path):
            print("Processing project", project["name"])
            for root, dirs, files in os.walk(path):
                for file in files:
                    try:
                        if file.endswith(FILE_LANGUAGE_EXTENSION):
                            process_python_file(project, os.path.join(root, file))
                        else:
                            if file.lower().startswith("readme."):
                                process_readme_file(project, os.path.join(root, file))
                    except:
                        pass
            project['pipeline_status'] = 'PROCESSED'
            repository_projects.update({'_id': project['_id']}, {"$set": project}, upsert=False)
        else:
            project['pipeline_status'] = 'INITIAL'
            repository_projects.update({'_id': project['_id']}, {"$set": project}, upsert=False)
    except:
        print("Error procesing project {0} [{1}] - {2}".format(project['id'], project['name'], sys.exc_info()[0]))
