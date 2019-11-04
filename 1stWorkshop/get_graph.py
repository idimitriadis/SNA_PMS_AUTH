import networkx as nx
import pickle

def load_hashtags_brexit():
    file = open('hashtags.txt','r')
    G=nx.Graph()
    G.name = 'Brexit Hashtags'
    for line in file:
        line = line.lower()
        details = line.split(',')
        d1=details[0].replace('\n','')
        d2=details[1].replace('\n','')
        if d1!=d2:
            G.add_edge(d1,d2)
    file.close()
    print (nx.info(G)+'\n')
    nx.write_edgelist(G,'brexit.csv')

def load_karate_club():
    G = nx.karate_club_graph()
    G.name = 'karate'
    print (nx.info(G))
    nx.write_edgelist(G,'karate.csv')

def generate_graph(words):
    from string import ascii_lowercase as lowercase
    G = nx.Graph(name="words")
    lookup = dict((c,lowercase.index(c)) for c in lowercase)
    def edit_distance_one(word):
        for i in range(len(word)):
            left, c, right = word[0:i], word[i], word[i+1:]
            j = lookup[c] # lowercase.index(c)
            for cc in lowercase[j+1:]:
                yield left + cc + right
    candgen = ((word, cand) for word in sorted(words)
               for cand in edit_distance_one(word) if cand in words)
    G.add_nodes_from(words)
    for word, cand in candgen:
        G.add_edge(word, cand)
    nx.write_edgelist(G,'words.csv')
    print (nx.info(G))
    return G

def words_graph():
    """
Words/Ladder Graph
------------------
Generate  an undirected graph over the 5757 5-letter words in the
datafile words_dat.txt.gz.  Two words are connected by an edge
if they differ in one letter, resulting in 14,135 edges. This example
is described in Section 1.1 in Knuth's book [1]_,[2]_.

References
----------
.. [1] Donald E. Knuth,
   "The Stanford GraphBase: A Platform for Combinatorial Computing",
   ACM Press, New York, 1993.
.. [2] http://www-cs-faculty.stanford.edu/~knuth/sgb.html
"""
    """Return the words example graph from the Stanford GraphBase"""
    import gzip
    fh=gzip.open('words_dat.txt.gz','r')
    words=set()
    for line in fh.readlines():
        line = line.decode()
        if line.startswith('*'):
            continue
        w=str(line[0:5])
        words.add(w)
    return generate_graph(words)


load_karate_club()
words_graph()
load_hashtags_brexit()
