# # 3rd Assignment
#
# This assignment will enable you to explore measure of centrality on two networks, a friendship network and a blog
# network.

# ## Part 1
#
# This part of the assignment (questions 1-4) can be answered by using the network `G1` (a network of friendships at a
# university department). Every node corresponds to a person, and every edge represents a friendship.
#
# *The network is loaded as a networkx graph object `G1`.*

import networkx as nx


# nx.write_edgelist(G1, "uni_friends.csv")
# G = graphLoad.load_karate_club()
# print (nx.voterank(G))
# ### Question 1
#
# Calculate the degree centrality, closeness centrality and normalized betweeness centrality (excluding endpoints) of
# the node #100.
#
# [*Return a tuple of floats (<degree_centrality>, <closeness_centrality>, <betweenness_centrality>)]


def answer_one():
    degree_centrality = nx.degree_centrality(G1)
    closeness_centrality = nx.closeness_centrality(G1)
    betweenness_centrality = nx.betweenness_centrality(G1,endpoints=False,normalized=True)

    return  (degree_centrality[100], closeness_centrality[100], betweenness_centrality[100])

# #### For Questions 2, 3, and 4, we will assume that we don't know anything about the network structure, except for
#all the centrality values of the nodes. Based on this, use one of the covered centrality measures in order to
# rank the nodes and find the most appropriate candidate.

# ### Question 2
#
# Supposedly you are hired by an online e-commerce website and you are tasked with selecting one user in network G1 to
# whom you will send an online shopping voucher. Let's suppose that the user that will receive the voucher will promote and send
# it to their friends in the network. We want the voucher to reach as many nodes as possible. While the voucher can be
# forwarded to multiple users at the same time, the travel distance of the voucher is limited to one step, which means
# that if the voucher travels more than one step in the network, it is no longer valid. Use your knowledge in network
# centrality to select the best candidate for the voucher.
#
# [*Returns an integer, the name of the node.]


def answer_two():
    degree_centrality = nx.degree_centrality(G1)
    best_candidate = max(degree_centrality.items(), key = lambda x: x[1])

    return best_candidate[0]

# print (answer_two())

# ### Question 3
#
# For this question, the limit for the voucher's travel distance is removed. Due to the fact that the network is
# connected, regardless of who you pick, all nodes in the network will eventually receive the voucher. However, the
# point of this question is to ensure that the voucher reaches the nodes in the lowest possible average number of hops.
#
# Change your voucher selection strategy accordingly and write the code to find the best candidate in the network.
#
#
# [*Returns an integer, the name of the node]


def answer_three():
    closeness_centrality = nx.closeness_centrality(G1)
    best_candidate = max(closeness_centrality.items(), key = lambda x: x[1])

    return best_candidate[0]

# print (answer_three())

# ### Question 4
#
# Assuming that the restriction on the voucher's travel distance is still removed, similarly to the previous question,
# but now a competitor company has developed a strategy to remove a person from the network in order to disrupt the
# distribution of your voucher. More specifically, your competitor is targeting people (nodes) who are often information
# flow bridges between other groups of people.
#
# Find the one, riskiest person that the competitor company can remove from your network.
#
# [*Returns an integer, the name of the node]

def answer_four():
    betweenness_centrality = nx.betweenness_centrality(G1)
    best_candidate = max(betweenness_centrality.items(), key = lambda x: x[1])

    return best_candidate[0]

# print (answer_four())
# ## Part 2
#
# Graph `G2` is a directed graph network of political blogs, in which nodes correspond to a single blog and edges
# correspond to links between blogs. Utilize your knowledge of PageRank and HITS to answer the following questions (5-9)

# ### Question 5
#
# Use the Scaled Page Rank Algorithm on this network. Find the Page Rank of node 'realclearpolitics.com' with a damping
# value of 0.85
#
# [*Returns a float]


def answer_five():
    blogs = nx.pagerank(G2, alpha=0.85)
    blog = blogs['realclearpolitics.com']

    return blog


# ### Question 6
#
# Use the Scaled Page Rank Algorithm on this network with a damping value of 0.85 in order to find the 5 nodes with the
# highest Page Rqank.
#
# [*Returns a list of the top 5 blogs in desending order of Page Rank]


def answer_six():
    blogs = nx.pagerank(G2, alpha=0.85)
    top_five_blogs = sorted(blogs.items(), key=lambda x: x[1], reverse=True)[:5]
    result = [i[0] for i in top_five_blogs]

    return result


# ### Question 7
#
# Use the HITS Algorithm on the network to find the authority and hub scores of node 'realclearpolitics.com'
#
# [*Return tuple of floats (<authority_score>, <hub_score>)]


def answer_seven():
    blogs = nx.hits(G2)
    result = (blogs[0]['realclearpolitics.com'], blogs[1]['realclearpolitics.com'])

    return result


# ### Question 8
#
# Use the HITS Algorithm on this network to find the top 5 nodes with the highest hub scores.
#
# [*Returns a list of the top 5 blogs (nodes) in descending order according to the hub score]


def answer_eight():
    blogs = nx.hits(G2)
    top_five_blogs = sorted(blogs[0].items(), key=lambda x: x[1], reverse=True)[:5]
    result = [i[0] for i in top_five_blogs]

    return result


# ### Question 9
#
# Use the HITS Algorithm on this network to find the top 5 nodes with the highest authority scores.
#
# [*Returns a list of the top 5 blogs (nodes) in descending order according to the authority score]


def answer_nine():
    blogs = nx.hits(G2)
    top_five_blogs = sorted(blogs[1].items(), key=lambda x: x[1], reverse=True)[:5]
    result = [i[0] for i in top_five_blogs]

    return result

if __name__ == "__main__":
    G1 = nx.read_gml('data/university_friendships.gml')
    G2 = nx.read_gml('data/blogs.gml')
    print (answer_one())
    print (answer_two())
    print (answer_three())
    print (answer_four())
    print (answer_five())
    print (answer_six())
    print (answer_seven())
    print (answer_eight())
    print (answer_nine())