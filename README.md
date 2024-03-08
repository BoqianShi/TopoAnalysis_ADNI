# Investigating Alzheimer's Disease Progression Through Topological Analysis of ADNI fMRI Data

## Project Overview

This project aims to utilize topological data analysis (TDA) to uncover patterns and anomalies in brain networks associated with Alzheimer's Disease (AD) progression, using functional Magnetic Resonance Imaging (fMRI) data from the Alzheimer's Disease Neuroimaging Initiative (ADNI) database. Our goal is to identify significant functional connections and network organizations correlating with Alzheimer's Disease, thereby enhancing our understanding of AD and paving the way for advancements in fMRI classification.

### Author

Boqian Shi

### Date

Spring 2024

----

## About

The project harnesses a dataset of fMRI and T1W images from the ADNI database, covering various stages of cognitive impairment. Our approach includes data preprocessing to convert DICOM data to NIFTI format, aligning fMRI with T1W data, and using fMRIPrep for comprehensive preprocessing. The methodology further involves extracting functional brain networks using the Human Connectome Project's Multi-Modal Parcellation (HCP-MMP) and Pearson’s correlation for identifying functional connections.

### Methodology

#### Data Preprocessing

The initial step involves organizing fMRI data according to the Brain Imaging Data Structure (BIDS) standard and comprehensive preprocessing to prepare the data for analysis.

#### Network Extraction

This phase focuses on accurately delineating functional areas within the brain using HCP-MMP and identifying meaningful functional connections through Pearson’s correlation.

#### Topological Analysis

The core of this project, the topological analysis, includes graph filtration to explore network connectivity, calculation of network dissimilarity scores using the 2-Wasserstein distance, and centroids clustering to identify common patterns among different stages of Alzheimer's Disease.


## Quick Start
-----------
1. Prerequisite: install _scikit-learn_
2. Execute `main.py` to run different functions



## Acknowledgments

This project utilizes data from the Alzheimer's Disease Neuroimaging Initiative (ADNI), and we acknowledge their invaluable contribution to Alzheimer's Disease research.

