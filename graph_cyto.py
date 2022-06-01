import dash
import dash_cytoscape as cyto
import dash_daq as daq
from dash import Dash, dcc, html, Input, Output
from dash.dependencies import Input, Output, State
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

        layout = 'breadthfirst'

        @self.app.callback(
            Output('cytoscape-layout-1', 'layout'),
            Input('demo-dropdown', 'value')
        )
        def update_layout(value):
            if value == 'breadthfirst':
                return {
                    'name': value,
                    'roots': '[label = "License Management"]',
                    'animate': True
                }
            else:
                return {
                    'name': value,
                    'animate': True
                }
        @self.app.callback(
            Output('cytoscape-layout-1', 'stylesheet'),
            Input('font-slider', 'value')
        )
        def update_fontsize(value):
            size = str(value) + 'px'
            return[{
                "selector": "node",
                "style":{
                    "font-size": size,
                    "color": "black",
                    "content": "data(label)",
                    "width": value,
                    "height": value
                }
            }]
        self.app.layout = html.Div([
            dcc.Dropdown(['breadthfirst', 'circle', 'cola', 'concentric', 'cose', 'euler', 'grid', 'random'], 'breadthfirst', id='demo-dropdown'),
            html.Div(id='dd-output-container'),
            daq.Slider(
                id='font-slider',
                min=3,
                max=30,
                value=15,
                handleLabel={"showCurrentValue": True, "label": "VALUE"},
                step=1
            ),
            cyto.Cytoscape(
                id="cytoscape-layout-1",
                elements=self.nodes,
                style={"width": "100%", "height": "1200px"},
                layout={
                    "name": layout,
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