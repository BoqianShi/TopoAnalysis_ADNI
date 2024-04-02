# src/svm.py
import numpy as np
from sklearn.model_selection import KFold
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.metrics import confusion_matrix
import config
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import adjusted_rand_score
import numpy as np
import matplotlib.pyplot as plt

def run_svm_classification(subjects, l1 = 1, l2 = 1, c_value = 1, cv_folds=5, random_state = 0):
    """
    Performs SVM classification on subjects' barcode data with optional feature scaling using lambdas,
    and calculates accuracy score and confusion matrix.

    Parameters:
    - subjects: List of Subject objects with barcode data and labels.
    - lambdas: Optional array-like of lambdas to be applied to each feature. Must be the same length as the number of features.
    - cv_folds: Number of folds for cross-validation.

    Returns:
    - A dictionary containing the accuracy score, confusion matrix, and CV scores for each fold.
    """
    # Extract barcode vector data and their corresponding labels
    X = np.array([subject.barcode for subject in subjects])
    y = np.array([subject.group for subject in subjects])

    # Initialize the cross-validator
    kf = KFold(n_splits=cv_folds, shuffle=True, random_state=random_state)

    accuracies = []
    cv_scores = []

    for train_index, test_index in kf.split(X):
        # Splitting the data for this fold
        X_train, X_test = X[train_index], X[test_index]
        y_train, y_test = y[train_index], y[test_index]

        if l1 != 1 or l2 != 1:
            for i in range(len(X_train)):
                x_t = X_train[i]
                y_t = y_train[i]
                temp = lambda_adjustment(x_t, y_t, l1, l2)
                X_train[i] = temp
        # Standardize features
        scaler = StandardScaler().fit(X_train)
        X_train_transformed = scaler.transform(X_train)
        X_test_transformed = scaler.transform(X_test)

        # SVM Classifier
        clf = SVC(C=c_value).fit(X_train_transformed, y_train)

        # Evaluate the model
        accuracy = clf.score(X_test_transformed, y_test)
        accuracies.append(accuracy)

        # Predictions for confusion matrix
        y_pred = clf.predict(X_test_transformed)
        # Evaluate the model
        score = clf.score(X_test_transformed, y_test)
        cv_scores.append(score)

    average_score = np.mean(cv_scores)

    return {
        'model': clf,
        'X_scaled': X,  # 'X_scaled' is used for plotting the decision boundary in 'plot_svm_decision_boundary
        'average_score': average_score,
        'cv_scores': cv_scores
    }

def lambda_adjustment(x_t, y_t, l1, l2):

    if y_t == 1:
        x_t = x_t * l1
    elif y_t == 0:
        x_t = x_t * l2
    else:
        print("Error: Label mode not recognized. Please check the configuration file.")
    return x_t


def tsne_svm(data, labels, l):
    scaler = StandardScaler()
    data_scaled = scaler.fit_transform(data)
    if config.separation_mode == "strict_binary":
        kernel = 'linear'
    else:
        kernel = 'rbf'
    # Train the SVM classifier
    svc = SVC(kernel=kernel, C=1, gamma='auto')
    svc.fit(data_scaled, labels)

    # Create a mesh to plot the decision boundary
    x_min, x_max = data_scaled[:, 0].min() - 1, data_scaled[:, 0].max() + 1
    y_min, y_max = data_scaled[:, 1].min() - 1, data_scaled[:, 1].max() + 1
    xx, yy = np.meshgrid(np.arange(x_min, x_max, 0.02),
                        np.arange(y_min, y_max, 0.02))

    # Predict on the mesh and reshape for plotting
    Z = svc.predict(np.c_[xx.ravel(), yy.ravel()])
    Z = Z.reshape(xx.shape)
    
    # Predict the labels using the trained model
    predicted_labels = svc.predict(data_scaled)
    # Calculate and print the ARI score
    ari_score = adjusted_rand_score(labels, predicted_labels)
    print(f"Adjusted Rand Index score: {ari_score:.4f} with lambda = {l:.4f}")
    return ari_score, xx, yy, Z, data_scaled, labels