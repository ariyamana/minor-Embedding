
def a_star(G, h_cost, sources):
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
    min_est = {}
    min_src={}

    inf = len(G.nodes)**2*len(G.edges)*10**4 # a very large number

    print 'initializing done.', inf

    for v in G.nodes:
        for i in range(len(sources)):

            d[(v,i)] = inf      # best known distance from v to i
            est[(v,i)] = inf    # heuristic distance
            reached[(v,i)] = False  # node v reached from source i?

    for v in G.nodes:
        min_est[v] = inf    # min. dist. to v among all i

    for i in range(len(sources)):
        d[(sources[i],i)] = 0
        min_est[sources[i]] = 0;
        min_src[sources[i]] = i     #index of source for min_est

    print 'making dicts done.'
    print '-'*10


    while True:

        #current node calculation:
        cv = list(G.nodes)[0]

        for v in G.nodes:
            if min_est[v] < min_est[cv]:
                cv = v

        #current source calculation:
        print 'cv is ', cv
        print 'min_src[cv] is ', min_src[cv]

        cs = min_src[cv]
        print 'this is cs:', cs

        reached[(cv,cs)] = True

        # Check if all sources have reached cv:
        check_counter=0
        for i in range(len(sources)):
            if reached[(cv,i)] == True:
                print 'reached i = ',i
                check_counter +=1
        print 'check counter = ', check_counter
        if check_counter == len(sources):
            return cv   # all sources have reached cv

        # Find new best source for cv:
        found_minsrc = 0

        for i in range(len(sources)):
            if reached[(cv,i)] == False:
                if est[(cv,i)] < est[(cv,found_minsrc)]:
                    found_minsrc = i

        min_src[cv] = found_minsrc
        print 'above:', min_src
        print 'best source for vertex', cv, 'is node', sources[found_minsrc],
        print 'which is source',  found_minsrc

        # Find new best distance for cv:
        min_est[cv] = est[(v,min_src[cv])]

        # update neighbour distances:
        for v in G.neighbours[cv]:
            print 'neighbors of', cv, ':', G.neighbours[cv]
            # alternate distance to cs
            alt = d[(cv,cs)] + G.edge_weights[(v,cv)]

            if alt < d[(v,cs)]:

                d[(v,cs)] = alt         #distance improved

                est[(v,cs)] = d[(v,cs)] + h_cost[v]  #new heuristic distance

                if est[(v,cs)] < min_est[v]:
                    min_est[v] = est[(v,cs)]    #improved best distance
                    min_src[v] = cs
                    print min_src
                    
        print '-'*10


if __name__=='__main__':
    import class_graph as CG

    node_l = range(10,17)
    node_w = {10:1, 11:1, 12:1, 13:1, 14:1, 15:1, 16:2000}

    h_cost = {10:200, 11:100, 12:208, 13:30, 14:40, 15:50, 16:50}

    edge_l = [(10,11),(10,16), (11,12), (12,13), (13, 15), (13,14), (14,15), (14,16), (15,16)]

    source = [10,14]

    G = CG.graph(node_l, edge_l, node_w)

    vertex = a_star(G, h_cost, source)

    print vertex
