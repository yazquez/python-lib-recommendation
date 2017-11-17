import sys
import nltk
from pymongo import MongoClient
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer

tokenizer = RegexpTokenizer(r'\w+')
stop_words = set(stopwords.words('english'))
stemmer = SnowballStemmer("english")

def get_repository_projects():
    client = MongoClient('localhost', 27017)
    db = client.tfm_data
    return db.projects

def get_repository_library():
    client = MongoClient('localhost', 27017)
    db = client.tfm_data
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

def process_library(library):
    library_processed = []
    for lib in library:
        if repository_library.find_one({"name": lib}):
            library_processed.append(lib)
    return library_processed

repository_projects = get_repository_projects()
repository_library = get_repository_library()

for project in repository_projects.find({'pipeline_status': 'PROCESSED'}):
    try:
        print("Processing",project["name"])
        project['readme_words'] = get_words(project['readme_txt'])
        project['library'] = process_library(project['library'])
        project['pipeline_status'] = 'DONE'

        repository_projects.update({'_id': project['_id']}, {"$set": project}, upsert=False)
    except:
        print("Error procesing project {0} [{1}] - {2}".format(project['id'], project['name'], sys.exc_info()[0]))
        pass


# Finalmente eliminaremos de nuestro repositorio los proyectos que no tienen librerías o que no tienen ningun elemento en su lista de palabras (la descomposición de los ficheros **readme**)

i = 0
for project in repository_projects.find({'pipeline_status': 'DONE'}):
    if len(project['library']) == 0 or len(project['readme_words']) == 0:
        i += 1
        print("Deleting",project["name"])
        repository_projects.delete_one({'id': project["id"]})

print("Projects deleted:", i)

