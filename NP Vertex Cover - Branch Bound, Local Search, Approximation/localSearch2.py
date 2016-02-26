# Local Search
# Strategy 2
# Author Zongwan
# Team U
import random
from time import time 
from collections import defaultdict

# Given a graph, return a valid vertex cover and initialized loss fucntion for each vertex
def ConstructVC(content, n, m, loss, adjnode,uncover):
	vc = list()
	for u in range (1, n+1):
		if u not in vc:
			for j in range (len(adjnode[u])):
				v = adjnode[u][j]
				if v not in vc:
					if len(adjnode[u]) > len(adjnode[v]):
						vc.append(u)
					else:
						vc.append(v)
				if u in vc:
					break
	for item in vc:
		loss[item] = 0;
	for u in vc:
		mylist = [item for item in adjnode[u] if item not in vc]
		loss[u] += len(mylist)
	for u in vc:
		if loss[u] == 0:
			(c,loss,uncover) = UpdateRm(vc,u,loss,uncover,adjnode)
	return (vc, loss)

# Check if current solution is a valid vertex cover
def IsVertexCover(sol, totalvertex, adjnode):
	for item in range (1, totalvertex+1):
		if item not in sol:
			for node in adjnode[item]:
				if node not in sol:
					return False
	return True

# After removing a node from current solution, update loss function and uncovered nodes 
def UpdateRm(sol,key,loss,uncover,adjnode):
	sol.remove(key)
	loss.pop(key)
	# Update loss function
	mylist = [item for item in adjnode[key] if item in sol]
	for item in mylist:
		loss[item] += 1
	# Update uncovered edge
	mylist = [item for item in adjnode[key] if item not in sol]
	if mylist:
		uncover[key] = mylist
		for item in mylist:
			if item in uncover.keys():
				uncover[item].append(key)
			else:
				keylist = list()
				keylist.append(key)
				uncover[item] = keylist
	return (sol,loss, uncover)

# After adding a node into current solution, update loss function and uncovered nodes 
def UpdateAdd(sol,key,loss,uncover,adjnode):
	sol.append(key)
	uncover.pop(key)
	mylist = [item for item in adjnode[key] if item in sol]
	for item in mylist:
		loss[item] -= 1
	mylist = [item for item in adjnode[key] if item not in sol]
	for item in mylist:
		uncover[item].remove(key)
		if not uncover[item]:
			uncover.pop(item)
	loss[key] = len(mylist)
	return (sol,loss,uncover)

# Choose a vertex from current solution randomly
def ChooseRmVertex(sol,loss):
	best = random.choice(sol)
	k = 20
	for i in range (k):
		temp = random.choice(sol)
		if loss[temp] < loss[best]:
			best = temp
	return best

# Initialized vertex cover
def LocalSearch2(graph,cutoff,seed):
	random.seed(seed)
	t = time()
	adjnode = dict()
	print graph
	file = open(graph+'.graph','r')
	content = file.readlines()
	totalvertex = int(content[0].split(" ")[0])
	totaledge = int(content[0].split(" ")[1])
	for i in range (1, totalvertex+1):
		try:
			adjnode[i] = [int(item) for item in content[i].strip().split(" ")]
		except:
			adjnode[i] = {}

	c = list() # current solution may be a valid vertex cover, may be not
	opt = list()  # current optimal vertex cover
	loss = dict()  # key: vertex in current solution; value: corresponding loss value for each key
	uncover = dict() # key: vertex not in current solution; value: adjacent nodes which are also not in current solution
	# Initialized vertex cover
	(c, loss) = ConstructVC(content, totalvertex, totaledge, loss, adjnode, uncover)
	tracefile = open(graph+'_LS2_'+str(cutoff)+'_'+str(seed)+'.trace','w')
	print "Time %0.2f initial size %d" %(time() - t, len(c))
	while time() - t < cutoff:
		if IsVertexCover(c,totalvertex, adjnode):  # If a vertex cover, record timestamp and its size, remove min loss vertex from it
			print "Time %0.2f size %d" %(time() - t, len(c))
			tracefile.write("%0.2f, %d" %(time() - t, len(c)))
			tracefile.write('\n')
			opt = c[:]
			rm = min(loss, key = loss.get)
			(c,loss,uncover) = UpdateRm(c,rm, loss,uncover,adjnode)   	
			continue
		# If not a vertex cover, choose a vertex from it randomly
		u = ChooseRmVertex(c,loss)
		# Remove this vertex, update vertex cover and loss funtion
		(c,loss,uncover) = UpdateRm(c,u,loss,uncover,adjnode)
		# Find a uncovered edge e and its two end points
		endone = random.choice(uncover.keys())  
		endtwo = random.choice(uncover[endone])
		if endtwo not in uncover.keys():
			mylist = [item for item in adjnode[endtwo] if item not in c]
			if mylist:
				uncover[endtwo] = mylist
		if len(uncover[endone]) > len(uncover[endtwo]):
			v = endone
		else:
			v = endtwo
		# Add the endpoint of e with greater gain, breaking ties by random one
		(c,loss,uncover) = UpdateAdd(c,v,loss,uncover,adjnode)
	solfile = open(graph+'_LS2_'+str(cutoff)+'_'+str(seed)+'.sol','w')
	# print len(opt)
	# print opt
	solfile.write("%d," %len(opt))
	solfile.write('\n')
	solfile.write(str(opt).replace("[","").replace("]",""))

