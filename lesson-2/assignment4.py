# # 4th Assignment
import pickle
import time
import networkx as nx
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import MinMaxScaler

# ## Part 1 - Company Mails
#
# The second part of this assignment involves work with a company's mail network, once again. This time, each node
# corresponds to a person in the company, while each edge indicates that one mail at least has been sent between two
# people.
#
# The node attributes `Department` and `ManagementSalary` are also included in the network
#  * `Department` - the department in the company which the person belongs to.
#  * `ManagementSalary` - whether the person is receiving a salary for a management position.
#
### Part 1 - Create the Graph
#
# In the data folder, you will find two pickle files that contain all the edges *edge_list*, nodes *node_list*
# and their attributes.
# First of all, your task is to create a node attributed graph using the files above.
# To make sure that your Graph is identical to the expected one, the expected one is also provided below (see Lines 28-31)

G = pickle.load(open('data/email_prediction.pkl','rb'))
# print(nx.info(G))
# for n in G.nodes(data=True):
#     print (n)

def create_the_email_graph():
    G = nx.Graph()
    G.add_edges_from(pickle.load(open('data/edge_list','rb')))
    G.add_nodes_from(pickle.load(open('data/node_list','rb')))
    return  G



# ### Part 1A - Salary Prediction
#
# By using the network `G`, detect the people in the network that have missing value for the node attribute
# `ManagementSalary` and predict if these people are receiving a management position salary.
#
# To achieve this, you need to
#   1. Create a matrix of node features using NetworkX.
#   2. Train a sklearn classifier using nodes that have `ManagementSalary` data.
#   3. Predict a probability of the node (person) receiving a management salary for all the nodes where
#      `ManagementSalary` is missing.
#
# Predictions will need to be given as the probability that an employ is receiving the salary for the management
# position.

def in_management(node):
    management=node[1]['ManagementSalary']
    if management==0:
        return 0
    elif management==1:
        return 1
    else:
        return None

def in_management(node):
    management=node[1]['ManagementSalary']
    if management==0:
        return 0
    elif management==1:
        return 1
    else:
        return None

def predict_salary_type():
    df = pd.DataFrame(index=G.nodes())
    df['clustering'] = pd.Series(nx.clustering(G))
    df['degree_centrality'] = pd.Series(nx.degree_centrality(G))
    df['closeness'] = pd.Series(nx.closeness_centrality(G, wf_improved = True))
    df['betweeness'] = pd.Series(nx.betweenness_centrality(G, normalized=True))
    df['pr'] = pd.Series(nx.pagerank(G))
    df['is_management'] = pd.Series([in_management(node) for node in G.nodes(data=True)])
    df_train = df[~pd.isnull(df['is_management'])]
    df_test = df[pd.isnull(df['is_management'])]
    features = ['clustering',  'degree_centrality', 'closeness', 'betweeness', 'pr']
    X_train = df_train[features]
    Y_train = df_train['is_management']
    X_test = df_test[features]
    scaler = MinMaxScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    clf = MLPClassifier(hidden_layer_sizes = [10, 5], alpha = 5,
                       random_state = 0, solver='lbfgs', verbose=0)
    clf.fit(X_train_scaled, Y_train)
    test_proba = clf.predict_proba(X_test_scaled)[:, 1]
    results =  pd.Series(test_proba,X_test.index)
    results = results.sort_values(ascending=False)
    return results

# print (predict_salary_type())

# ### Part 1B - New Connections Prediction
#
# As a last part of this assignment, you are required to predict the future connections between the network's employees.
# Information regarding the future connections are loaded below into the `future_connections` variable.
# The index is a tuple that indicates a node pair that currently does not have a connection, while the
# `Future Connection` column declares whether an edge between those nodes will exist in the future. A value of 1.0
# indicates a future connection.

future_connections = pd.read_csv('data/future_connections.csv', index_col=0, converters={0: eval})
# print (future_connections.head(10))


# Use network `G` and the `future_connections` variable to identify the edges in `future_connections` with missing
# values and predict whether or not these edges will have a connection in the future.
#
# To achieve this, you should create a matrix of features for all the edges found in `future_connections`, using
# NetworkX. Then, train a sklearn classifier on those edges in `future_connections` which have a `Future_Connection`
# data. Finally, predict the probability of the edge being a future connection for all the edges in `future_connections`
# where `Future_Connection` is missing
#
# Use your trained classifier and return a series of length 122112 with the index being the edge represented by a tuple
# of nodes and the value being the probability (0-1) of the edge being in a future connection.
#
#     Example:
#
#         (107, 348)    0.35
#         (542, 751)    0.40
#         (20, 426)     0.55
#         (50, 989)     0.35
#                   ...
#         (939, 940)    0.15
#         (555, 905)    0.35
#         (75, 101)     0.65
#         Length: 122112, dtype: float64


def new_connections_predictions():
    df = future_connections
    df['jaccard_coefficient'] = [x[2] for x in nx.jaccard_coefficient(G, df.index)]
    df['resource_allocation_index'] = [x[2] for x in nx.resource_allocation_index(G, df.index)]
    df['preferential_attachment'] = [x[2] for x in nx.preferential_attachment(G, df.index)]
    df['common_neighbors'] = df.index.map(lambda ind: len(list(nx.common_neighbors(G, ind[0], ind[1]))))
    print ('.......we have extracted all the features......')
    df_train = df[~pd.isnull(df['Future Connection'])]
    df_test = df[pd.isnull(df['Future Connection'])]
    features = ['jaccard_coefficient', 'resource_allocation_index', 'preferential_attachment', 'common_neighbors']
    X_train = df_train[features]
    Y_train = df_train['Future Connection']
    X_test = df_test[features]
    scaler = MinMaxScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    clf = LogisticRegression(solver='liblinear', random_state=14)
    clf.fit(X_train_scaled, Y_train)
    predictions = np.round(clf.predict_proba(X_test_scaled)[:, 1], 2)
    results = pd.Series(data=predictions, index=X_test.index)
    results = results.sort_values(ascending=False)
    return results



# print (new_connections_predictions())