# main.py
# The main function that handles all the scripts and functions
# Author: Boqian Shi

import logging
import math
import config
import src.clustering
from src.subject import Subject, SubjectLoader
from src.barcode import get_barcode, plot_cycle_barcode, plot_component_barcode
import numpy as np
from sklearn.metrics.cluster import contingency_matrix
from sklearn.metrics import adjusted_rand_score
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from datetime import datetime

# Write subject information into new CSV file
# Do not use this function unless you want to overwrite the current CSV file
def write_current():
    # Find unmatched items
    subject_manager = SubjectLoader()
    subject_manager.load_subject_data()
    subject_manager.save_subjects_to_csv("./matrix_subjects.csv")

# Subfunction to print subject information
def print_subject_info(subject_manager):
    # Get subjects belonging to a specific group
    for group in config.groups:
        group_subjects = subject_manager.get_subjects_by_group(group)
        print(f"\nSubjects in group {group}: ({len(group_subjects)} subjects)")
        for subject in group_subjects:
            print(subject)


# Load subject information from CSV file
def load_content():
    # Load subject information from CSV file
    subject_manager = SubjectLoader()

    # Load subject data from directory
    subject_manager.load_subject_data()

    if config.separation_mode == "strict_binary":
        subject_manager.strict_binary_label()
        if len(subject_manager.subjects) == config.num_strict_binary:
            print("All" , len(subject_manager.subjects), "subjects loaded successfully.")
        else:
            print("Error loading subjects, expected ", config.num_subjects, " but got ", len(subject_manager.subjects))
    
        if config.debug == 1:
            print_subject_info(subject_manager)
            

    if config.debug == 1:
        print_subject_info(subject_manager)
        if len(subject_manager.subjects) == config.num_subjects:
            print("All" , len(subject_manager.subjects), "subjects loaded successfully.")
        else:
            print("Error loading subjects, expected ", config.num_subjects, " but got ", len(subject_manager.subjects))
    
    
    if config.label_mode == "binary":
        subject_manager.binary_label()
    else:
        subject_manager.original_label()


    return subject_manager

# Generate barcode representation of the network
def generate_barcode(subject_manager):
    for subject in subject_manager.subjects:
        # Set the barcode mode to config values
        barcode = get_barcode(subject.data, barcode_mode=config.barcode_mode, adj_mode=config.adj_mode)
        # plot_barcode(barcode)
        subject.set_barcode(barcode)
        # print(subject)
        
# Plot the barcode of a single subject
def plot_single_barcode(subject):
    barcode_data = subject.barcode
    if config.barcode_mode == "component":
        plot_component_barcode(barcode_data, "Component Barcode: " + subject.subject_id)
    elif config.barcode_mode == "cycle":
        plot_cycle_barcode(barcode_data, "Cycle Barcode: " + subject.subject_id)
    else:
        plot_component_barcode(barcode_data, "Component Barcode: " + subject.subject_id)
        plot_cycle_barcode(barcode_data, "Cycle Barcode: " + subject.subject_id)

# Calculate the purity score
def purity_score(labels_true, labels_pred):
    mtx = contingency_matrix(labels_true, labels_pred)
    return np.sum(np.amax(mtx, axis=0)) / np.sum(mtx)

# Get the number of clusters based on the label mode
def get_cluster_number():
    
    if config.label_mode == "binary":
        return 2
    else:
        if config.separation_mode == "strict_binary":
            return 2
        else:
            return 4

