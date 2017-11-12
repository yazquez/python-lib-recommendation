import requests
import json
from time import sleep
from pymongo import MongoClient
from datetime import date, timedelta

MIN_STARTS = 10
START_DATE = date(2012, 1, 1)
END_DATE = date(2017, 10, 31)
URL_PATTERN = 'https://api.github.com/search/repositories?q=language:Python+created:{0}+stars:>={1}&type=Repositories'


def get_repository_projects():
    client = MongoClient('localhost', 27017)
    db = client.tfm_data
    return db.projects


def insert_project(github_project):
    if repository_projects.find_one({"id": github_project["id"]}):
        print("Project {0} is already included in the repository".format(github_project["name"]))
    else:
        project = {
            'id': github_project["id"],
            'name': github_project["name"],
            'full_name': github_project["full_name"],
            'created_at': github_project["created_at"],
            'git_url': github_project["git_url"],
            'description': github_project["description"],
            'language': github_project["language"],
            'stars': github_project["stargazers_count"],
            'readme_txt': "",
            'readme_language': None,
            'readme_words': [],
            'library': [],
            'raw_data': github_project,
            'pipeline_status': 'INITIAL',
            'library_lines': [],
        }
        repository_projects.insert(project)


def get_projects_by_date(date):
    print("Processing date", date)
    url_pattern = URL_PATTERN
    url = url_pattern.format(date, MIN_STARTS)
    response = requests.get(url)
    if (response.ok):
        response_data = json.loads(response.content.decode('utf-8'))['items']
        for project in response_data:
            insert_project(project)
    else:
        response.raise_for_status()


repository_projects = get_repository_projects()

for project_create_at in [START_DATE + timedelta(days=x) for x in range((END_DATE - START_DATE).days + 1)]:
    try:
        get_projects_by_date(project_create_at)
    except:
        print(">> Reached call limit, waiting 61 seconds...")
        sleep(61)
        get_projects_by_date(project_create_at)
