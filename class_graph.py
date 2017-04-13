from priodict import priorityDictionary

class graph():
    def __init__(self, node_list, edge_list, node_weights):
        self.nodes = set(node_list)
        self.available_nodes = set([n for n in node_list])
        self.original_nodes_list = node_list
        self.original_num_node = len(node_list)
        self.node_weights = node_weights

        self.edges = set(edge_list)

        self.calcuate_neighbours()
        self.calculate_edge_weights()

        # WARNNG: only has the correct number for chimera graphs
        self.calculate_diameter()

    def add_node(self, index, node_weight=0):

        self.nodes.add(index)
        self.node_weights[index] = node_weight

    def add_edge(self, start, end, edge_weight=0):

        self.edges.add((start,end))
        self.edge_weights[(start,end)]= edge_weight

        if start in self.neighbours.keys():
            if end not in self.neighbours[start]:
                self.neighbours[start].append(end)
        else:
            self.neighbours[start] = [end]

        if end in self.neighbours.keys():
            if start not in self.neighbours[end]:
                self.neighbours[end].append(start)
        else:
            self.neighbours[end]=[start]

    def del_node(self, node):

        # remove all edges attached to that node first.
        for neighbour in self.neighbours[node]:

            self.del_edge((node, neighbour))
            self.del_edge((neighbour, node))

            self.neighbours[neighbour].remove(node)

        # remove the node and its weight:
        self.nodes.remove(node)
        del self.node_weights[node]
        del self.neighbours[node]

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
            if edge[1] not in self.neighbours[edge[0]]:
                self.neighbours[edge[0]].append(edge[1])
            if edge[0] not in self.neighbours[edge[1]]:
                self.neighbours[edge[1]].append(edge[0])

    def calculate_edge_weights(self):
        self.edge_weights = {}

        for edge in self.edges:
            self.edge_weights[edge] = self.node_weights[edge[0]]
            self.edge_weights[(edge[1],edge[0])] = self.node_weights[edge[1]]

    def calculate_diameter(self,):
        '''Chimera graphs are 2 dimensional lattices of complete bipartite
        unit cells. Therefore, if they are indexed correctly the node 0
        (first node), and the last Node are going to have the maximum shortest
        distance from each other.
        This is the reason I replace the diameter by the distance between the
        firat and the last node:'''
        self.diameter = len(self.shortestPath(0,self.original_num_node-1))

    def add_dummy(self, vertex, vertex_model):

        s = self.dummy_index(vertex)

        self.add_node(s, 0)

        for v in vertex_model:
            self.add_edge(s,v, 0)
            self.add_edge(v,s, 0)

        return s

    def del_dummies(self):

        dummies_list = [v for v in self.nodes if v >= self.original_num_node ]

        for dummy in dummies_list:
            self.del_node(dummy)

    def Dijkstra(self,start,end=None):

        D = {}	# dictionary of final distances
        P = {}	# dictionary of predecessors
        Q = priorityDictionary()   # est.dist. of non-final vert.
        Q[start] = 0
    	for v in Q:
            D[v] = Q[v]
            if v == end:
                break
            for w in self.neighbours[v]:
                vwLength = D[v] + self.edge_weights[(v,w)]
                if w in D:
                    if vwLength < D[w]:
                        error = "found, better path to already-final vertex"
                        raise ValueError, error
                elif w not in Q or vwLength < Q[w]:
                    Q[w] = vwLength
                    P[w] = v

        return (D,P)

    def shortestPath(self,start,end):
    	"""
    	Find a single shortest path from the given start vertex
    	to the given end vertex.
    	The input has the same conventions as Dijkstra().
    	The output is a list of the vertices in order along
    	the shortest path.
    	"""

    	D,P = self.Dijkstra(start,end)

    	Path = []

        while 1:
            Path.append(end)
            if end == start:
                break
            end = P[end]

    	Path.reverse()

    	return Path

    def a_star(self, sources, old_target):
        '''
        Implementation of multisource A* as mentioned in
        practical heuristic for minor embedding paper.

        multisource A*
        Input: graph G, edge weights , heuristic costs , sources

        Output: vertex cv such that maxk i=1 d(cv, s(i)) is
        minimal among all vertices
        '''

        # Initializing variables:
        d = {}
        est = {}
        reached = {}
        min_est = priorityDictionary()
        min_src={}
        path=[]
        path_cs = []
        inf = len(self.original_nodes_list )**2*\
        len(self.edges)*10**4 # a very large number

        for v in self.nodes:
            for i in range(len(sources)):

                # d[(v,i)] = inf      # best known distance from v to i
                # est[(v,i)] = inf    # heuristic distance
                # reached[(v,i)] = False  # node v reached from source i?

                d[(v,sources[i])] = inf      # best known distance from v to i
                est[(v,sources[i])] = inf    # heuristic distance
                reached[(v,sources[i])] = False  # node v reached from source i?

        for v in self.nodes:
            min_est[v] = inf    # min. dist. to v among all i

        for i in range(len(sources)):

            # This is dangereous:
            d[(sources[i],sources[i])] = 0

            min_est[sources[i]] = 0;

            #min_src[sources[i]] = i     #index of source for min_est
            # I am trying to use the correct indecies for sources:
            min_src[sources[i]] = sources[i]     #index of source for min_est


        while True:

            #current node calculation:
            if path != []:
                cv = self.neighbours[path[-1]][0]
            else:
                cv = self.neighbours[sources[0]][0]

            for v in self.nodes:
                    if min_est[v] < min_est[cv]:
                        cv = v

            #current source calculation:
            cs = min_src[cv]

            reached[(cv,cs)] = True

            # Check if all sources have reached cv:
            check_counter = 0
            for i in range(len(sources)):
                if (cv,sources[i]) in reached.keys():
                    if  reached[(cv,sources[i])] == True:
                        if cv not in sources:
                            if cv not in self.neighbours[sources[i]]:
                                check_counter += 1

            if check_counter == len(sources):
                return cv   # all sources have reached cv

            # Find new best source for cv:
            found_minsrc = sources[0]

            for i in range(len(sources)):
                 if reached[(cv,sources[i])] == False:

                    if est[(cv,sources[i])] < est[(cv,found_minsrc)]:
                        found_minsrc = sources[i]

            min_src[cv] = found_minsrc

            # Find new best distance for cv:
            min_est[cv] = est[(v,min_src[cv])]

            # update neighbour distances:
            for v in self.neighbours[cv]:
                # alternate distance to cs
                alt = d[(cv,cs)] + self.edge_weights[(v,cv)]

                if alt < d[(v,cs)]:

                    d[(v,cs)] = alt         #distance improved

                    # calculate heuristic cost for vertex v to old target g*:
                    h_cost_v = len(self.shortestPath(v, old_target))

                    #est[(v,cs)] = d[(v,cs)] + h_cost[v]  #new heuristic distance
                    est[(v,cs)] = d[(v,cs)] + h_cost_v

                    if est[(v,cs)] < min_est[v]:
                        min_est[v] = est[(v,cs)]    #improved best distance
                        min_src[v] = cs
