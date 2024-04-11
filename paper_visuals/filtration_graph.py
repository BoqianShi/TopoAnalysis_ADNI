import networkx as nx
import matplotlib.pyplot as plt
# Generate a more complex graph for the final stage with more edges and weights
plt.rcParams.update({'font.size': 18})  # Adjust the number to your desired font size

G = nx.Graph()
edges_with_weights = [
    (1, 2, 3), (1, 4, 2), (2, 5, 5), (4, 3, 6), 
    (1, 5, 5), (4, 5, 6), (2, 3, 6), (3, 5, 4)
]
G.add_weighted_edges_from(edges_with_weights)
pos = {
    1: (0.2, 1), 
    2: (1.18, 1.2), 
    3: (0.9, 0.1),  
    4: (0, 0.3),  
    5: (0.5, 0.6)
}

filtration_steps = []
for i in range(1, max(weight for _, _, weight in edges_with_weights) + 1):
    edges_at_step = [(u, v) for u, v, weight in edges_with_weights if weight <= i]
    filtration_steps.append((i, nx.Graph(edges_at_step)))

max_filtration_step = 6

fig, ax = plt.subplots(2, 1, figsize=(10, 8), gridspec_kw={'height_ratios': [1, 1]})
all_nodes = set(G.nodes())

for idx, (step, subgraph) in enumerate(filtration_steps):
    subgraph.add_nodes_from(all_nodes)
    # Calculate position for the reversed plotting order
    reversed_idx = len(filtration_steps) - idx - 1
    subpos = {node: (reversed_idx * 2 + pos[node][0], pos[node][1]) for node in all_nodes}
    
    nx.draw_networkx_nodes(subgraph, pos=subpos, ax=ax[0], node_size=50)
    nx.draw_networkx_edges(subgraph, pos=subpos, ax=ax[0])
    ax[0].text(reversed_idx * 2 + 0.5, -0.5, f'$G_{{𝜺_{7-step}}}$', horizontalalignment='center')

ax[0].set_xlim(-0.5, len(filtration_steps) * 2 - 0.2)
ax[0].set_ylim(-1, 1.5)
ax[0].axis('off')
ax[0].set_title('Graph on Increasing Thresholds')



components_over_time = {
    0: 1,
    1: 1,  # At step 1, there are 2 connected components
    2: 1,
    3: 2,
    4: 3,
    5: 4,
    6: 5,
    7: 5
}

steps = sorted(components_over_time.keys())
counts = [components_over_time[step] for step in steps]
# Plot the single line that represents the connected component's number at different times
ax[1].step(steps, counts, where='post', linewidth=2)

# Set the limits and labels for the barcode plot
ax[1].set_xlim(0, max_filtration_step + 0.5)
ax[1].set_ylim(0, max(counts) + 1)
ax[1].set_xlabel('Weight Threshold')
ax[1].set_ylabel('$𝜷_0$')

# Set the x-tick labels to reflect w_i notation
ax[1].set_xticks(range(1, max_filtration_step + 1))
ax[1].set_xticklabels([f'$𝜺_{{{i}}}$' for i in range(1, max_filtration_step + 1)])
ax[1].set_title('0D Barcode (Connected Components)')

# Show the plot
plt.tight_layout()
plt.show()
