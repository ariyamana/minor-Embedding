'''
TODO:
 >>> the chain produced by A* includes the sources and the end .
 it must not include them.
 >>> check the above ^^

2_ write get embedding
3_ write validate embedding.

'''
import class_mapping as MP
from random import shuffle

def embed(G_dict, H_dict):

    #initialize mapping
    mapping = MP.mapping(G_dict, H_dict)

    # create initial placement to have vertex model phi and inverse phi:

    mapping.initial_placement()


    # check if mapping is an embedding of G in H
    # If yes -->  return mapping
    # if NO --> rip up and re route
    if mapping.is_valid_embedding:
        mapping.get_embedding()
    else:
        mapping = ripUP_and_reRoute(mapping)

    return mapping


def ripUP_and_reRoute(mapping):

    # Find the number of unplaced variables:

    # Initialize some statistics:

    # find a random order of vertices of G:
    shuffled_G_Vertices = [v for v in list(mapping.G.nodes)]
    shuffle(shuffled_G_Vertices)

    # BIG LOOP:-------------------------------------------
    stage = 0
    while stage <= 2:
        stage += 1
    # Continue while :
    # 1_ an embedding is found
    # 2_ no improvement_max is reached
    # 3_ stage is less than 2 ?!

        # update the statstics

        # loop over variables in G:-------------------------
        for vertex in shuffled_G_Vertices:
            '''rip_UP:
            '''
            old_route = mapping.rip_UP(vertex)


            '''re_route :
            '''
            mapping.routing(vertex, old_root)

        # update statistics

        # check if we found an embedding

        # check if there has been an improvement 5 criteria:

        # update stats according to the improvement_max

        # specify improevement

    return mapping

if __name__ == "__main__":
    G_d = {0:[1,2,3,4], 1:[0,2,3,4], 2:[0,1,3,4], 3:[0,1,2,4], 4: [0,1,2,3]}
    H_d = {0:[4,5,6,7], 1:[4,5,6,7], 2:[4,5,6,7], 3:[4,5,6,7],
           4:[0,1,2,3], 5:[0,1,2,3], 6:[0,1,2,3], 7:[0,1,2,3]}

    res = embed(G_d, H_d)

    print 'final solution:', res.phi
