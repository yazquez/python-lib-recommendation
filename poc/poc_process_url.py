import re
import uuid
import nltk
import os
from pymongo import MongoClient
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer




MIN_STARTS = 10
URL_PATTERN = 'https://api.github.com/search/repositories?q=language:Python+created:{0}+stars:>={1}&type=Repositories'

CLONE_COMMAND = "git clone {0} {1}"
ROOT_PATH = "d:/tfm/tmp"

LIBRARY_PATTERN = '(?m)^(?:from[ ]+(\S+)[ ]+)?import[ ]+([\S,\s]+)(\n)$'
FILE_LANGUAGE_EXTENSION = ".py"


def get_repository_library():
    client = MongoClient('localhost', 27017)
    db = client.tfm_poc
    return db.library


def get_words(text):
    def add_word(word):
        word = word.lower()
        if word not in stop_words and not word.replace('.', '').isdigit():
            words.append(stemmer.stem(word))

    words = []
    for chunk in nltk.ne_chunk(nltk.pos_tag(tokenizer.tokenize(text))):
        # nltk.word_tokenize    devuelve la lista de palabras que forman la frase (tokenización)
        # nltk.pos_tag          devuelve el part of speech (categoría) correspondiente a la palabra introducida
        # nltk.ne_chunk         devuelve la etiqueta correspondiente al part of speech (POC)
        try:
            if chunk.label() == 'PERSON':
                # PERSON es un POC asociado a los nombres propios, los cuales no vamos a añadir
                pass
            else:
                for c in chunk.leaves():
                    add_word(c[0])
        except AttributeError:
            add_word(chunk[0])

    return words

def process_readme_file(project, file_path):
    with open(file_path, 'r') as f:
        project['readme_txt'] = f.read()


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



def proccess_url(git_url):
    project = dict()
    os.chdir(ROOT_PATH)
    #dir_name = uuid.uuid4().hex
    dir_name = 'aca231c613ff4f6d8cfa240c6157b10e'
    path = ROOT_PATH + "/" + dir_name

    if os.path.isdir(path):
        #os.system(CLONE_COMMAND.format(git_url, dir_name))
        project['git_url'] = git_url
        project['library'] = []
        project['library_lines'] = []
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
        project['readme_words'] = get_words(project['readme_txt'])
        project['library'] = process_library(project['library'])
        project['pipeline_status'] = 'DONE'

    return project


tokenizer = RegexpTokenizer(r'\w+')
stop_words = set(stopwords.words('english'))
stemmer = SnowballStemmer("english")


sample_project = proccess_url("https://github.com/yazquez/programmable-agents_tensorflow.git")

sample_project


#
#
# for project in repository_projects.find({'pipeline_status':'CLONED'}):
#     try:
#         path = ROOT_PATH + "/" + str(project["id"])
#         if os.path.isdir(path):
#             print("Processing project", project["name"])
#             for root, dirs, files in os.walk(path):
#                 for file in files:
#                     try:
#                         if file.endswith(FILE_LANGUAGE_EXTENSION):
#                             process_python_file(project, os.path.join(root, file))
#                         else:
#                             if file.lower().startswith("readme."):
#                                 process_readme_file(project, os.path.join(root, file))
#                     except:
#                         pass
#             project['pipeline_status'] = 'PROCESSED'
#             repository_projects.update({'_id': project['_id']}, {"$set": project}, upsert=False)
#     except:
#         print("Error procesing project {0} [{1}] - {2}".format(project['id'], project['name'], sys.exc_info()[0]))