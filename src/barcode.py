# barcode.py
# Functions for generating barcode representation of the network
# Author: Boqian Shi

import numpy as np
import config
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

def compute_mst_sets(mst):
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

def compute_nonmst_sets(nonmst):
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

def get_barcode(adj, barcode_mode = "attached", adj_mode = "ignore_negative", l = 1):
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
    adj = set_mode(adj, adj_mode)
    mst, nonmst = bd_decomposition(adj)
    if config.geo_mode == "topo":
        # Cycle number 64261
        if barcode_mode == "cycle":
            return compute_nonmst_sets(nonmst)
        # Component number 359
        elif barcode_mode == "component":
            return compute_mst_sets(mst)
        # Attached number 64620
        elif barcode_mode == "attached":
            return np.concatenate((compute_mst_sets(mst), compute_nonmst_sets(nonmst)), axis=0)
        else:
            print("invalid mode in barcode generation in topo-only mode")
    else: 
        if l == 1:
            vec = adj[np.triu_indices(adj.shape[0], k=1)]
            return np.concatenate((vec, compute_mst_sets(mst), compute_nonmst_sets(nonmst)), axis=0)
        else: 
            # print("lambda changed", l)
            vec = adj[np.triu_indices(adj.shape[0], k=1)]
            vec_scaled = vec * (1 - l)
        
        # Assuming compute_mst_sets(mst) and compute_nonmst_sets(nonmst) return numpy arrays
            mst_scaled = compute_mst_sets(mst) * l
            nonmst_scaled = compute_nonmst_sets(nonmst) * l  # If you need to multiply this by l, do it here similarly
            
            # Use np.concatenate with a tuple containing all arrays to concatenate
            barcode = np.concatenate((vec_scaled, mst_scaled, nonmst_scaled), axis=0)
            return barcode



# Every connected component has a death value at ∞
# In this case, we set it to 1 for better visualization
def plot_component_barcode(births, title="Component Barcode"):
    """
    Plots the component barcode representation of a network.

    Args:
        births (numpy.ndarray): Array of birth values.
        title (str, optional): Title of the plot. Defaults to "Component Barcode".
    """
    plt.figure(figsize=(10, 5))  # Increased figure size for clarity
    for i, birth in enumerate(births):
        plt.plot([birth, 1], [i, i], 'k', lw=0.5, alpha=0.5)  # Decreased line width and added transparency
    plt.title(title)
    plt.xlabel("Feature Lifetime")
    plt.ylabel("Feature Index")
    plt.grid(True)
    plt.yticks([])  # Remove y-ticks for clarity
    plt.tight_layout()  # Adjust layout to fit the figure size
    plt.show()

# Cycles in the graph filtration are all considered born at −∞
# In this case, we set it to 0 or -1 for better visualization
def plot_cycle_barcode(deaths, title="Cycle Barcode"):
    """
    Plots the cycle barcode representation of a network.

    Args:
        deaths (numpy.ndarray): Array of death values.
        title (str, optional): Title of the plot. Defaults to "Cycle Barcode".
    """
    plt.figure(figsize=(10, 5))  # Increased figure size for clarity
    for i, death in enumerate(deaths):
        if config.adj_mode == "ignore_negative" or config.adj_mode == "absolute":
            birth = 0
        elif config.adj_mode == "original":
            birth = -1
        plt.plot([birth, death], [i, i], 'k', lw=0.5, alpha=0.5)  # Decreased line width and added transparency
    plt.title(title)
    plt.xlabel("Feature Lifetime")
    plt.ylabel("Feature Index")
    plt.grid(True)
    plt.yticks([])  # Remove y-ticks for clarity
    plt.tight_layout()  # Adjust layout to fit the figure size
    plt.show()
