import networkx as nx

class Graph:
    def __init__(self, name):
        self.name = name
        self.G = nx.Graph()
    def addNode(self, node):
        self.G.add_node(node)
        print(node + " added to Graph " + self.name)
    def addEdge(self, edge):
        print(edge + " added to Graph " + self.name)
    def showGraph(self):
        import matplotlib.pyplot as plt
        options = {
            "font_size": 10,
            "node_size": 6000,
            "node_color": "blue",
            "edgecolors": "black",
            "linewidths": 3,
            "width": 2,
        }
        nx.draw_networkx(self.G, **options)

        # Set margins for the axes so that nodes aren"t clipped
        ax = plt.gca()
        ax.margins(0.20)
        plt.axis("off")
        plt.show()