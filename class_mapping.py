from random import shuffle, choice
import class_graph as CLG
import networkx as nx
import matplotlib.pyplot as plt
from numpy import random

class mapping():
    def __init__(self, G_dict, H_dict):
        ''' It should create these two graph objects: G and directed_H:'''
        # Build an instance of Graph class with graph G:
        G_nodes =[]
        G_edges = []
        G_node_weights = {}

        for key in G_dict.keys():
            G_nodes.append(key)
            G_node_weights[key] = 0

        for key in G_dict.keys():
            for v2 in G_dict[key]:
                G_edges.append((key,v2))

        self.G = CLG.graph(G_nodes, G_edges, G_node_weights)

        # build another instance of Graph object using H info:
        H_nodes =[]
        H_edges = []
        H_node_weights = {}

        for key in H_dict.keys():
            H_nodes.append(key)
            H_node_weights[key] = 0

        for key in H_dict.keys():
            for v2 in H_dict[key]:
                H_edges.append((key,v2))
                H_edges.append((v2,key))

        self.directed_H = CLG.graph(H_nodes, H_edges, H_node_weights)

    def initial_placement(self):
        ''' initialize phi and inverse phi
        for now by a random inital placement.
        '''
        self.phi = {}
        self.phi_inverse = {}
        self.roots = {}

        vertices = [v for v in list(self.G.nodes)]
        shuffle(vertices)

        for vertex in vertices:

            list_available = [v for v in self.directed_H.available_nodes]
            heuristic_root = choice(list_available)

            self.routing(vertex,heuristic_root)

            #print vertex, 'in G -->', self.phi[vertex], 'in H'
            #print 'weights:', self.directed_H.node_weights
            #print 'edge weights:', self.directed_H.edge_weights

            self.directed_H.available_nodes =\
            self.directed_H.available_nodes - set(self.phi[vertex])


    def is_valid_embedding(self):
        ''' check if the current mapping is a valid embedding.'''
        NOT_VALID = False

        for v in self.G.nodes:
            if len(self.phi[v]) == 0:
                NOT_VALID = True

        for node in self.phi_inverse.keys():
            if  len(self.phi_inverse[node]) > 1:
                NOT_VALID = True

        return NOT_VALID

    def add_sources(self, vertex):
        ''' add dummy source nodes on the H graph to represent vertex models:'''
        sources_list = []

        for neighbour in self.G.neighbours[vertex]:
            if neighbour in self.phi.keys():
                if self.phi[neighbour] != []:
                    source = self.directed_H.add_dummy(neighbour, \
                    self.phi[neighbour])

                    sources_list.append(source)

        return sources_list

    def del_sources(self):
        ''' get rid of the dummy source nodes added before'''
        self.directed_H.del_dummies()

    def routing(self, vertex, old_root):
        ''' '''
        # populate sources for vertex:
        sources = self.add_sources(vertex)

        if sources == []:
            ''' assign a random node on H_directed'''
            new_root = choice(self.G.original_nodes_list)
            chain = new_root
        else:
            # A*  gives the root node
            new_root = self.directed_H.a_star(sources, old_root)

            # chain is the union of shortest pathes from root to each
            # neighbouring vertex model:
            chain = [new_root]
            for source in sources:
                path = self.directed_H.shortestPath(new_root,source)
                for node in path:
                    if node != new_root and node != source:
                        if node not in self.directed_H.neighbours[source]:
                            chain.append(node)


        # delete the sources for the mapping:
        self.del_sources()

        # make sure that chain is always a list:
        if not isinstance(chain, list):
            chain = [chain]

        # Update mapping with new root and new chain
        # Update the root:
        self.roots[vertex] = new_root

        # Update the vertex model:
        self.phi[vertex] = [v for v in chain]

        # Update the inverse vertex model and the node weights:
        for node in chain:
            if node in self.phi_inverse.keys():
                self.phi_inverse[node].append(vertex)
            else:
                self.phi_inverse[node] = [vertex]

            # Update the node_weight for node.
            self.directed_H.node_weights[node] = self.directed_H.diameter **\
            len(self.phi_inverse[node])

        # update the edge weights in directed_H:
        self.directed_H.calculate_edge_weights()

    def rip_Up(self, vertex):

        '''
        ...
        '''

        # store the root node:
        old_root  = self.roots[vertex]

        # clear the root
        self.roots[vertex] = []

        # clear the phi inverse and node weights in directed_H:
        for node in self.phi[vertex]:
            self.phi_inverse[node].remove(vertex)

            # Update the node_weight for node.
            self.directed_H.node_weights[node] = self.directed_H.diameter **\
            len(self.phi_inverse[node])

        # update the edge weights in directed_H:
        self.directed_H.calculate_edge_weights()

        # clear phi:
        self.phi[vertex]= []

        return old_root

    def visualize(self, pos):

        g_emb = nx.Graph()

        g_emb.add_nodes_from(self.directed_H.original_nodes_list)

        g_emb.add_edges_from(self.directed_H.edges)

        #pos=nx.spring_layout(g_emb, iterations = 10*6)
        color_dict={}
        for vertex in self.G.nodes:
            color_dict[vertex] = random.rand(3,1)

        colors = []
        labels={}
        for node in self.directed_H.original_nodes_list:

            if node in self.phi_inverse.keys():
                if self.phi_inverse[node] ==[]:
                    label[node]=' '
                    colors.append([.9,0.9,0.9])
                else:
                    labels[node] = self.phi_inverse[node][0]
                    colors.append(color_dict[self.phi_inverse[node][0]])
            else:
                colors.append([.9,0.9,0.9])
                labels[node]=' '

        nx.draw(g_emb, pos, node_size=100, node_color= colors)

        nx.draw_networkx_labels(g_emb,pos,labels=labels,font_size=7,\
        font_family='sans-serif', edge_color='#878787')

        plt.axis('off')
        #plt.savefig("weighted_graph.png") # save as png
        plt.show() # display
