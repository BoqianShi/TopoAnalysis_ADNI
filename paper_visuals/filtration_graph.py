import networkx as nx
import matplotlib.pyplot as plt
# Generate a more complex graph for the final stage with more edges and weights
plt.rcParams.update({'font.size': 18})  # Adjust the number to your desired font size

G = nx.Graph()
edges_with_weights = [
    (1, 2, 2), (1, 4, 3), (3, 5, 4), (2, 5, 5), (4, 3, 5), 
    (1, 5, 4)
]
G.add_weighted_edges_from(edges_with_weights)
pos = {
    1: (0.2, 1), 
    2: (1.18, 1.2), 
    3: (0.9, 0.1),  
    4: (0, 0.3),  
    5: (0.5, 0.6)
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
max_filtration_step = 5

# Create the figure and axes, one row for the subgraphs, one for the barcode
fig, ax = plt.subplots(2, 1, figsize=(10, 8), gridspec_kw={'height_ratios': [1, 1]})

# Create a set of all nodes in the graph
all_nodes = set(G.nodes())

for idx, (step, subgraph) in enumerate(filtration_steps):
    # Add all nodes to the subgraph, even if they have no edges
    subgraph.add_nodes_from(all_nodes)
    
    # Determine the position for each subgraph plot
    # This should include positions for all nodes, not just those in the subgraph
    subpos = {node: (idx * 2 + pos[node][0], pos[node][1]) for node in all_nodes}
    
    # Draw the nodes and the edges
    nx.draw_networkx_nodes(subgraph, pos=subpos, ax=ax[0], node_size=50)
    nx.draw_networkx_edges(subgraph, pos=subpos, ax=ax[0])
    
    # Label each subgraph with its filtration step
    ax[0].text(idx * 2 + 0.5, -0.5, f'$G_{{w_{step}}}$', horizontalalignment='center')


# Set the top axis limits and turn off axis for this row
# Make sure the limit is large enough to accommodate all subgraphs
ax[0].set_xlim(-0.5, len(filtration_steps) * 2 - 0.2)
ax[0].set_ylim(-1, 1.5)
ax[0].axis('off')
ax[0].set_title('Graph on Different Thresholds')


components_over_time = {
    0: 5,
    1: 5,  # At step 1, there are 2 connected components
    2: 4,
    3: 3,
    4: 1,
    5: 1,
    6: 1
}

steps = sorted(components_over_time.keys())
counts = [components_over_time[step] for step in steps]
# Plot the single line that represents the connected component's number at different times
ax[1].step(steps, counts, where='post', linewidth=2)

# Set the limits and labels for the barcode plot
ax[1].set_xlim(0, max_filtration_step + 1)
ax[1].set_ylim(0, max(counts) + 1)
ax[1].set_xlabel('Weight Threshold (w)')
ax[1].set_ylabel('Beta_0')

# Set the x-tick labels to reflect w_i notation
ax[1].set_xticks(range(1, max_filtration_step + 1))
ax[1].set_xticklabels([f'$w_{{{i}}}$' for i in range(1, max_filtration_step + 1)])
ax[1].set_title('0D Barcode (Connected Components)')

# Show the plot
plt.tight_layout()
plt.show()
