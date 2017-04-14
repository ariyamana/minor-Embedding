'''
Module to create different input graphs.
'''

from numpy import array
import networkx as nx

def get_chimera_graph(M,N,L=4):

    node_list = range(M*N*2*L)
    edge_list = []
    g_dict = {}

    pos = {}
    h_space = 0.01
    v_space = 0.01

    block_w = (1 - (M-1)*h_space)/(1.0*M)
    block_l = (1 - (N-1)*v_space)/(1.0*N)

    for m in range(1, M+1):

        left_boundary = (m-1)* (block_w + h_space)
        for n in range(1, N+1):
            num_var_before = 2*(n-1)*M*L + 2*(m-1)*L

            top_boundary = (n-1)* (block_l + v_space)

            # complete bipartite inside a unit cell:
            for q in range(L):
                for p in range(L, 2*L):
                    edge_list.append((num_var_before+q,num_var_before+p))

                    if (p-L) < (L*1.0/2.0):
                         y = top_boundary  + block_l*1.0/(L+1.) * ((p-L)-1./2.)
                         x = left_boundary + block_w*1.0/2.0
                    else:
                        y = top_boundary + block_l*1.0/(L+1.) * ((p-L) + 1./2.)
                        x = left_boundary + block_w*1.0/2.0
                    pos[num_var_before+p] = array([x,y])

                if q < (L*1.0/2.0):
                     x = left_boundary+ block_w*1.0/(L+1.) * (q+1-1./2.)
                     y = top_boundary + block_l*1.5/(L+1.)
                else:
                    x = left_boundary+ block_w*1.0/(L+1.) * (q+1+1./2.)
                    y = top_boundary + block_l*1.5/(L+1.)
                pos[num_var_before+q] = array([x,y])
            # the horizontal edges:
            if m < M:
                for p in range(L, 2*L):
                    edge_list.append((num_var_before+p,num_var_before+p+2*L))
            # the vertical edges:
            if n < N:
                for q in range(L):
                    edge_list.append((num_var_before+q,num_var_before+q+2*M*L))

    for node in node_list:
        g_dict[node] = []

    for edge in edge_list:
        g_dict[edge[0]].append(edge[1])
        g_dict[edge[1]].append(edge[0])

    return g_dict, pos

def get_gerid_graph(K,T):

        G = nx.grid_2d_graph(K, T)

        G_d={}
        for node in G.nodes():
            G_d[node[0]*T+node[1]]=[]
            neigh = G.neighbors(node)
            for n in neigh:
                G_d[node[0]*T+node[1]].append(n[0]*T+n[1])

        return G_d
