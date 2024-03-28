# Topological Analysis Framework of ADNI fMRI Data for Investigating Alzheimer's Disease Progression

## Project Overview

**Author:** Boqian Shi  
**Institution:** Duke University  
**Program:** Master of Science in Computer Science  
**Date:** Spring 2024

This Master's project by Boqian Shi implements a framework that utilizing topological data analysis (TDA) to analyze functional Magnetic Resonance Imaging (fMRI) data from the Alzheimer's Disease Neuroimaging Initiative (ADNI). The goal is to uncover patterns in brain networks associated with Alzheimer's Disease progression, identifying key functional connections and network organizations.

---

## About the Project

### Data Source
- **Dataset:** fMRI and T1W images from the ADNI database.
    - Total 117 subjects, all in numpy now:
        1. AD - 27 subjects
        2. CN - 32 subjects
        3. LMCI - 23 subjects
        4. MCI - 8 subjects (Treated as LMCI for the balancing purpose)
        5. EMCI - 26 subjects
- **Stages:** Covers various stages of cognitive impairment.

### Methodology Overview

#### 1. Data Preprocessing
- **Objective:** Organize fMRI data according to BIDS and prepare it for analysis.
- **Tools:** fMRIPrep for comprehensive preprocessing.
- **Notebook:** `References/notebooks/pre_processing.ipynb`

#### 2. Network Extraction
- **Objective:** Delineate functional areas and identify functional connections.
- **Tools:** HCP-MMP for brain parcellation, Pearson’s correlation for connection identification.
- **Notebook:** `References/notebooks/fmri_prep.ipynb`

#### 3. Topological Analysis
- **Objective:** Explore network connectivity and identify patterns among Alzheimer's Disease stages.
- **Methods:** Graph filtration, 2-Wasserstein distance for network dissimilarity, centroids clustering.
- **Highlight:** This phase is the core of the project, leveraging TDA for insightful analysis.

---

## Configuration with `config.py`

`config.py` serves as the central configuration file for customizing the analysis process. It allows users to specify various parameters that control how data is processed and analyzed. Here's how you can use `config.py`:

- **Separation mode**: Define how the data will be separated into different groups (`mixed_separation`, `strict_binary`) 
    - **mixed_separation**: 2 groups: AD + MCI + LMCI **vs** CN + EMCI
    - **strict_binary**: 2 groups: AD **vs** CN (ignore the rest)

- **Group Names**: Define the groups of subjects (`AD`, `CN`, `LMCI`, `EMCI`, `MCI`) to include in the analysis.

- **Number of Subjects**: Set the total number of subjects to analyze.

- **Barcode Mode**: Choose the barcode computation mode (`component`, `cycle`, `attached`) to tailor the topological features extracted.
    - **component**: Only use 0th Betti (which are the components) to perform the similarity matching.  
        - **Currently not supported**
    - **cycle**: Only use 1th Betti (which are the cycles) to perform the similarity matching.
        - **Currently not supported**
    - **attached**: Simply attach the components and cycles together by:
        > attached = component + cycle

- **Adjacency Matrix Mode**: Select how to handle the adjacency matrix (`original`, `ignore_negative`, `absolute`) for network construction.
    - **original**: Use original adjacency matrix.
    - **ignore_negative**: Simply remove all the negative values.
    - **absolute**: Use absolute values for all the values to get a new matrix.

- **Geometry Mode**: Decide whether to include geometric information (`geo_included`) or focus solely on topological aspects (`topo`).
    - **geo_included**: Use geometry information.
    - **topo**: Only use topological information (components and cycles).
        - **Currently not supported**

- **Label Mode**: Specify label configuration (`original`, `binary`) for your dataset.
    - **original**: Use 5 groups to recognize.
    - **binary**: If *AD* or *ECMI*, label = 1, else label = 0.

- **Data Directory**: Indicate the directory where subject data files are located.

- **Subject CSV File**: Provide the path to the CSV file containing subject information.

- **Debug Flag**: Enable (`1`) or disable (`0`) debug mode for additional logging and diagnostics.

To modify the analysis, edit the `config.py` file's variables according to your needs and preferences. This flexibility allows for a customized analysis approach tailored to the specificities of your dataset and research objectives.

## Quick Start Guide

1. **Prerequisite:** Ensure _scikit-learn_ is installed.
2. **Configuration:** Adjust `config.py` as needed.
3. **Execution:** Run `main.py` to start the analysis with your configurations.

## Acknowledgments

This project utilizes data from the Alzheimer's Disease Neuroimaging Initiative (ADNI), and we acknowledge their invaluable contribution to Alzheimer's Disease research. 

Special thanks to Mr. Alireza Fathian and Prof. Yousef Jamali for providing referencing data; their paper "The trend of disruption in the functional brain network topology of Alzheimer’s disease" ([Nature](https://www.nature.com/articles/s41598-022-18987-y)) has greatly inspired the pre-processing steps undertaken in this project. 

Additionally, we are grateful for the guidance and resources provided by my advisor, Prof. Songdechakraiwut, particularly the code for topological clustering available at [topo-clustering](https://github.com/topolearn/topo-clustering). Their contributions have been instrumental in shaping the methodologies and analyses employed in our investigation.