# Grid search for the best parameters
# Only deal with learning_rate and topo_relative_weight
def grid_search(subject_manager):
    # Default variables
    max_iter_alt = 300
    max_iter_interp = 300

    n_clusters = get_cluster_number()
    # Setup logging
    logging.basicConfig(filename='training_logs.txt', level=logging.INFO, 
                        format='%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

    # Define the range of values for learning_rate and top_relative_weight
    learning_rate_range = [0.01, 0.02, 0.03, 0.05, 0.07, 0.1, 0.12, 0.15, 0.2, 0.3]  # From 0.01 to 0.2
    topo_relative_weight_range = [0.01, 0.05, 0.1, 0.15, 0.25, 0.35, 0.4, 0.5, 0.65, 0.75, 0.85, 0.95, 0.97, 0.99]  # From 0.1 to 0.99

    labels_true = subject_manager.get_labels()
    best_ari = -1  # Start with the worst possible score
    best_params = None
    results = np.zeros((len(learning_rate_range), len(topo_relative_weight_range)))  # To store ARI scores

    for i, lr in enumerate(learning_rate_range):
        for j, trw in enumerate(topo_relative_weight_range):
            labels_pred = np.random.randint(0, 2, len(labels_true))  # Example random predictions
            clustering_model = src.clustering.clustering(subject_manager, n_clusters, trw, max_iter_alt, max_iter_interp, lr)
            labels_pred = clustering_model.fit_predict()
            ari_score = adjusted_rand_score(labels_true, labels_pred)
            results[i, j] = ari_score
            
            if ari_score > best_ari:
                best_ari = ari_score
                best_params = (lr, trw)
            print(f"Learning Rate: {lr}, Topo Relative Weight: {trw}, ARI: {ari_score}")

    # Log the best configuration
    logging.info(f"Best ARI: {best_ari} with Learning Rate: {best_params[0]} and Topo Relative Weight: {best_params[1]}")
    logging.info(f"Separation_mode: {config.separation_mode}, Adjacency Matrix Mode: {config.adj_mode}, Labeling Mode: {config.label_mode}")
    print(f"Best ARI: {best_ari} with Learning Rate: {best_params[0]} and Topo Relative Weight: {best_params[1]}")
    # Visualization
    plt.figure(figsize=(10, 8))
    sns.heatmap(results, xticklabels=np.round(topo_relative_weight_range, 3), yticklabels=np.round(learning_rate_range, 3), annot=True, fmt=".3f", cmap="viridis")
    plt.title('Grid Search Results (ARI Score)')
    plt.xlabel('Top Relative Weight')
    plt.ylabel('Learning Rate')

    # Get current date and time for the filename
    current_time = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    filename = f'Grid_Search_Results_ARI_Score_{current_time}_{config.label_mode}_{config.separation_mode}.png'

    # Save the figure
    plt.savefig(filename, dpi=300, bbox_inches='tight')

    plt.show()

    return best_params, best_ari

def random_seed_search(subject_manager, n_clusters, topo_relative_weight, max_iter_alt,
                                                    max_iter_interp, learning_rate):
    # Assuming config.random_seed is a list of seeds
    best_ari_score = -1  # Start with the worst possible score
    best_labels_pred = None
    best_labels_true = None
    best_seed = None
    labels_true = subject_manager.get_labels()

    for seed in range(1000):
        config.random_seed = seed
        # Create the clustering model with the current seed
        clustering_model = src.clustering.clustering(subject_manager, n_clusters, topo_relative_weight, max_iter_alt,
                                                    max_iter_interp, learning_rate)
        
        # Fit and predict
        labels_pred = clustering_model.fit_predict()
        
        # Calculate ARI score
        ari_score = adjusted_rand_score(labels_true, labels_pred)
        print(f'Random Seed: {seed}, Adjusted Rand Index: {ari_score}')
        
        # Update best ARI score, labels, and seed if current ARI is better
        if ari_score > best_ari_score:
            best_ari_score = ari_score
            best_labels_pred = labels_pred
            best_labels_true = labels_true
            best_seed = seed

    # After iterating through all seeds, print the best ARI and its corresponding labels and seed
    print('Best Adjusted Rand Index:', best_ari_score)
    print('Best Seed:', best_seed)
    print('Best Labels Predicted:', best_labels_pred)
    print('Labels True:', best_labels_true)
    logging.info(f"Best ARI: {best_ari_score} with Random Seed: {best_seed}")

def iter_search(subject_manager):
    max_iter_list = [100, 200, 300 ,500, 700, 1000, 1500]
    for max_iter in max_iter_list:
        clustering_model = src.clustering.clustering(subject_manager, n_clusters, topo_relative_weight, max_iter, max_iter, learning_rate)
        labels_pred = clustering_model.fit_predict()
        labels_true = subject_manager.get_labels()
        ari_score = adjusted_rand_score(labels_true, labels_pred)
        print(f'Max Iteration Num: {max_iter}, Adjusted Rand Index: {ari_score}')

if __name__ == '__main__':
    print(
        "Project: Topological Clustering of Brain Networks\n"
    )
    print("Separation_mode: ", config.separation_mode)
    print(f"Barcode Processing Mode: {'Component-based' if config.barcode_mode == 'component' else 'Cycle-based' if config.barcode_mode == 'cycle' else 'Attached (Component + Cycle)'}")
    print(f"Geometric Information Mode: {'Included' if config.geo_mode == 'geo_included' else 'Excluded (Topological Information Only)'}")
    print(f"Adjacency Matrix Mode: {'Original' if config.adj_mode == 'original' else 'Ignore Negative Edges' if config.adj_mode == 'ignore_negative' else 'Absolute Values'}")
    print(f"Labeling Mode: {'Original Labels' if config.label_mode == 'original' else 'Binary Labels'}")

    # Load subject information from CSV file
    subject_manager = load_content()

    # Generate barcode representation of the network
    generate_barcode(subject_manager=subject_manager)    


    # Topological clustering variables
    n_clusters = get_cluster_number()

    max_iter_alt = 300
    max_iter_interp = 300
    learning_rate = 0.05
    topo_relative_weight = 0.25  # 'topo_relative_weight' between 0 and 1

    # Single test flag for single parameter testing
    single_test = 1
    if single_test == 1:
    
        clustering_model = src.clustering.clustering(subject_manager, n_clusters, topo_relative_weight, max_iter_alt,
                                    max_iter_interp,
                                    learning_rate)
        labels_pred = clustering_model.fit_predict()
        labels_true = subject_manager.get_labels()

        # Use Adjusted Rand Index score to evaluate the result
        ari_score = adjusted_rand_score(labels_true, labels_pred)
        print('Adjusted Rand Index:', ari_score)
        print(labels_pred)
        print(labels_true)
    else:
        # grid_search(subject_manager)
        # random_seed_search(subject_manager, n_clusters, topo_relative_weight, max_iter_alt,max_iter_interp,learning_rate)
        # iter_search(subject_manager)
        pass