# clustering.py
# Contains the clustering class that is used to perform topological clustering on the network data.
# Author: Boqian Shi

from sklearn.manifold import MDS
import matplotlib.pyplot as plt
import numpy as np
import config
import src.barcode
import sys
import math
import random
from src.subject import Subject, SubjectLoader
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import minimum_spanning_tree
from matplotlib import pyplot as plt

class k_centroids_clustering:

    def __init__(self, subject_loader, n_clusters, top_relative_weight, max_iter_alt,
                 max_iter_interp, learning_rate):
        self.subject_loader = subject_loader
        self.n_clusters = n_clusters
        self.top_relative_weight = top_relative_weight
        self.max_iter_alt = max_iter_alt
        self.max_iter_interp = max_iter_interp
        self.learning_rate = learning_rate

    def fit_predict(self):
        """
        Computes topological clustering and predicts cluster index for each sample.
        """    
        random.seed(config.random_seed)    
        # Since we are using HCI-MMP parcellation, the number of nodes is 360
        # MST only returns 359 edges, we have to minus one if we are not using geometric info
        if config.barcode_mode == "cycle":
            n_node = 359 
        elif config.barcode_mode == "attached":
            n_node = 360
        else:
            print("Barcode Mode", config.barcode_mode," not supported in fit_predict function")
        
        n_edges = math.factorial(n_node) // math.factorial(2) // math.factorial(
            n_node - 2)  # n_edges = (n_node choose 2)
        n_births = n_node - 1
        if config.geo_mode == "geo_included":
            self.weight_array = np.append(
                np.repeat(1 - self.top_relative_weight, n_edges),
                np.repeat(self.top_relative_weight, n_edges))
        #elif(config.geo_mode == "topo"):
        #    self.weight_array = np.repeat(1 - self.top_relative_weight, n_edges)
        else:
            print("Geo Mode", config.geo_mode," not supported in fit_predict function")

        X = self.barcode_to_array()
        
        # Random initial condition
        self.centroids = X[random.sample(range(X.shape[0]), self.n_clusters)]
        #print(X.shape)
        #print(self.centroids.shape)
        # Assign the nearest centroid index to each data point
        assigned_centroids = self._get_nearest_centroid(X[:, None, :], self.centroids[None, :, :])
        prev_assigned_centroids = assigned_centroids

        for it in range(self.max_iter_alt):
            for cluster in range(self.n_clusters):
                # Previous iteration centroid
                prev_centroid = np.zeros((n_node, n_node))
                prev_centroid[np.triu_indices(
                    prev_centroid.shape[0],
                    k=1)] = self.centroids[cluster][:n_edges]
                
                # Determine data points belonging to each cluster
                cluster_members = X[assigned_centroids == cluster]

                # Compute the sample mean and top. centroid of the cluster
                cluster_mean = cluster_members.mean(axis=0)
                sample_mean = np.zeros((n_node, n_node))
                sample_mean[np.triu_indices(sample_mean.shape[0],
                                            k=1)] = cluster_mean[:n_edges]
                top_centroid = cluster_mean[n_edges:]
                
                top_centroid_birth_set = top_centroid[:n_births]
                top_centroid_death_set = top_centroid[n_births:]

                # Update the centroid
                # try:
                cluster_centroid = self._top_interpolation(
                        prev_centroid, sample_mean, top_centroid_birth_set,
                        top_centroid_death_set)
                self.centroids[cluster] = src.barcode.get_barcode(cluster_centroid)
                #except:
                #    print(
                #        'Error: Possibly due to the learning rate is not within appropriate range.'
                #    )
                #    sys.exit(1)

            # Update the cluster membership
            assigned_centroids = self._get_nearest_centroid(
                X[:, None, :], self.centroids[None, :, :])

            # Compute and print loss as it is progressively decreasing
            loss = self._compute_top_dist(
                X, self.centroids[assigned_centroids]).sum() / len(X)
            # print('Iteration: %d -> Loss: %f' % (it, loss))

            if (prev_assigned_centroids == assigned_centroids).all():
                break
            else:
                prev_assigned_centroids = assigned_centroids
        return assigned_centroids

    def barcode_to_array(self):
        """
        Convert barcode to array X.
        """
        
        X = []
        for subject in self.subject_loader.subjects:
            X.append(subject.barcode)
        X = np.asarray(X)
        return X


    def _get_nearest_centroid(self, X, centroids):
        """Determines cluster membership of data points."""
        dist = self._compute_top_dist(X, centroids)
        nearest_centroid_index = np.argmin(dist, axis=1)
        return nearest_centroid_index

    def _compute_top_dist(self, X, centroid):
        """Computes the pairwise top. distances between networks and centroids."""
        return np.dot((X - centroid)**2, self.weight_array)

    def _top_interpolation(self, init_centroid, sample_mean,
                           top_centroid_birth_set, top_centroid_death_set):
        """Topological interpolation."""
        curr = init_centroid
        for _ in range(self.max_iter_interp):
            # Geometric term gradient
            geo_gradient = 2 * (curr - sample_mean)

            # Topological term gradient
            sorted_birth_ind, sorted_death_ind = self._compute_optimal_matching(
                curr)
            top_gradient = np.zeros_like(curr)
            
            top_gradient[sorted_birth_ind] = top_centroid_birth_set
            top_gradient[sorted_death_ind] = top_centroid_death_set
            top_gradient = 2 * (curr - top_gradient)

            # Gradient update
            curr -= self.learning_rate * (
                (1 - self.top_relative_weight) * geo_gradient +
                self.top_relative_weight * top_gradient)
        return curr

    def _compute_optimal_matching(self, adj):
        mst, nonmst = src.barcode.bd_decomposition(adj)
        birth_ind = np.nonzero(mst)
        death_ind = np.nonzero(nonmst)
        sorted_temp_ind = np.argsort(mst[birth_ind])
        sorted_birth_ind = tuple(np.array(birth_ind)[:, sorted_temp_ind])
        sorted_temp_ind = np.argsort(nonmst[death_ind])
        sorted_death_ind = tuple(np.array(death_ind)[:, sorted_temp_ind])
        return sorted_birth_ind, sorted_death_ind

    