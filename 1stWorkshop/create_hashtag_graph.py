import networkx as nx
import pickle

def load_hashtags_brexit():
    file = open('hashtags.txt','r')
    G=nx.Graph()
    for line in file:
        line = line.lower()
        details = line.split(',')
        d1=details[0].replace('\n','')
        d2=details[1].replace('\n','')
        if d1!=d2:
            G.add_edge(d1,d2)
    file.close()
    print (nx.info(G))
    nx.write_edgelist(G,'brexit1.csv')

load_hashtags_brexit()


