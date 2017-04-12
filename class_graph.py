class graph():
    def __init__(self, node_list, edge_list, node_weights):
        self.nodes = set(node_list)
        self.original_num_node = len(self.nodes)
        self.node_weights = node_weights
        self.edges = set(edge_list)
        self.calcuate_neighbours()
        self.calculate_edge_weights()

    def add_node(self, index, node_weight=0):

        self.nodes.add(index)
        self.node_weights[index] = node_weight

    def add_edge(self, start, end, edge_weight=0):

        self.edges.add((start,end))
        self.edge_weights[(start,end)]= edge_weight

    def del_node(self, node):

        # remove all edges attached to that node first.
        for neighbour in self.neighbours[node]:
            self.del_edge((node, neighbour))
            # Not needed for dummies:
            #self.del_edge((neighbour, node))

        # remove the node and its weight:
        self.nodes.remove(node)
        del self.node_weights[node]

    def del_edge(self, edge):

        #remove the edge and its weight:
        self.edges.remove(edge)
        del self.edge_weights[edge]

    def dummy_index(self, index):

        return self.original_num_node + index


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

    def calculate_diameter():
        pass

    def add_dummy(self, vertex, vertex_model):

        s = self.dummy_index(vertex)

        self.add_node(s, 0)

        for v in vertex_model:
            self.add_edge((s,v), 0)

        return s

    def del_dummies(self):

        dummies_list = [v if v >= self.original_num_node for v in self.nodes]

        for dummy in dummies:
            self.del_node(dummy)
