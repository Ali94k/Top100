import requests
import json
from requests.auth import HTTPBasicAuth
from collections import defaultdict

class GitHubAPI:
    id: int
    node_id: str
    name: str
    full_name: str
    private: bool
    html_url: str
    description: str
    stargazers_count: int
    language: str

    def __init__(self, id: int, node_id: str, name: str, full_name: str, private: bool, html_url: str, description: str, stargazers_count: int, language: str) -> None:
        self.id = id
        self.node_id = node_id
        self.name = name
        self.full_name = full_name
        self.private = private
        self.html_url = html_url
        self.description = description
        self.stargazers_count = stargazers_count
        self.language = language

def createTable(sectionItems):
    table = []

    sortedItems = sorted(sectionItems, key=lambda k: k.stargazers_count or 0, reverse=True)[:100]

    table.append('|Name|Description|Language|Star count|\n')
    table.append('|---|---|---|---|\n')

    for r in sortedItems:
        try:
            name = f'[{r.name[:20]}]({r.html_url})'
            description = r.description or 'No description'
            description = description.replace('|', '\\')
            table.append(f'|{name}|{description}|{r.language}|{r.stargazers_count}|\n')
        except Exception as ex:
            print(ex)


    return table

sectionItems = list()

i=100
j=1

org = 'SomeOrg'

while i==100:
    try:
        repo =f'https://api.github.com/orgs/{org}/repos?page={j}&per_page={i}'
        r = requests.get(repo, auth=HTTPBasicAuth('UserName', 'Token'))
        if(r.ok):
            items = json.loads(r.text or r.content)
            for t in items:
                sectionItems.append(
                    GitHubAPI(t["id"], t["node_id"], t["name"], t["full_name"], t["private"], 
                    t["html_url"], t["description"], t["stargazers_count"],  t["language"]))
            print(len(items))
            i = len(items)
        else:
            print('not ok', end=' ')
            print(i, end=' ')
    except Exception as ex:
        print(ex)
    print(j)
    j=j+1

with open(f'{org}ReposTop100_1.md', 'w', encoding='utf-8') as f:
    f.writelines(createTable(sectionItems))

