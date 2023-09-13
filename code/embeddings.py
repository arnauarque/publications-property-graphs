import sys
import networkx as nx
from node2vec import Node2Vec
from node2vec.edges import HadamardEmbedder
from gensim.models import Word2Vec
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE
from sklearn.decomposition import PCA
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegressionCV
from sklearn.metrics import accuracy_score, confusion_matrix
import numpy as np
import pandas as pd
from data_generator import welcomeMsg, infomsg


# Method to print a summary of the graph obtained as a parameter
def print_summary(g):
    title = '[Graph summary]\n'
    ninfo = '\tNodes: %d\n' % len(g.nodes())
    einfo = '\tEdges: %d\n' % len(g.edges())
    head = '--------'+''.join(['-' for _ in range(len(max(ninfo,einfo)))])+'\n'
    print(head, title, ninfo, einfo, head, sep='')


# Method to get the specific-typed nodes of a graph
def get_nodes(g, type, data=True):
    nodes = [(n,d) if data else n \
                for n,d in g.nodes(data=True) \
                if d['labels'] == ':%s' % type]
    return nodes


# Method to obtain the nodes of a graph as a pandas DataFrame
def nodes_to_df(g):
    df = pd.DataFrame([ n for n in g.nodes(data=True) ])
    return df


# Method to plot the embeddings passed as a parameter
def plot_embeddings(node_embeddings, node_targets):
    transforms = [TSNE, PCA]
    for transform in transforms: 
        trans = transform(n_components=2)
        node_embeddings_2d = trans.fit_transform(node_embeddings)
        
        alpha = 0.7
        label_map = {l: i for i, l in enumerate(np.unique(node_targets))}
        node_colours = [label_map[target] for target in node_targets]

        plt.figure(figsize=(8,8))
        plt.scatter(
            node_embeddings_2d[:, 0],
            node_embeddings_2d[:, 1],
            c=node_colours,
            cmap="jet",
            alpha=alpha,
        )
        plt.title("{} visualization of node embeddings".format(transform.__name__))
        plt.show()


# Method to get the node embeddings of a graph given a model
def get_embeddings(g, model, num):
    embeddings = model.wv.vectors
    labels = get_model_labels(g, model)
    if num:
        translator = labels_to_ids(g)
        labels = [ translator[lab] for lab in labels ]
    return embeddings, np.array(labels)


# Method to convert the labels of a graph as a dictionary with IDS
def labels_to_ids(g):
    labels = [d['labels'] for _,d in g.nodes(data=True)]
    unique_labels = np.sort(np.unique(labels))
    ids = {t:i for i,t in enumerate(unique_labels)}
    return ids


# Method to convert the labels of a graph as a dictionary with IDS
def ids_to_labels(g):
    labels = [d['labels'] for _,d in g.nodes(data=True)]
    unique_labels = np.sort(np.unique(labels))
    ids = {i:t for i,t in enumerate(unique_labels)}
    return ids


# Method to get the unique lables of the nodes of a given graph
def get_labels(g):
    labels = [ d['labels'].split(':')[-1] for _,d in g.nodes(data=True) ]
    return np.sort(np.unique(labels))


# Method to get the true labels associated to each embedding
def get_model_labels(g, model):
    labels = []
    for key in model.wv.index_to_key: 
        found = False
        for n,d in g.nodes(data=True):
            if key == n: 
                labels.append(d['labels'])
                found = True
                break
        if not found:
            print('[WARNING] Label not found for node \'%s\'' % key)
    return np.array(labels)
    

## -------------------------------------------------------------------------
## -- Main program
## -------------------------------------------------------------------------
if __name__ == '__main__':
    
    welcomeMsg('Embeddings program')
    
    infomsg('Loading graph NetworkX graph...')
    g = nx.read_graphml('./data/graph.graphml')
    print_summary(g)
    
    infomsg('Generating embeddings...')
    node2vec = Node2Vec(g, dimensions=10, walk_length=5, num_walks=10, p=2, q=2, workers=1)
    n2v_model = node2vec.fit(window=3, min_count=1, batch_words=4)
    
    infomsg('Showing embeddings...', pre='\n')
    emb, tar = get_embeddings(g, n2v_model, num=False)
    plot_embeddings(emb,tar)
    
    infomsg('Training model...')
    emb, tar = get_embeddings(g, n2v_model, num=True)
    
    x_train, x_test, y_train, y_test = train_test_split(emb, tar, train_size=0.8, test_size=None)
    
    info = 'Array shapes:\n\tX_train = {}\n\ty_train = {}\n\tX_test = {}\n\ty_test = {}'
    print(info.format(x_train.shape, y_train.shape, x_test.shape, y_test.shape))
    
    clf = LogisticRegressionCV(Cs=10, 
                               cv=10, 
                               scoring="accuracy", 
                               verbose=False, 
                               multi_class="ovr", 
                               max_iter=300)
    clf.fit(x_train, y_train)
    
    y_pred = clf.predict(x_test)
    acc = accuracy_score(y_test, y_pred)
    
    cm = pd.DataFrame(confusion_matrix(y_test, y_pred),
                      columns = get_labels(g), 
                      index = get_labels(g))
    print('\n[CONFUSION MATRIX]')
    print(cm.to_latex())
    
    print('\n[ACCURACY] %.3f\n' % acc)
    