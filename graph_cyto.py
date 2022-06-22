import json

import dash
import dash_cytoscape as cyto
import dash_daq as daq
import networkx as nx
from dash import dcc, html
from dash.dependencies import Input, Output

cyto.load_extra_layouts()



class Graph:

    def __init__(self, name):
        self.name = name
        self.app = dash.Dash(__name__)
        self.nodes = []
        self.G = nx.Graph()

    def addNode(self, id, label):
        self.nodes.append({"data":{"id":id, "label":label}})
        self.G.add_node(id, label=label)
    def addEdge(self, source, target):
        self.nodes.append({"data":{"source":source, "target":target}})
        self.G.add_edge(source, target)
    def showGraph(self):

        layout = 'breadthfirst'
        degree = 0

        @self.app.callback(
            Output('cytoscape-layout-1', 'layout'),
            Input('method', 'value'),
            Input('topic', 'value')
        )
        def update_layout(method, topic):
            ctx = dash.callback_context
            input = ctx.triggered_id
            if input == 'method':
                if method == 'breadthfirst':
                    return {
                        'name': method,
                        'roots': '[label = "License Management"]',
                        'animate': True
                    }
                else:
                    return {
                        'name': method,
                        'animate': True
                    }
            elif input == 'topic':
                return{
                    'name': 'breadthfirst',
                    'roots': '[label = "' + topic + '"]',
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

        @self.app.callback(
            Output('degree', 'value'),
            Input('topic', 'value')
        )
        def update_degree(value):
            print(value)
            node = [x for x, y in self.G.nodes(data=True) if y['label'] == value]
            degree = nx.degree(self.G, node[0])
            return 'Degree: ' + str(degree)

        self.app.layout = html.Div([
            dcc.Dropdown(['breadthfirst', 'circle', 'cola', 'concentric', 'cose', 'euler', 'grid', 'random'], 'breadthfirst', id='method'),
            dcc.Dropdown([datadict['label'] for e, datadict in self.G.nodes.items()],'License Management', id='topic'),
            daq.Slider(
                id='font-slider',
                min=3,
                max=30,
                value=15,
                handleLabel={"showCurrentValue": True, "label": "VALUE"},
                step=1
            ),
            dcc.Textarea(
                id='degree',
                value='degree',
                style={'width': '30%', 'height': 20},
            ),
            cyto.Cytoscape(
                id="cytoscape-layout-1",
                elements=self.nodes,
                style={"width": "100%", "height": "1200px"},
                layout={
                    "name": layout,
                    'roots': '[label = "Internationalization"]'
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

        self.app.run_server(host='0.0.0.0', port=8080, debug=True)

    def writeGraph(self):
        json_complete = {"elements":str(self.nodes)[1:-1]}
        str_f_json = "./graph.json"
        with open(str_f_json, "w", encoding="utf8") as f:
            json.dump(json_complete, f, ensure_ascii=False)

    def getNetworkXGraph(self):
        return self.G
