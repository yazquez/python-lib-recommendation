from pymongo import MongoClient
import requests
import re

PYPI_LIST_URL = 'https://pypi.python.org/simple/'

def get_repository_library():
    client = MongoClient('localhost', 27017)
    db = client.tfm_data
    return db.library

def insert_library(library_name):
    library_name = library_name.lower()
    if repository_library.find_one({"name": library_name}):
        print("Library {0} is already included in the repository".format(library_name))
    else:
        library = {
            'name': library_name
        }
        repository_library.insert(library)

def show_library(library_name):
    library_name = library_name.lower().replace("-", "_")
    library_name = library_name.lower()
    print(library_name)

repository_library = get_repository_library()

content = requests.get(PYPI_LIST_URL)

for line in content.text.split('\n'):
    match = re.search("'>([\w\-\.]+)", line)
    if match:
        show_library(match.group(1))