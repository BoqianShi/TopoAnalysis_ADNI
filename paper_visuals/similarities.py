import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial.distance import pdist, squareform

def set_mode(adj, mode='original'):
    if mode == 'ignore_negative':
        adj = np.where(adj < 0, 0, adj)
    elif mode == 'absolute':
        adj = np.abs(adj)
    return adj

def calculate_group_averages(subjects):
    """
    Calculate the average adjacency matrix for each group.
    """
    mode = "original"
    group_matrices = {'AD': [], 'LMCI': [], 'EMCI': [], 'CN': []}
    for subject in subjects:
        group_matrices[subject.group].append(set_mode(subject.data, mode))
    
    group_averages = {}
    for group, matrices in group_matrices.items():
        group_averages[group] = np.mean(matrices, axis=0)
    
    return group_averages

def compute_dissimilarity_between_groups(group_averages):
    """
    Compute the dissimilarity between each pair of group averages.
    """
    groups = list(group_averages.keys())
    dissimilarity_matrix = np.zeros((len(groups), len(groups)))
    
    for i, group1 in enumerate(groups):
        for j, group2 in enumerate(groups):
            if i <= j:  # Compute only for one triangle and mirror it as the matrix is symmetric
                dissimilarity = np.linalg.norm(group_averages[group1] - group_averages[group2], 'fro')
                dissimilarity_matrix[i, j] = dissimilarity
                dissimilarity_matrix[j, i] = dissimilarity
                
    return dissimilarity_matrix, groups

def visualize_similarity(similarity_matrix, groups):
    """
    Visualize the similarity matrix with a white background and black font.
    """
    fig, ax = plt.subplots()
    # Use a white background
    ax.imshow(np.ones_like(similarity_matrix), cmap='Greys', vmin=0, vmax=1, aspect='auto')
    
    # Show the similarity scores in black font
    for (i, j), z in np.ndenumerate(similarity_matrix):
        ax.text(j, i, '{:0.3f}'.format(z), ha='center', va='center', color='white')
    
    # Set group names as labels
    ax.set_xticks(np.arange(len(groups)))
    ax.set_yticks(np.arange(len(groups)))
    ax.set_xticklabels(groups)
    ax.set_yticklabels(groups)
    
    plt.xticks(rotation=90)
    plt.show()
