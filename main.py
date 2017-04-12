import class_mapping as MP

def embed(G, H):

    #initialize mapping
    mapping = MP.mapping(G, H)

    # create initial placement to have vertex model phi and inverse phi:
    mapping.initial_placement()

    # check if mapping is an embedding of G in H
    # If yes -->  return mapping
    # if NO --> rip up and re route
    if mapping.is_valid_embedding:
        mapping.get_embedding()
    else:
        mapping = ripUP_and_reRoute(mapping)


def ripUP_and_reRoute(mapping):

    # Find the number of unpaced variables:

    # Initialize some statistics:

    # Make the directed H:

    # Find diameter of H

    # find a random order of nodegs of G:

    # BIG LOOP:-------------------------------------------
    # Continue while :
    # 1_ an embedding is found
    # 2_ no improvement_max is reached
    # 3_ stage is less than 2 ?!

        # update the statstics

        # loop over variables in G:-------------------------

            # rip_UP $$$$$$$$$$$$
            # re_route $$$$$$$$$$

            mapping = re_route(variable, G, directed_H, phi, phi_inverse, diameter)

        # update statistics

        # check if we found an embedding

        # check if there has been an improvement 5 criteria:

        # update stats according to the improvement_max

        # specify improevement

    return mapping


def re_route(variable, G, directed_H, phi, phi_inverse, diameter):

    # if this variable has a phi remove it and update the following:
    # phi, inverse phi, node and edge weights on H

    # Get its neighouring variables in G

    # if all the neighbours are empty --> assign a random node on H
    # if not :
        chain = routing(variable, G, directed_H, phi, inverse_phi, diameter)

    # Update phi and inverse phi according to chain

    # update node wieghts on H

    return mapping



def routing(vertex, mapping, diameter):

    # populate sources for vertex:
    sources = mapping.add_sources(vertex)

    # Prepare heuristic costs:
    h_cost = ???

    # A* gives the root node
    root = a_star(mapping.directed_H, h_cost, sources)

    # delete the sources for the mapping:
    mapping.del_sources()

    # build the path for the chain given the route.
    chain = ???

    return chain
