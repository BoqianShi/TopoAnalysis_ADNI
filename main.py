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
        
def plot_single_barcode(subject):
    barcode_data = subject.barcode
    if config.barcode_mode == "component":
        plot_component_barcode(barcode_data, "Component Barcode: " + subject.subject_id)
    elif config.barcode_mode == "cycle":
        plot_cycle_barcode(barcode_data, "Cycle Barcode: " + subject.subject_id)
    else:
        plot_component_barcode(barcode_data, "Component Barcode: " + subject.subject_id)
        plot_cycle_barcode(barcode_data, "Cycle Barcode: " + subject.subject_id)

def purity_score(labels_true, labels_pred):
    mtx = contingency_matrix(labels_true, labels_pred)
    return np.sum(np.amax(mtx, axis=0)) / np.sum(mtx)


def grid_search(subject_manager):
    # Default variables
    max_iter_alt = 300
    max_iter_interp = 300
    if config.label_mode == "binary":
        n_clusters = 2
    else:
        n_clusters = 4

    # Setup logging
    logging.basicConfig(filename='training_logs.txt', level=logging.INFO, 
                        format='%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

    # Define the range of values for learning_rate and top_relative_weight
    learning_rate_range = np.linspace(0.01, 0.2, 10)  # From 0.01 to 0.2
    top_relative_weight_range = np.linspace(0.1, 0.99, 10)  # From 0.1 to 0.99

    labels_true = subject_manager.get_labels()
    best_ari = -1  # Start with the worst possible score
    best_params = None
    results = np.zeros((len(learning_rate_range), len(top_relative_weight_range)))  # To store ARI scores

    for i, lr in enumerate(learning_rate_range):
        for j, trw in enumerate(top_relative_weight_range):
            labels_pred = np.random.randint(0, 2, len(labels_true))  # Example random predictions
            clustering_model = src.clustering.clustering(subject_manager, n_clusters, trw, max_iter_alt, max_iter_interp, lr)
            labels_pred = clustering_model.fit_predict()
            ari_score = adjusted_rand_score(labels_true, labels_pred)
            results[i, j] = ari_score
            
            if ari_score > best_ari:
                best_ari = ari_score
                best_params = (lr, trw)
            print(f"Learning Rate: {lr}, Top Relative Weight: {trw}, ARI: {ari_score}")

    # Log the best configuration
    logging.info(f"Best ARI: {best_ari} with Learning Rate: {best_params[0]} and Top Relative Weight: {best_params[1]}")
    print(f"Best ARI: {best_ari} with Learning Rate: {best_params[0]} and Top Relative Weight: {best_params[1]}")
    
    # Visualization
    plt.figure(figsize=(10, 8))
    sns.heatmap(results, xticklabels=np.round(top_relative_weight_range, 2), yticklabels=np.round(learning_rate_range, 2), annot=True, fmt=".2f", cmap="viridis")
    plt.title('Grid Search Results (ARI Score)')
    plt.xlabel('Top Relative Weight')
    plt.ylabel('Learning Rate')
    plt.show()

    return best_params, best_ari


if __name__ == '__main__':
    print("Running on barcode mode: ", config.barcode_mode)
    print("Running on geo mode: ", config.geo_mode)
    # Load subject information from CSV file
    subject_manager = load_content()

    # Generate barcode representation of the network
    generate_barcode(subject_manager=subject_manager)    


    # Topological clustering variables
    if config.label_mode == "binary":
        n_clusters = 2
    else:
        n_clusters = 4

    top_relative_weight = 0.99  # 'top_relative_weight' between 0 and 1
    max_iter_alt = 300
    max_iter_interp = 300
    learning_rate = 0.05
    grid_search(subject_manager)

    # Single test flag for single parameter testing
    single_test = 0
    if single_test == 1:
        clustering_model = src.clustering.clustering(subject_manager, n_clusters, top_relative_weight, max_iter_alt,
                                    max_iter_interp,
                                    learning_rate)
        labels_pred = clustering_model.fit_predict()
        labels_true = subject_manager.get_labels()

        # Use Adjusted Rand Index
        ari_score = adjusted_rand_score(labels_true, labels_pred)
        print('Adjusted Rand Index:', ari_score)
