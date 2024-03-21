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

def grid_search():
    # Setup logging
    logging.basicConfig(filename='training_logs.txt', level=logging.INFO, 
                        format='%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

    # Define the range of values for learning_rate and top_relative_weight
    learning_rates = np.linspace(0.01, 0.1, 10)  # Example: from 0.01 to 0.1, 10 values
    top_relative_weights = np.linspace(0.9, 0.99, 10)  # Example: from 0.9 to 0.99, 10 values

    # Variables for tracking the best configuration
    best_purity = 0
    best_lr = 0
    best_trw = 0
    labels_true = subject_manager.get_labels()

    # Loop over all combinations of learning_rate and top_relative_weight
    for lr in learning_rates:
        for trw in top_relative_weights:
            # Setup and train the clustering model with the current parameters
            clustering_model = src.clustering.clustering(subject_manager, n_clusters, trw, max_iter_alt,
                                                        max_iter_interp, lr)
            labels_pred = clustering_model.fit_predict()

            # Calculate the purity score
            current_purity = purity_score(labels_true, labels_pred)
            logging.info(f'Learning Rate: {lr}, Top Relative Weight: {trw}, Purity Score: {current_purity}')

            # Update best parameters if current configuration is better
            if current_purity > best_purity:
                best_purity = current_purity
                best_lr = lr
                best_trw = trw

    # Log the best configuration
    logging.info(f'Best Configuration -> Learning Rate: {best_lr}, Top Relative Weight: {best_trw}, Highest Purity Score: {best_purity}')

    print(f'Best Configuration -> Learning Rate: {best_lr}, Top Relative Weight: {best_trw}, Highest Purity Score: {best_purity}')



if __name__ == '__main__':
    print("Running on barcode mode: ", config.barcode_mode)
    print("Running on geo mode: ", config.geo_mode)
    # Load subject information from CSV file
    subject_manager = load_content()




    # Generate barcode representation of the network
    generate_barcode(subject_manager=subject_manager)    


    # Topological clustering variables
    n_clusters = 10
    top_relative_weight = 0.98  # 'top_relative_weight' between 0 and 1
    max_iter_alt = 300
    max_iter_interp = 300
    learning_rate = 0.05
    grid_search()

    # single train below
    clustering_model = src.clustering.clustering(subject_manager, n_clusters, top_relative_weight, max_iter_alt,
                                max_iter_interp,
                                learning_rate)
    # labels_pred = clustering_model.fit_predict()   
    # labels_true = subject_manager.get_labels()
    # print('Purity score:', purity_score(labels_true, labels_pred))
    
    # Single test flag for single subject testing
    single_test = 0
    if single_test == 1:
        # Plot barcode for a specific subject
        subject_130_S_4984 = subject_manager.get_subject_by_id("130S4984")
        # print(subject_130_S_4984)
        #plot_single_barcode(subject_130_S_4984)
        data = np.asarray(subject_130_S_4984.data)
        n_node = data.shape[1]
        n_edges = math.factorial(n_node) // math.factorial(2) // math.factorial(
                n_node - 2)  # n_edges = (n_node choose 2)
        #n_births = n_node - 1
        print(n_node)
