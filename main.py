'''
'''
import class_mapping as MP
from random import shuffle
import time

def embed(G_dict, H_dict):

    #initialize mapping
    mapping = MP.mapping(G_dict, H_dict)

    # create initial placement to have vertex model phi and inverse phi:
    mapping.initial_placement()


    # check if mapping is an embedding of G in H
    if mapping.is_valid_embedding:
        return mapping
    else:
        mapping = ripUP_and_reRoute(mapping)

    return mapping


def ripUP_and_reRoute(mapping):

    # TODO:Initialize some statistics:

    # find a random order of vertices of G:
    shuffled_G_Vertices = [v for v in list(mapping.G.nodes)]
    shuffle(shuffled_G_Vertices)

    # BIG LOOP:-------------------------------------------
    stage = 0
    while stage <= 2:
        stage += 1
    # TODO:Continue while :
    # 1_ an embedding is found (DONE)
    # 2_ no improvement_max is reached (not tracking improvements now)
    # 3_ stage is less than 2 ?! (DONE)

        # TODO:update the statstics

        # loop over variables in G:-------------------------
        for vertex in shuffled_G_Vertices:
            '''rip_UP:
            '''
            old_route = mapping.rip_UP(vertex)


            '''
            re_route :
            '''
            mapping.routing(vertex, old_root)

        # update statistics

        # check if we found an embedding
        if mapping.is_valid_embedding:
            break

        # TODO:check if there has been an improvement 5 criteria:
        # update stats according to the improvement_max
        # specify improevement

    return mapping

if __name__ == "__main__":

    import graph_gen as GG

    G_d = GG.get_gerid_graph(3,4)

    H_d, positions = GG.get_chimera_graph(M=4,N=4,L=4)

    res = embed(G_d, H_d)

    print 'final solution:', res.phi
    res.visualize(positions)

    for n in range(3,6):
        G_d = GG.get_complete_graph(n)
        H_d, positions = GG.get_chimera_graph(M=2,N=2,L=4)
        t1=time.time()
        res = embed(G_d, H_d)
        t2=time.time()
        print 'Complete graph of size', n, '@time:', t2-t1
        res.visualize(positions)
