# Topological Analysis on ADNI fMRI Data for Investigating Alzheimer's Disease Progression

## Project Overview

**Author:** Boqian Shi  
**Institution:** Duke University  
**Program:** Master of Science in Computer Science  
**Date:** Spring 2024

This Master's project by Boqian Shi utilizes topological data analysis (TDA) to analyze functional Magnetic Resonance Imaging (fMRI) data from the Alzheimer's Disease Neuroimaging Initiative (ADNI). The goal is to uncover patterns in brain networks associated with Alzheimer's Disease progression, identifying key functional connections and network organizations.

---

## About the Project

### Data Source
- **Dataset:** fMRI and T1W images from the ADNI database.
    - Total 117 subjects, all in numpy now:
        1. AD - 27 subjects
        2. CN - 32 subjects
        3. LMCI - 23 subjects
        4. MCI - 8 subjects
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

`config.py` is the central configuration file for this project, enabling customization of the analysis process. Here’s a breakdown of key parameters you can adjust:

- **Group Names:** Define subject groups (`AD`, `CN`, `LMCI`, `EMCI`, `MCI`).
- **Number of Subjects:** Specify total subjects to analyze.
- **Barcode Mode:** Choose computation mode (`component`, `cycle`, `attached`) for topological features.
- **Adjacency Matrix Mode:** Handle adjacency matrix (`original`, `ignore_negative`, `absolute`).
- **Geometry Mode:** Include geometric info (`geo_included`) or focus on topology (`topo`).
- **Label Mode:** Set label configuration (`original`, `binary`).
- **Data Directory & Subject CSV File:** Specify locations for data files and subject information.
- **Debug Flag:** Enable/disable debug mode for additional logging.

For detailed instructions on configuring these parameters, refer to the comments within `config.py`.

## Quick Start Guide

1. **Prerequisite:** Ensure _scikit-learn_ is installed.
2. **Configuration:** Adjust `config.py` as needed.
3. **Execution:** Run `main.py` to start the analysis with your configurations.

## Acknowledgments

This project utilizes data from the Alzheimer's Disease Neuroimaging Initiative (ADNI), and we acknowledge their invaluable contribution to Alzheimer's Disease research. 

Special thanks to Mr. Alireza Fathian and Prof. Yousef Jamali for providing referencing data; their paper "The trend of disruption in the functional brain network topology of Alzheimer’s disease" ([Nature](https://www.nature.com/articles/s41598-022-18987-y)) has greatly inspired the pre-processing steps undertaken in this project. 

Additionally, we are grateful for the guidance and resources provided by my advisor, Prof. Songdechakraiwut, particularly the code for topological clustering available at [topo-clustering](https://github.com/topolearn/topo-clustering). Their contributions have been instrumental in shaping the methodologies and analyses employed in our investigation.
