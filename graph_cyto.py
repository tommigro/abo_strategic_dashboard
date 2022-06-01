import dash
import dash_cytoscape as cyto
from dash import html
from dash.dependencies import Input, Output, State
from dash import dcc
import json
cyto.load_extra_layouts()
class Graph:
    def __init__(self, name):

        self.name = name
        self.app = dash.Dash(__name__)
        self.nodes = []

    def addNode(self, id, label):
        self.nodes.append({"data":{"id":id, "label":label}})
    def addEdge(self, source, target):
        self.nodes.append({"data":{"source":source, "target":target}})
    def showGraph(self):
        default_stylesheet = [
            {
                "selector": "node",
                "style": {
                    "width": "100%",
                    "height": "350px",
                    "content": "data(label)",
                    "font-size": "20px",
                    "text-valign": "center",
                    "text-halign": "center",
                }
            }
        ]
        self.app.layout = html.Div([
            cyto.Cytoscape(
                id="cytoscape-layout-1",
                elements=self.nodes,
                style={"width": "100%", "height": "1200px"},
                layout={
                    "name": "breadthfirst",
                    'roots': '[label = "License Management"]'
                },
                stylesheet=[{
                    "selector":"node",
                    "style":{
                        "font-size":"20px",
                        "color":"black",
                        "content":"data(label)",
                        "width":"10",
                        "height":"10"
                    }
                },
                {
                    "selector":"edge",
                    "style":{
                        "width":1
                    }
                }
                ]
            )
        ])

        self.app.run_server(debug=True)

    def writeGraph(self):
        json_complete = {"elements":str(self.nodes)[1:-1]}
        str_f_json = "./graph.json"
        with open(str_f_json, "w", encoding="utf8") as f:
            json.dump(json_complete, f, ensure_ascii=False)