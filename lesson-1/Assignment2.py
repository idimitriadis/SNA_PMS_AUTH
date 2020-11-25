# # 1st Assignment - Network Connectivity - part B
# This assignment involves the importing and analysis of an internal email communication network amongst employees
# of a manufacturing company.
#
# Each node depicts and employee and each directed edge between two nodes depicts and individual mail. The node to the
# left represents the sender and the node to the right represents the recipient.

import networkx as nx


# ### Question 1
#
# Use NetworkX to load up the directed multigraph, located in `mail_network.txt` and make sure the node names are
# strings.
#
# [*Returns a directed multigraph networkx graph]

def answer_one():
    DMGraph = nx.read_edgelist('graphs/email_network.txt', data=[('time', int)], create_using=nx.MultiDiGraph())
    return DMGraph


# for n in MG.edges(data=True):
#     print (n)
# ### Question 2
#
# Find the number of employees and mails in the graph from Question 1.
#
# [*Returns a tuple (<num_of_employees>, <num_of_mails>).*


def answer_two(multigraph):
    # Your Code Here
    num_of_employees = len(multigraph.nodes())
    num_of_mails = len(multigraph.edges())

    # print((num_of_employees, num_of_mails))

    return  (num_of_employees, num_of_mails) # Your Answer Here




# ### Question 3
#
# * Part 1. For this part, we assume that the information in this company can only be exchanged via mail.
#
#   Whenever an employee sends a mail to another employee, a one-way communication channel is created, which allows the
#   sender to provide info to the receiver, but not vice versa
#
#   Based on the mail transaction present in our dataset, detect whether it is possible for info to go from every employ
#   to every other employ (True, False)
#
# * Part 2. For this part, we assume that the communication channel that is established by a mail allows for vice-versa
#           communication (both ways)
#
#   Based on the mail transaction present in our dataset, detect whether it is possible for info to go from every employ
#   to every other employ (True, False)
#
# [*Returns a tuple of bools (<part1>, <part2>)]

def answer_three(multigraph):
    # Your Code Here
    is_strongly = nx.is_strongly_connected(multigraph)
    is_connected = nx.is_weakly_connected(multigraph)
    # Alternative solution for part 2
    # g = nx.to_undirected(multigraph)
    # is_connected = nx.is_connected(g)

    # print((is_strongly, is_connected))

    return (is_strongly, is_connected) # Your Answer Here



# ### Question 4
#
# What is the number of nodes in the largest (in terms of nodes) weakly connected component?
#
# [*Returns an int]


def answer_four(multigraph):
    # Your Code Here
    # sort weakly connected components by num of nodes inside each component
    weakly_con_comps = sorted(nx.weakly_connected_components(multigraph), key=len, reverse=True)

    # print(len(weakly_con_comps[0]))

    return len(weakly_con_comps[0]) # Your Answer Here



# ### Question 5
#
# What is the number of nodes in the largest (in terms of nodes) strongly connected component?
#
# [*Returns an int]

def answer_five(multigraph):
    # Your Code Here
    # sort strongly connected components by num of nodes inside each component
    strongly_con_comps = sorted(nx.strongly_connected_components(multigraph), key=len, reverse=True)

    # print(len(strongly_con_comps[0]))

    return len(strongly_con_comps[0])  # Your Answer Here



# ### Question 6
#
# Use the NetworkX function for strongly connected component subgraphs to find the subgraph of nodes in a largest
# strongly connected component. Assume that this graph is called G_sc.
#
# [*Returns a NetworkX MultiDiGraph named G_sc]


def answer_six(multigraph):
    # Your Code Here
    strongly_con_comps = sorted(nx.strongly_connected_components(multigraph), key=len, reverse=True)
    G_sc = nx.subgraph(multigraph, strongly_con_comps[0])

    # print(len(G_sc.nodes()))
    # print(len(G_sc.edges()))

    return G_sc # Your Answer Here

# ### Question 7
#
# Calculate the average distance between nodes in G_sc (from question 6)
#
# [*Returns a float]


def answer_seven(G_sc):
    # Your Code Here
    try:
        avg = nx.average_shortest_path_length(G_sc)
    except nx.NetworkXError:
        print ('Graph is not connected')
        avg = 0

    # print ('Average distance:', avg)

    return avg # Your Answer Here

# ### Question 8
#
# Calculate the largest possible distance between two employees in the G_sc graph (from question 6)
#
# [*Returns an int]


def answer_eight(G_sc):
    # Your Code Here
    try:
        diameter = nx.diameter(G_sc)
    except nx.exception.NetworkXError:
        print ('Found infinite path length because the graph is not connected')
        diameter = 0

    # print ('diameter:', diameter)

    return diameter # Your Answer Here


# ### Question 9
#
# Find the set of nodes in G_sc with eccentricity equal to the diameter
#
# [*Returns the set of the node(s)]


