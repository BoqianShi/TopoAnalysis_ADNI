# Topological Analysis on ADNI fMRI Data for Investigating Alzheimer's Disease Progression

## Project Overview

This project aims to utilize topological data analysis (TDA) to uncover patterns and anomalies in brain networks associated with Alzheimer's Disease (AD) progression, using functional Magnetic Resonance Imaging (fMRI) data from the Alzheimer's Disease Neuroimaging Initiative (ADNI) database. Our goal is to identify significant functional connections and network organizations correlating with Alzheimer's Disease, thereby enhancing our understanding of AD and paving the way for advancements in fMRI classification.

### Author

Boqian Shi

### Date

Spring 2024

---

## About

The project harnesses a dataset of fMRI and T1W images from the ADNI database, covering various stages of cognitive impairment. Our approach includes data preprocessing to convert DICOM data to NIFTI format, aligning fMRI with T1W data, and using fMRIPrep for comprehensive preprocessing. The methodology further involves extracting functional brain networks using the Human Connectome Project's Multi-Modal Parcellation (HCP-MMP) and Pearson’s correlation for identifying functional connections.

### Methodology

#### Data Preprocessing

The initial step involves organizing fMRI data according to the Brain Imaging Data Structure (BIDS) standard and comprehensive preprocessing to prepare the data for analysis.

**This part's code can be find in References/notebooks/pre_procerssing.ipynb**

#### Network Extraction

This phase focuses on accurately delineating functional areas within the brain using HCP-MMP and identifying meaningful functional connections through Pearson’s correlation.

**This part's code can be find in References/notebooks/fmri_prep.ipynb**

#### Topological Analysis

The core of this project, the topological analysis, includes graph filtration to explore network connectivity, calculation of network dissimilarity scores using the 2-Wasserstein distance, and centroids clustering to identify common patterns among different stages of Alzheimer's Disease.

---

## Configuration with `config.py`

`config.py` serves as the central configuration file for customizing the analysis process. It allows users to specify various parameters that control how data is processed and analyzed. Here's how you can use `config.py`:

- **Group Names**: Define the groups of subjects (`AD`, `CN`, `LMCI`, `EMCI`, `MCI`) to include in the analysis.

- **Number of Subjects**: Set the total number of subjects to analyze.

- **Barcode Mode**: Choose the barcode computation mode (`component`, `cycle`, `attached`) to tailor the topological features extracted.
    - **component**: Only use 0th Betti (which are the components) to perform the similarity matching.
    - **cycle**: Only use 1th Betti (which are the cycles) to perform the similarity matching.
    - **attached**: Simply attach the components and cycles together by:
        > attached = component + cycle

- **Adjacency Matrix Mode**: Select how to handle the adjacency matrix (`original`, `ignore_negative`, `absolute`) for network construction.
    - **original**: Use original adjacency matrix.
    - **ignore_negative**: Simply remove all the negative values.
    - **absolute**: Use absolute values for all the values to get a new matrix.

- **Geometry Mode**: Decide whether to include geometric information (`geo_included`) or focus solely on topological aspects (`topo`).
    - **geo_included**: Use geometry information.
    - **topo**: Only use topological information (components and cycles).

- **Label Mode**: Specify label configuration (`original`, `binary`) for your dataset.
    - **original**: Use 5 groups to recognize.
    - **binary**: If *AD* or *ECMI*, label = 1, else label = 0.

- **Data Directory**: Indicate the directory where subject data files are located.

- **Subject CSV File**: Provide the path to the CSV file containing subject information.

- **Debug Flag**: Enable (`1`) or disable (`0`) debug mode for additional logging and diagnostics.

To modify the analysis, edit the `config.py` file's variables according to your needs and preferences. This flexibility allows for a customized analysis approach tailored to the specificities of your dataset and research objectives.

## Quick Start

1. Prerequisite: Install _scikit-learn_.
2. Configure analysis parameters in `config.py` as described above.
3. Execute `main.py` to run the analysis with your specified configurations.

## Acknowledgments

This project utilizes data from the Alzheimer's Disease Neuroimaging Initiative (ADNI), and we acknowledge their invaluable contribution to Alzheimer's Disease research. Special thanks to Mr. Alireza Fathian and Prof. Yousef Jamali for providing referencing data; their paper "The trend of disruption in the functional brain network topology of Alzheimer’s disease" ([Nature](https://www.nature.com/articles/s41598-022-18987-y)) has greatly inspired the pre-processing steps undertaken in this project. 

Additionally, we are grateful for the guidance and resources provided by my advisor, Prof. Songdechakraiwut, particularly the code for topological clustering available at [topo-clustering](https://github.com/topolearn/topo-clustering). Their contributions have been instrumental in shaping the methodologies and analyses employed in our investigation.
