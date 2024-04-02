import numpy as np
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
from src.subject import SubjectLoader, Subject
from main import load_content
import config
from src.barcode import get_barcode
from src.svm import tsne_svm
# Function to extract barcode data and labels
def extract_data(subject_loader, l = 0.5):
    data = []
    labels = []
    
    for subject in subject_loader.subjects:
        # subject.assign_label()
        # Set the barcode mode to config values
        if subject.label == "AD" or subject.label == "CN":
            barcode = get_barcode(subject.data, barcode_mode=config.barcode_mode, adj_mode=config.adj_mode, l = l)
            # plot_barcode(barcode)
            subject.set_barcode(barcode)
            data.append(subject.barcode)
            labels.append(subject.label)
    return np.array(data), labels

def visualize_data_grid(subject_manager, l_list):
    # Determine the size of the grid
    n_rows = len(l_list) // 3 + (1 if len(l_list) % 3 > 0 else 0)
    
    # Create a figure and a set of subplots
    fig, axs = plt.subplots(n_rows, 3, figsize=(15, n_rows * 5))
    axs = axs.flatten()  # Flatten the array of axes for easy indexing
    
    for i, l in enumerate(l_list):
        data, labels = extract_data(subject_manager, l)  # Assume this function is adapted to handle l
        
        # Perform t-SNE dimensionality reduction
        tsne = TSNE(n_components=2, random_state=42)
        transformed_data = tsne.fit_transform(data)
        
        # Plotting in the ith subplot
        groups = set(labels)
        colors = ['red', 'blue', 'green', 'purple']
        group_color = {group: color for group, color in zip(groups, colors)}
        
        for group in groups:
            idx = [j for j, label in enumerate(labels) if label == group]
            axs[i].scatter(transformed_data[idx, 0], transformed_data[idx, 1], c=group_color[group], label=group, alpha=0.6)
        
        axs[i].set_title('L: ' + str(l))
        axs[i].set_xlabel('Component 1')
        axs[i].set_ylabel('Component 2')
        axs[i].legend()
    
    # Hide any unused subplots
    for ax in axs[len(l_list):]:
        ax.set_visible(False)
    
    plt.tight_layout()
    plt.show()

# Function to visualize the data
def visualize_data(data, labels, l):
    # Perform t-SNE dimensionality reduction
    tsne = TSNE(n_components=2, random_state=42)
    transformed_data = tsne.fit_transform(data)
    
    # Plotting
    plt.figure(figsize=(15, 8))
    groups = set(labels)
    colors = ['red', 'blue', 'green', 'purple']
    group_color = {group: color for group, color in zip(groups, colors)}
    for group in groups:
        idx = [i for i, label in enumerate(labels) if label == group]
        plt.scatter(transformed_data[idx, 0], transformed_data[idx, 1], c=group_color[group], label=group, alpha=0.6)
    plt.title('Topological Feature Visualization by Group' + ' L: ' + str(l))
    plt.legend()
    plt.show()
    
def plot(xx, yy, Z, data_scaled, labels, l):
    # print(Z)
    # Plot the decision boundary
    plt.contourf(xx, yy, Z, cmap=plt.cm.coolwarm, alpha=0.8)

    # Plot also the data points
    scatter = plt.scatter(data_scaled[:, 0], data_scaled[:, 1], c=labels, cmap=plt.cm.coolwarm, edgecolors='k')

    legend_labels = {0: 'AD', 1: 'CN'}
    handles, _ = scatter.legend_elements()
    plt.legend(handles, [legend_labels[label] for label in [0, 1]], title="Group")

    plt.title(f'SVM Decision Boundary and Data Points (AD vs CN); lambda = {l:.4f})')
    plt.show()


grid_search = 0
subject_manager = load_content()
if grid_search:
    l_list = np.arange(0.4, 0.6, 0.001)
    max_ari = 0
    for l in l_list:
        data, labels = extract_data(subject_manager, l)
        # Visualize the data
        # visualize_data(data, labels, l)
        tsne = TSNE(n_components=2, random_state=42)
        transformed_data = tsne.fit_transform(data)
        temp = []
        for label in labels:
            if label == "AD":
                temp.append(0)
            else:
                temp.append(1)
        
        ari_score, xx, yy, Z, data_scaled, _ = tsne_svm(transformed_data, temp, l)
        if ari_score > max_ari:
            max_ari = ari_score
            best_l = l
            best_xx = xx
            best_yy = yy
            best_Z = Z
            best_data_scaled = data_scaled

    plot(best_xx, best_yy, best_Z, best_data_scaled, temp, best_l)
else:
    # max l: 
    # 0.423, 0.462
    l = 0.462
    data, labels = extract_data(subject_manager, l)
    # Visualize the data
    tsne = TSNE(n_components=2, random_state=42)
    transformed_data = tsne.fit_transform(data)
    temp = []
    for label in labels:
        if label == "AD":
            temp.append(0)
        else:
            temp.append(1)
    ari_score, xx, yy, Z, data_scaled, _ = tsne_svm(transformed_data, temp, l)
    plot(xx, yy, Z, data_scaled, temp, l)