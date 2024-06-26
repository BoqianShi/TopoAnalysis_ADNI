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
from paper_visuals.similarities import compute_dissimilarity_between_groups, visualize_similarity, calculate_group_averages

from src.svm import run_svm_classification


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
    elif config.separation_mode == "cn_separation":
        subject_manager.cn_separation_label()
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
        if config.separation_mode == "strict_binary" or config.separation_mode == "cn_separation":
            return 2
        else:
            return 4

# Grid search for the best parameters
# Only deal with learning_rate and topo_relative_weight
def grid_search_centroids(subject_manager):
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
            clustering_model = src.clustering.k_centroids_clustering(subject_manager, n_clusters, trw, max_iter_alt, max_iter_interp, lr)
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
    
    sum_aris = 0
    aris_list = []
    for seed in range(100):
        config.random_seed = seed
        # Create the clustering model with the current seed
        clustering_model = src.clustering.k_centroids_clustering(subject_manager, n_clusters, topo_relative_weight, max_iter_alt,
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
        sum_aris += ari_score
        aris_list.append(ari_score)
    # After iterating through all seeds, print the best ARI and its corresponding labels and seed
    print('Best Adjusted Rand Index:', best_ari_score)
    print('Best Seed:', best_seed)
    print('Average ARI:', sum_aris / 100)
    print('variance:', np.var(aris_list))
    #print('Best Labels Predicted:', best_labels_pred)
    #print('Labels True:', best_labels_true)
    logging.info(f"Best ARI: {best_ari_score} with Random Seed: {best_seed}")

def iter_search(subject_manager):
    max_iter_list = [100, 200, 300 ,500, 700, 1000, 1500]
    for max_iter in max_iter_list:
        clustering_model = src.clustering.k_centroids_clustering(subject_manager, n_clusters, topo_relative_weight, max_iter, max_iter, learning_rate)
        labels_pred = clustering_model.fit_predict()
        labels_true = subject_manager.get_labels()
        ari_score = adjusted_rand_score(labels_true, labels_pred)
        print(f'Max Iteration Num: {max_iter}, Adjusted Rand Index: {ari_score}')

def k_centroids_test(subject_manager):
    # Topological clustering variables
    generate_barcode(subject_manager=subject_manager)    
    n_clusters = get_cluster_number()

    max_iter_alt = 300
    max_iter_interp = 300
    learning_rate = 0.05
    topo_relative_weight = 0.25  # 'topo_relative_weight' between 0 and 1

    # Single test flag for single parameter testing
    single_test = 0
    if single_test == 1:
    
        clustering_model = src.clustering.k_centroids_clustering(subject_manager, n_clusters, topo_relative_weight, max_iter_alt,
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
        random_seed_search(subject_manager, n_clusters, topo_relative_weight, max_iter_alt,max_iter_interp,learning_rate)
        # iter_search(subject_manager)
        # clustering_model = src.clustering.k_centroids_clustering(subject_manager, n_clusters, topo_relative_weight, max_iter_alt, max_iter_interp, learning_rate)

def similarity_score():
    subject_manager = SubjectLoader()
    subject_manager.load_subject_data()
    subject_manager.mci_correct()
    group_averages = calculate_group_averages(subject_manager.subjects, config.adj_mode)
    #print_subject_info(subject_manager)
    dissimilarity_matrix, groups = compute_dissimilarity_between_groups(group_averages)
    cn_average_dissimilarity = np.mean(dissimilarity_matrix[0])
    print(f"Average Dissimilarity of CN group: {cn_average_dissimilarity}")
    emci_average_dissimilarity = np.mean(dissimilarity_matrix[1])
    print(f"Average Dissimilarity of EMCI group: {emci_average_dissimilarity}")
    lmci_average_dissimilarity = np.mean(dissimilarity_matrix[2])
    print(f"Average Dissimilarity of LMCI group: {lmci_average_dissimilarity}")
    ad_average_dissimilarity = np.mean(dissimilarity_matrix[3])
    print(f"Average Dissimilarity of AD group: {ad_average_dissimilarity}")
    print(dissimilarity_matrix)

def svm_classification_grid_l1(subject_loader, l1, l2):
    for subject in subject_loader.subjects:
        # Set the barcode mode to config values
        barcode = get_barcode(subject.data, barcode_mode=config.barcode_mode, adj_mode=config.adj_mode, l = 0.99)
        # plot_barcode(barcode)
        subject.set_barcode(barcode)
    # Call the SVM classification function# Define your grid of values to search over
    l1_values = np.arange(0.8, 1.2, 0.01)
    # Perform grid search
    best_accuracy = 0
    best_l1_value = None

    for l1_value in l1_values:
        results = run_svm_classification(subject_loader.subjects, l1_value, l2, c_value = 1, cv_folds=5)
        if results['average_score'] > best_accuracy:
            best_accuracy = results['average_score']
            best_l1_value = l1_value
        print(f"Accuracy: {results['average_score']} with l1={l1_value}")

    print(f"Best Average Accuracy: {best_accuracy} with l1={best_l1_value}")

def svm_classification_grid_c(subject_loader, l1, l2):
    for subject in subject_loader.subjects:
        # Set the barcode mode to config values
        barcode = get_barcode(subject.data, barcode_mode=config.barcode_mode, adj_mode=config.adj_mode, l = 0.99)
        # plot_barcode(barcode)
        subject.set_barcode(barcode)
    # Call the SVM classification function# Define your grid of values to search over
    c_values = [0.01, 0.1, 1, 10, 100, 1000]
    # Perform grid search
    best_accuracy = 0
    best_c_value = None

    for c_value in c_values:
        results = run_svm_classification(subject_loader.subjects, l1, l2, c_value = c_value, cv_folds=5)
        if results['average_score'] > best_accuracy:
            best_accuracy = results['average_score']
            best_c_value = c_value
        print(f"Accuracy: {results['average_score']} with c={c_value}")

    print(f"Best Average Accuracy: {best_accuracy} with c={best_c_value}")

def svm_classification_grid_random(subject_loader, l1, l2):
    for subject in subject_loader.subjects:
        # Set the barcode mode to config values
        barcode = get_barcode(subject.data, barcode_mode=config.barcode_mode, adj_mode=config.adj_mode, l = 0.99)
        # plot_barcode(barcode)
        subject.set_barcode(barcode)
    # Call the SVM classification function# Define your grid of values to search over
    random_seeds = range(100)
    # Perform grid search
    best_accuracy = 0
    best_seed = None

    for seed in random_seeds:
        results = run_svm_classification(subject_loader.subjects, l1, l2, c_value = 1, cv_folds=5, random_state=seed)
        if results['average_score'] > best_accuracy:
            best_accuracy = results['average_score']
            best_seed = seed
        print(f"Accuracy: {results['average_score']} with seed={seed}")

    print(f"Best Average Accuracy: {best_accuracy} with seed={best_seed}")


def svm_classification_grid_lambda(subject_loader, l1, l2):
    # Perform grid search
    temp = subject_loader.subjects.copy()
    lambda_values = np.arange(0, 0.99, 0.1)
    best_accuracy = 0
    best_l_value = None
    for l in lambda_values:
        for subject in temp:
            # Set the barcode mode to config values
            barcode = get_barcode(subject.data, barcode_mode=config.barcode_mode, adj_mode=config.adj_mode, l = l)
            # plot_barcode(barcode)
            subject.set_barcode(barcode)
        # Call the SVM classification function# Define your grid of values to search over
        results = run_svm_classification(temp, l1, l2, c_value = 1, cv_folds=5)
        if results['average_score'] > best_accuracy:
            best_accuracy = results['average_score']
            best_l_value = l
        print(f"Accuracy: {results['average_score']} with lambda={l}")

    print(f"Best Average Accuracy: {best_accuracy} with l1={best_l_value}")



def svm_classification(subject_loader, l1, l2):
    
    for subject in subject_loader.subjects:
        # Set the barcode mode to config values
        barcode = get_barcode(subject.data, barcode_mode=config.barcode_mode, adj_mode=config.adj_mode, l = 0.5)
        # plot_barcode(barcode)
        subject.set_barcode(barcode)
    results = run_svm_classification(subject_loader.subjects, l1, l2, c_value = 1, cv_folds=5, random_state = 0)

    print(f"Average Cross-Validation Score: {results['average_score']}")
    print(f"Cross-Validation Scores for Each Fold: {results['cv_scores']}") 
    
if __name__ == '__main__':
    print(
        "\nProject: Topological Clustering of Brain Networks\n"
    )
    print("Separation_mode: ", config.separation_mode)
    print(f"Barcode Processing Mode: {'Component-based' if config.barcode_mode == 'component' else 'Cycle-based' if config.barcode_mode == 'cycle' else 'Attached (Component + Cycle)'}")
    print(f"Geometric Information Mode: {'Included' if config.geo_mode == 'geo_included' else 'Excluded (Topological Information Only)'}")
    print(f"Adjacency Matrix Mode: {'Original' if config.adj_mode == 'original' else 'Ignore Negative Edges' if config.adj_mode == 'ignore_negative' else 'Absolute Values'}")
    print(f"Labeling Mode: {'Original Labels' if config.label_mode == 'original' else 'Binary Labels'}")

    # The following code calculates the similarity between the group averages
    # similarity_score()

    # The following code tests the k-centroids clustering algorithm
    subject_manager = load_content()
    k_centroids_test(subject_manager)  




    # The following code tests the svm classification algorithm

    l1 = 1
    l2 = 1
    # svm_classification(subject_manager, l1, l2)

    