def answer_nine(G_sc, diameter):
    # Your Code Here
    try:
        ecc = nx.eccentricity(G_sc)
    except nx.exception.NetworkXError:
        print('Graph is not connected')
        ecc = 0

    ecc = {key: value for key, value in ecc.items() if value == diameter}

    # print ('Eccentricity: ', ecc)
    # print(list(ecc.keys()))

    return list(ecc.keys()) # Your Answer Here


# ### Question 10
#
# What is the set of node(s) in G_sc with eccentricity equal to the radius?
#
# [*Returns the set of the node(s)]


def answer_ten(G_sc):
    # Your Code Here
    try:
        ecc = nx.eccentricity(G_sc)
    except nx.exception.NetworkXError:
        print('Graph is not connected')
        ecc = 0

    try:
        radius = nx.radius(G_sc)
    except nx.exception.NetworkXError:
        print('Found infinite path length because the graph is not connected')
        radius = 0

    ecc = {key: value for key, value in ecc.items() if value == radius}

    # print ('Eccentricity: ', ecc)
    # print(list(ecc.keys()))

    return list(ecc.keys())  # Your Answer Here




# ### Question 11
#
# Find which node in G_sc is connected to the most other nodes by a shortest path of length equal to the diameter
# of G_sc
#
# Find the number of nodes that are connected to this node
#
# [*Returns a tuple (<name of node>, <number of satisfied connected nodes>)]


def answer_eleven(G_sc):
    # shortest path of length equal to the diameter => node must be in the periphery
    diameter = answer_eight(G_sc)
    periphery = answer_nine(G_sc,diameter)
    max_count = 0
    max_node = None
    for node in periphery:
        path_length = nx.shortest_path_length(G_sc, node)
        count = list(path_length.values()).count(diameter)
        if count > max_count:
            max_node = node
            max_count = count
    return (max_node, max_count)



# ### Question 12
#
# Assuming that we want to prevent the communication from flowing from the node that we found in question 11 from any
# node in the center of G_sc, detect the smallest number of nodes you would need to remove from the graph (you are not
# allowed to remove the node from the previous question or the center nodes).
#
# [*Returns an integer]

def answer_twelve(ans):
    try:
        cen = nx.center(G_sc)
    except nx.exception.NetworkXError:
        print('Graph is not connected')
        cen = {}
    print ('Central: ', cen)

    min_nodes_to_cut = nx.node_connectivity(G_sc, s=ans[0], t=cen[0])

    print(min_nodes_to_cut)

    return min_nodes_to_cut


# ### Question 13
#
#
# Create an undirected graph named G_un using G_sc (it is possible to ignore the attributes).
#
# [*Returns a NetworkX Graph (G_un)]

# In[ ]:

def answer_thirteen(G_sc):
    # Your Code Here

    if nx.is_directed(G_sc):
        G_un = nx.to_undirected(G_sc)
    else:
        G_un = G_sc

    # print(nx.is_directed(G_un))

    return  G_un # Your Answer Here


# ### Question 14
#
# Find the transitivity and the average clustering coefficient of graph G_un.
#
# [*Returns a tuple (<transitivity>, <avg_clustering_coefficient>]

# In[ ]:

def answer_fourteen(G_un):
    # Your Code Here
    G = nx.Graph(G_un)
    transitivity = nx.transitivity(G)
    avg_cc = nx.average_clustering(G)

    # print('Transitivity: ', transitivity)
    # print('Average clustering coefficient: ', avg_cc)

    # print((transitivity, avg_cc))

    return (transitivity, avg_cc) # Your Answer Here


MG = answer_one()
print (nx.info(MG))
print (answer_two(MG))
connection_tuple = answer_three(MG)
print (connection_tuple)
num_of_nodes_weakly = answer_four(MG)
print (num_of_nodes_weakly)
num_of_nodes_strongly = answer_five(MG)
print (num_of_nodes_strongly)
G_sc = answer_six(MG)
print (nx.info(G_sc))
avg = answer_seven(G_sc)
print ('average distance: ',avg)
diameter = answer_eight(G_sc)
print ('diameter: ',diameter)
ecc_keys = answer_nine(G_sc, diameter)
print ('set of nodes with eccentricity equal to the diameter: ',ecc_keys)
ecc_keys_radius = answer_ten(G_sc)
print ('set of nodes with eccentricity equal to the radius: ',ecc_keys_radius)
ans = answer_eleven(G_sc)
print ('node in G_sc is connected to the most other nodes by a shortest path of length equal to the diameter',ans)
min_nodes_to_cut = answer_twelve(ans)
print ('prevent the communication flow by removing node:',min_nodes_to_cut)
G_un = answer_thirteen(G_sc)
trans_avgcc = answer_fourteen(G_un)
print (trans_avgcc)