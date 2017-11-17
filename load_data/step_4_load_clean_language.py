from pymongo import MongoClient
from langdetect import detect


def get_repository_projects():
    client = MongoClient('localhost', 27017)
    # db = client.github_t5
    db = client.tfm_data
    return db.projects


def detect_language(project):
    language = None
    try:
        if len(project['readme_txt']):
            language = detect(project['readme_txt'])
    except:
        pass
    return (language)


repository_projects = get_repository_projects()

projects_not_english = [project for project in list(repository_projects.find()) if detect_language(project) != 'en']


print("English proyects number  :", len(projects_not_english))
print("Total number of proyects :", repository_projects.count() )


# for project in projects_not_english:
#     repository_projects.delete_one({'id': project["id"]})

print("Total number of proyects :", repository_projects.count() )