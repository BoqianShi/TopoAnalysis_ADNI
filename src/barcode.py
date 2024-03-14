# barcode.py
# Functions for generating barcode representation of the network
# Author: Boqian Shi

import numpy as np
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import minimum_spanning_tree
from matplotlib import pyplot as plt

def bd_decomposition(adj):
    """
    Birth-death decomposition of a network adjacency matrix.

    Args:
        adj (numpy.ndarray): Adjacency matrix of the network.

    Returns:
        tuple: A tuple containing the minimum spanning tree (MST) and the non-MST edges.
    """
    eps = np.nextafter(0, 1)
    adj[adj == 0] = eps
    adj = np.triu(adj, k=1)
    Xcsr = csr_matrix(-adj)
    Tcsr = minimum_spanning_tree(Xcsr)
    mst = -Tcsr.toarray()  # Reverse the negative sign
    nonmst = adj - mst
    return mst, nonmst

def compute_birth_sets(mst):
    """
    Computes birth sets of a network.
    Representing components in the networks.

    Args:
        adj (numpy.ndarray): Adjacency matrix of the network.

    Returns:
        tuple: A tuple containing the sorted birth set and the sorted death set.
    """
    birth_ind = np.nonzero(mst)
    # death_ind = np.nonzero(nonmst)
    return np.sort(mst[birth_ind])

def compute_death_sets(nonmst):
    """
    Computes birth sets of a network.
    Representing components in the networks.

    Args:
        adj (numpy.ndarray): Adjacency matrix of the network.

    Returns:
        tuple: A tuple containing the sorted birth set and the sorted death set.
    """
    # birth_ind = np.nonzero(mst)
    death_ind = np.nonzero(nonmst)
    return np.sort(nonmst[death_ind])


def set_mode(adj, mode='original'):
    """
    Set mode for the adjacaency matrix.

    Args:
        adj (numpy.ndarray): Adjacency matrix of the network.
        mode (str): Mode of processing the barcode.
            'original': Use the original adjacency matrix.
            'ignore_negative': Ignore negative values in the adjacency matrix.
            'absolute': Take the absolute values of the adjacency matrix.

    Returns:
        list: A list containing the birth and death sets of the network.
    """
    if mode == 'ignore_negative':
        adj = np.where(adj < 0, 0, adj)
    elif mode == 'absolute':
        adj = np.abs(adj)

    return adj

def get_barcode(adj, mode = "cycles", barcode_mode = "ignore_negative"):
    """
    Computes the barcode representation of a network.

    Args:
        adj (numpy.ndarray): Adjacency matrix of the network.
        mode (string): Use components, cycles, or attached methods to generate barcode
            options: 1. "components"
                     2. "cycles"
                     3. "attached"

    Returns:
        list: A list containing the birth and death sets of the network.
    """
    X = []
    adj = set_mode(adj, barcode_mode)
    mst, nonmst = bd_decomposition(adj)
    if mode == "cycle":
        X.append(compute_death_sets(nonmst))
    elif mode == "components":
        X.append(compute_birth_sets(mst))
    elif mode == "attached":
        X.append(compute_birth_sets(mst), compute_death_sets(nonmst))
    else:
        print("invalid mode in barcode generation")
    return X

def plot_barcode(births, deaths, title="Barcode"):
    """
    Plots the barcode representation of a network.

    Args:
        births (numpy.ndarray): Array of birth values.
        deaths (numpy.ndarray): Array of death values.
        title (str, optional): Title of the plot. Defaults to "Barcode".
    """
    plt.figure(figsize=(10, 5))  # Increased figure size for clarity
    for i, (birth, death) in enumerate(zip(births, deaths)):
        plt.plot([birth, death], [i, i], 'k', lw=0.5, alpha=0.5)  # Decreased line width and added transparency
    plt.title(title)
    plt.xlabel("Feature Lifetime")
    plt.ylabel("Feature Index")
    plt.grid(True)
    plt.yticks([])  # Remove y-ticks for clarity
    plt.tight_layout()  # Adjust layout to fit the figure size
    plt.show()