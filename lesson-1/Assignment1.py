
# coding: utf-8

# # Assignment 1 - Creating and Manipulating Graphs
#
# Eight employees at a small company were asked to choose 3 movies that they would most enjoy watching for the upcoming company movie night. These choices are stored in the file `Employee_Movie_Choices.txt`.
#
# A second file, `Employee_Relationships.txt`, has data on the relationships between different coworkers.
#
# The relationship score has value of `-100` (Enemies) to `+100` (Best Friends). A value of zero means the two employees haven't interacted or are indifferent.
#
# Both files are tab delimited.

# In[ ]:

import networkx as nx
import pandas as pd
import numpy as np
from networkx.algorithms import bipartite


# This is the set of employees
employees = set(['Pablo',
                 'Lee',
                 'Georgia',
                 'Vincent',
                 'Andy',
                 'Frida',
                 'Joan',
                 'Claude'])

# This is the set of movies
movies = set(['The Shawshank Redemption',
              'Forrest Gump',
              'The Matrix',
              'Anaconda',
              'The Social Network',
              'The Godfather',
              'Monty Python and the Holy Grail',
              'Snakes on a Plane',
              'Kung Fu Panda',
              'The Dark Knight',
              'Mean Girls'])


# you can use the following function to plot graphs
# make sure to comment it out before submitting to the autograder
def plot_graph(G,type=1):
    import matplotlib.pyplot as plt
    plt.figure()
    pos = nx.spring_layout(G)
    edges = G.edges()
    if type==1:
      nx.draw_networkx(G, pos, edges=edges)
    elif type==2:
      color_map=[]
      for node,at in G.nodes(data=True):
        if at['type']=='movie':
          color_map.append('blue')
        else: color_map.append('red')
      nx.draw(G,pos,node_color=color_map,with_labels=True)
    elif type==3:
      nx.draw_networkx(G, pos, edges=edges)
    plt.show()



# ### Question 1
#
# Using NetworkX, load in the bipartite graph from `Employee_Movie_Choices.txt` and return that graph.
#
# *This function should return a networkx graph with 19 nodes and 24 edges*

# In[ ]:

def answer_one():
  graph = nx.read_edgelist("graphs/Employee_Movie_Choices.txt", delimiter="\t")
  return graph


# ### Question 2
#
# Using the graph from the previous question, add nodes attributes named `'type'` where movies have the value `'movie'` and employees have the value `'employee'` and return that graph.
#
# *This function should return a networkx graph with node attributes `{'type': 'movie'}` or `{'type': 'employee'}`*

# In[ ]:

def answer_two():
  import matplotlib.pyplot as plt
  graph = answer_one()
  for node in graph.nodes():
    if node in movies:
      graph.nodes[node]['type'] = 'movie'
    elif node in employees:
      graph.nodes[node]['type'] = 'employee'
  return graph


# ### Question 3
#
# Find a weighted projection of the graph from `answer_two` which tells us how many movies different pairs of employees have in common.
#
# *This function should return a weighted projected graph.*

# In[ ]:

def answer_three():
  graph = answer_two()
  projection = bipartite.weighted_projected_graph(graph, employees)
  return projection


# ### Question 4
#
# Suppose you'd like to find out if people that have a high relationship score also like the same types of movies.
#
# Find the Pearson correlation ( using `DataFrame.corr()` ) between employee relationship scores and the number of movies they have in common. If two employees have no movies in
#common it should be treated as a 0, not a missing value, and should be included in the correlation calculation.
#
# *This function should return a float.*

# In[ ]:

def answer_four():
    # Your Code Here
    G = answer_two()
    E = bipartite.weighted_projected_graph(G, employees)

    relationship_df = pd.read_csv('graphs/employee_relationships.txt', delim_whitespace=True, header=None, names=["E1", "E2", "Relationship"])
    relationship_g = nx.from_pandas_edgelist(relationship_df, "E1", "E2", edge_attr="Relationship")
    weight_attr = {(i[0], i[1]): i[2] for i in E.edges(data="weight")}
    nx.set_edge_attributes(relationship_g, 0, "Shared_Movies")
    nx.set_edge_attributes(relationship_g, weight_attr, "Shared_Movies")
    idx = [(i[0], i[1]) for i in relationship_g.edges(data=True)]
    relationship = [i[2] for i in relationship_g.edges(data="Relationship")]
    movies = [i[2] for i in relationship_g.edges(data="Shared_Movies")]
    correlation_df = pd.DataFrame({"Relationship": relationship, "Shared_Movies": movies}, index=idx)
    print (correlation_df)
    correlation_pearson = correlation_df.corr("pearson")
    print (correlation_pearson)

G = answer_one()
G = answer_two()
G = answer_three()
plot_graph(G,type=3)
answer_four()