import networkx as nx
import matplotlib.pyplot as plt
# Generate a more complex graph for the final stage with more edges and weights
G = nx.Graph()
edges_with_weights = [
    (1, 2, 1), (1, 3, 1), (1, 4, 2), (2, 3, 2), (2, 5, 3), 
    (3, 4, 3), (3, 6, 4), (4, 5, 4), (4, 7, 5), (5, 6, 5),
    (6, 7, 6)
]
G.add_weighted_edges_from(edges_with_weights)
pos = {
    1: (1, 0), 
    2: (0.8, 1.2), 
    3: (0.6, 0.4),  
    4: (1.23, 1),  
    5: (0.5, 0.45), 
    6: (0.8, 0.12),   
    7: (0.3, 0.5)   
}

# When drawing, we use the pos dictionary
# nx.draw(G, pos, with_labels=True, node_size=700)
# Define the layout of the network graphs
# Determine the filtration steps: at each step, add the edges with weight equal or less than the step
filtration_steps = []
for i in range(1, max(weight for _, _, weight in edges_with_weights) + 1):
    edges_at_step = [(u, v) for u, v, weight in edges_with_weights if weight <= i]
    filtration_steps.append((i, nx.Graph(edges_at_step)))
# Adjust the maximum weight for the filtration steps
 # Adjust the last filtration step to not be too far right
# Since the max weight is 6, we set the limit to 7 for a tighter fit
max_filtration_step = 7

# Create the figure and axes, one row for the subgraphs, one for the barcode
fig, ax = plt.subplots(2, 1, figsize=(16, 8), gridspec_kw={'height_ratios': [1, 1]})
# Plot the subgraphs horizontally on the top row
for idx, (step, subgraph) in enumerate(filtration_steps):
    # Determine the position for each subgraph plot
    subpos = {node: (idx * 2 + pos[node][0], pos[node][1]) for node in subgraph.nodes()}
    nx.draw_networkx(subgraph, pos=subpos, ax=ax[0], node_size=50)
    # Label each subgraph with its filtration step
    ax[0].text(idx * 2 + 0.5, -0.5, f'$G_{{w_{step}}}$', horizontalalignment='center')

# Set the top axis limits and turn off axis for this row
# Make sure the limit is large enough to accommodate all subgraphs
ax[0].set_xlim(-0.5, len(filtration_steps) * 2 - 0.2)
ax[0].set_ylim(-1, 1.5)
ax[0].axis('off')
ax[0].set_title('Filtration of Graphs')

# Plot the barcode on the bottom row
for edge in edges_with_weights:
    node_label = f'w_{edge[2]}'  # This changes the label to w_1, w_2, etc.
    birth = edge[2]
    ax[1].hlines(y=node_label, xmin=birth, xmax=8, color='black', linewidth=2)  # xmax is now set to 8

# Set the limits and labels for the barcode plot
ax[1].set_xlim(0, max_filtration_step + 1)
ax[1].set_ylim(-1, 8)
ax[1].set_xlabel('Filtration step')
ax[1].set_ylabel('Edge birth')
# Update the y-tick labels to reflect w_i notation
ax[1].set_yticks(range(8))
ax[1].set_yticklabels([f'$w_{{{i}}}$' for i in range(1, 8)] + [''])
ax[1].set_title('Barcode of Edge Birth')


# Add additional lines to connect the subgraphs to the barcode points
for idx, edge in enumerate(edges_with_weights):
    birth = edge[2]
    ax[1].vlines(x=birth, ymin=0, ymax=idx+1, color='black', linestyles='dashed', linewidth=1)

# Show the plot
plt.tight_layout()
plt.show()
