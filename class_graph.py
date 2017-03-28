class graph():
    def __init__(self, node_list, edge_list, node_weights):
        self.nodes = set(node_list)
        self.node_weights = node_weights
        self.edges = set(edge_list)
        self.calcuate_neighbours()
        self.calculate_edge_weights()

    def calcuate_neighbours(self):

        self.neighbours = {}

        for vertex in self.nodes:
            self.neighbours[vertex] =[]

        for edge in self.edges:
            self.neighbours[edge[0]].append(edge[1])
            self.neighbours[edge[1]].append(edge[0])

    def calculate_edge_weights(self):
        self.edge_weights = {}

        for edge in self.edges:
            self.edge_weights[edge] = self.node_weights[edge[0]]
            self.edge_weights[(edge[1],edge[0])] = self.node_weights[edge[1]]
