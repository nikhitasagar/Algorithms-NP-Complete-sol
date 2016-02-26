import networkx as nx
import time
import sys


def Approximation(file_name, cutoff_time, randseed):
	G = nx.MultiGraph()
	f = open('%s.graph'%file_name,'r')
	content = f.readlines()
	num_vertices = int(content[0].split(" ")[0])
	#num_vertices = 6
	num_edges = int(content[0].split(" ")[1])
	

	for i in range (1, num_vertices+1):
		#adjnode[i] = [int(item) for item in content[i].strip().split(" ")]
		G.add_node(i, visited = False)
		#G.add_node(i)
		#if content[i] != '':
		try:
			edges = [int(item) for item in content[i].strip().split(" ")]
			for e in edges:
				G.add_edge(i,e)
		except ValueError:
   			pass  

	start = time.time()
	vc = []
	for (u,v) in G.edges_iter():
		if G.node[u]['visited'] == False and G.node[v]['visited'] == False:
			G.node[u]['visited'] = True
			G.node[v]['visited'] = True
	vc = [n for n in G if G.node[n]['visited']==True]
	elapsed = str(time.time() - start)

	output_sol = open('%s_Approx_%d_%d.sol'%(file_name, cutoff_time, randseed), 'w')
	output_sol.write(str(len(vc)) + "\n" + str(vc).strip('[]'))
	output_trace = open("%s_Approx_%d_%d.trace" %(file_name, cutoff_time, randseed), 'a')
	output_trace.write(str(elapsed)+", "+str(len(vc)))
	print vc
	print elapsed
	print len(vc)