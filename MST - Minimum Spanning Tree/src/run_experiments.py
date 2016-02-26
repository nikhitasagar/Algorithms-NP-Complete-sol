#!/usr/bin/python
##  CSE6140 HW1
##  This assignment requires installation of networkx package if you want to make use of available graph data structures or you can write your own!!
##  Please feel free to modify this code or write your own
import networkx as nx
import time
import sys

class disjoint_set:
    def __init__(self):
        self.parent = dict()
        self.rank = dict()
    
    def make_set(self, node):
        self.parent[node] = node
        self.rank[node] = 0

    def find(self, node):
        if self.parent[node] != node:
            self.parent[node] = self.find(self.parent[node])
        return self.parent[node]

    def union(self,u, v):
        root_u = self.find(u)
        root_v = self.find(v)
        if root_u != root_v:
            if self.rank[root_u] > self.rank[root_v]:
                self.parent[root_v] = root_u
            else:
                self.parent[root_u] = root_v
                if self.rank[root_u] == self.rank[root_v]: self.rank[root_v] += 1

class RunExperiments:
    def read_graph(self, filename):
        G = nx.MultiGraph()
        edge_list = open(filename,"r").read().split("\n")
        edges = []
        for e in edge_list[1:]:
            if e:
                n1,n2,w = e.split(" ")
                edges.append((int(n1),int(n2),int(w)))
        G.add_weighted_edges_from(edges)
        return G
        
    
    def computeMST(self, G):
        for node in G.nodes():
            self.ds.make_set(node)
        for u,v, w in sorted(G.edges(data=True),key=lambda (u,v,w):w['weight']):
            if self.ds.find(u) != self.ds.find(v):
                self.ds.union(u, v)
                self.mst.append((u,v,w['weight']))
        return sum(x[2] for x in self.mst)

    def recomputeMST(self,u,v,weight,G):
        if weight>=max(self.mst, key=lambda (v1,v2,w):w):
            return sum([x[2] for x in self.mst])
        for edge in self.mst:
            v1,v2,w = edge
            if(u,v)==(v1,v2) or (u,v)==(v2,v1):
                if w>weight:
                    self.mst.remove(edge)
                    self.mst.append((u,v,weight))
                    return sum([x[2] for x in self.mst])
                return sum([x[2] for x in self.mst])
        mst = nx.Graph()
        mst.add_weighted_edges_from(self.mst+[(u,v,weight)])
        cycleCheck = nx.cycle_basis(mst)[0]
        remove_edge = []
        for edge in self.mst + [(u,v,weight)]:
            v1,v2,w = edge
            if v1 in cycleCheck and v2 in cycleCheck:
                remove_edge.append(edge)
        remove_edge = max(remove_edge, key = lambda (v1,v2,w):w)
        if remove_edge in self.mst:
            self.mst.remove(remove_edge)
            self.mst.append((u,v,weight))
        return sum([x[2] for x in self.mst])

    def main(self):
        self.mst = []
        self.ds = disjoint_set()
        num_args = len(sys.argv)

        if num_args < 4:
            print ("error: not enough input arguments")
            exit(1)

        graph_file = sys.argv[1]
        change_file = sys.argv[2]
        output_file = sys.argv[3]

        #Construct graph
        G = self.read_graph(graph_file)

        start_MST = timeit.default_timer() #time in seconds
        MSTweight = self.computeMST(G) #call MST function to return total weight of MST
        total_time = (timeit.default_timer() - start_MST) * 1000 #to convert to milliseconds

        #Write initial MST weight and time to file
        output = open(output_file, 'w')
        output.write(str(MSTweight) + " " + str(total_time))


        #Changes file
        with open(change_file, 'r') as changes:
            num_changes = changes.readline()

            for line in changes:
                #parse edge and weight
                edge_data = list(map(lambda x: int(x), line.split()))
                assert(len(edge_data) == 3)

                u,v,weight = edge_data[0], edge_data[1], edge_data[2]

                #call recomputeMST function
                start_recompute = timeit.default_timer()
                new_weight = self.recomputeMST(u, v, weight, G)
                total_recompute = (timeit.default_timer() - start_recompute) * 1000 # to convert to milliseconds

                #write new weight and time to output file
                output.write(str(new_weight) + " " + str(total_recompute))




if __name__ == '__main__':
    # run the experiments
    runexp = RunExperiments()
    runexp.main()
