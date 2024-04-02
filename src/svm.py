# src/svm.py

from sklearn.model_selection import cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
import numpy as np
import config

def run_svm_classification(subjects, l1, l2, cv_folds=5):
    """
    Performs SVM classification on subjects' barcode data.

    Parameters:
    - subjects: List of Subject objects with barcode data and labels.
    - cv_folds: Number of folds for cross-validation.

    Returns:
    - A tuple containing the average CV score and an array of scores for each fold.
    """
    lambda_adjustment(subjects, l1, l2)
    # Extract barcode vector data and their corresponding labels
    X = [subject.barcode for subject in subjects]  # feature vectors
    y = [subject.group for subject in subjects]    # labels

    # Convert lists to numpy arrays for compatibility with scikit-learn
    X = np.array(X)
    y = np.array(y)

    # Data Preprocessing
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # SVM Classifier initialization
    svc = SVC(kernel='linear')

    # Cross-validation
    cv_scores = cross_val_score(svc, X_scaled, y, cv=cv_folds)

    # Calculate the average score
    average_score = np.mean(cv_scores)

    return average_score, cv_scores


def lambda_adjustment(subjects, l1, l2):

    if config.label_mode == "original":
        return subjects
    elif config.label_mode == "binary":
        for subject in subjects:
            if subject.group == 1:
                subject.barcode = subject.barcode * l1   
            elif subject.group == 0:
                subject.barcode = subject.barcode * l2
            else:
                print("Error: Label mismatched on subject: ", subject.subject_id, " Please check the label.")
    else:
        print("Error: Label mode not recognized. Please check the configuration file.")