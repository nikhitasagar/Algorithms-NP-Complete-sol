import networkx as nx
import time
import sys
import Queue
from copy import deepcopy as dc


#This is a built in python function. 
def min_weighted_vertex_cover(G, weight=None):
    weight_func = lambda nd: nd.get(weight, 1)
    cost = dict((n, weight_func(nd)) for n, nd in G.nodes(data=True))

    # while there are edges uncovered, continue
    for u,v in G.edges_iter():
        # select some uncovered edge
        min_cost = min([cost[u], cost[v]])
        cost[u] -= min_cost
        cost[v] -= min_cost

    return set(u for u in cost if cost[u] == 0)


def BnB(filename, cutoff, randseed):
    G = nx.Graph()
    f = open('%s.graph'%filename,'r')
    content = f.readlines()
    num_vertices = int(content[0].split(" ")[0])
    num_edges = int(content[0].split(" ")[1])

    for i in range (1, num_vertices+1):
        G.add_node(i)
        try:
            edges = [int(item) for item in content[i].strip().split(" ")]
            for e in edges:
                G.add_edge(i,e)
        except ValueError:
                pass  


    G_Remaining = dc(G)
    #best_initial = len(G.nodes())
    best_initial = len(min_weighted_vertex_cover(G, None))
    degree_sorted_nodes = sorted(G.degree(), key=G.degree().get)
    V_remaining = []
    #V_remaining = set()
    for item in degree_sorted_nodes:
        #V_remaining.add(item)
        V_remaining.append(item)

    q = Queue.LifoQueue()
    I = []
    q.put((I, V_remaining, G_Remaining))
    VC = min_weighted_vertex_cover(G, None)
    start = time.time()
    elapsed  = 0
    output_trace = open("%s_BnB_%d_%d.trace" %(filename, cutoff, randseed), 'a')
    while(not q.empty() and elapsed < cutoff):

        Inc, V_rem, G_rem = q.get()

        if not G_rem.edges():
            if len(Inc) < best_initial:
                best_initial = len(Inc)
                VC = Inc
                output_trace.write(str(elapsed)+", "+str(len(VC))+"\n")
        else:
            if V_rem:
                v = V_rem.pop()  
                if (len(Inc) + len(nx.maximal_matching(G_rem))) <= best_initial:
                    V_I = Inc
                    V_I = V_I + G_rem.neighbors(v)
                    V_R = V_rem
                    V_R = [item for item in V_rem if item not in G_rem.neighbors(v)]
                    G_pass = dc(G_rem)
                    G_pass.remove_nodes_from(G_rem.neighbors(v)) 
                    q.put((dc(V_I), dc(V_R), dc(G_pass)))
                
                G_rem.remove_node(v)
                Inc.append(v)
                if(len(Inc) + len(nx.maximal_matching(G_rem))) <= best_initial:
                    q.put((dc(Inc), dc(V_rem), dc(G_rem)))
        elapsed = (time.time() - start)
    
    output_sol = open('%s_BnB_%d_%d.sol'%(filename, cutoff, randseed), 'w')
    output_sol.write(str(len(VC)) + "\n" + str(VC).strip('[]'))

    print VC
    print len(VC)
    print elapsed
  