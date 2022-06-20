# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

import requests, json
import pandas as pd

import graph
import graph_cyto
import networkx as nx

token = "secret_n3wKS4kZdgUsy4OhKC8cF70SFIp6G0gEM1i0DzRNAJe"
databaseId_themes = "7c8039943a144836948a5a4f1fb8baf5"
databaseId_activities = "87544933f6924c55826e22418a647adf"
headers = {
    "Accept": "application/json",
    "Authorization": "Bearer " + token,
    "Content-Type": "application/json",
    "Notion-Version": "2021-08-16"
}

def readDatabase(databaseId, name, headers):
    readUrl = f"https://api.notion.com/v1/databases/{databaseId}/query"
    res = requests.request("POST", readUrl, headers=headers)
    data = res.json()
    str_f_json = "./" + name + ".json"
    with open(str_f_json, "w", encoding="utf8") as f:
        json.dump(data, f, ensure_ascii=False)

def analyzeThemes():
    f = open("./themes.json")
    data = json.load(f)
    res = data["results"]
    for page in res:
        name = page["properties"]["Name"]["title"][0]["text"]["content"]
        id = page["id"]
        g.addNode(id, name)
    for page in res:
        relations2activities = page["properties"]["Related to Themes (Property)"]["relation"]
        id = page["id"]
        for rel in relations2activities:
            g.addEdge(id, rel["id"])

def getThemeById(relationId):
    readUrl = f"https://api.notion.com/v1/pages/{relationId}"
    res = requests.request("GET", readUrl, headers=headers)
    data = res.json()
    activity_title = data["properties"]["Name"]["title"][0]["text"]["content"]
    return activity_title

def getActivityByRelation(relationId):
    readUrl = f"https://api.notion.com/v1/pages/{relationId}"
    res = requests.request("GET", readUrl, headers=headers)
    data = res.json()
    activity_title = data["properties"]["Activity (Project etc.)"]["title"][0]["text"]["content"]
    return activity_title

g = graph_cyto.Graph("MeinGraph")

#edges = g.getEdges()

readDatabase(databaseId_themes, "themes", headers)
analyzeThemes()
#getActivityByRelation("6425a1b5-35f1-4fec-939f-fb13f94dc56c")
g.writeGraph()
myGraph = g.getNetworkXGraph()
print(myGraph.degree['f66f1840-084d-4fd6-b615-35b84f9a0a8e'])
for e, datadict in myGraph.nodes.items():
    print (e, datadict, myGraph.degree[e])
#nodes = g.getNodes()
#g.showGraph()
