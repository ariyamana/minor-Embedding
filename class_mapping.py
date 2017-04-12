class mapping():
    def __init__(self, G, H):

        self.G = G
        self.directed_H = H

    def initial_placement(self):
        ''' initialize phi and inverse phi
        for now by a random inital placement.
        '''
        self.phi = {}
        self.phi_inverse = {}

    def update_mapping(self):
        ''' update vertex model phi and its inverse
        based on the changes throut the rip-up and reroute algorithms'''
        pass

    def is_valid_embedding(self):
        ''' check if the current mapping is a valid embedding.'''
        pass

    def get_embedding(self):
        ''' transform the current mapping into an embedding output format'''
        pass

    def add_sources(self, vertex):
        ''' add dummy source nodes on the H graph to represent vertex models:'''
        sources_list = []

        for neighbour in self.G.neighbours[vertex]:
            source = self.H.add_dummy(neighbour, self.phi[neighbour])
            sources_list.append(source)

        return sources

    def del_sources(self):
        ''' get rid of the dummy source nodes added before'''
        self.H.del_dummies()
