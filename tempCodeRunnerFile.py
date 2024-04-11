# First, let's import the required libraries
import numpy as np

# List of accuracy results from the k-fold cross validation
accuracies = [0.625, 0.75, 0.6086956521739131, 0.782608695652174, 0.7391304347826086]

# Calculating the mean and standard deviation of the accuracies
mean_accuracy = np.mean(accuracies)
std_deviation = np.std(accuracies)

print(mean_accuracy)
print(std_deviation)
