# main.py
# The main function that handles all the scripts and functions
# Author: Boqian Shi

import config
from src.subject import Subject, SubjectLoader
from src.barcode import get_barcode, plot_barcode

# Write subject information into new CSV file
def write_current():
    # Find unmatched items
    subject_manager = SubjectLoader()
    subject_manager.load_subject_data()
    subject_manager.save_subjects_to_csv("./matrix_subjects.csv")

def print_subject_info(subject_manager):
    # Get subjects belonging to a specific group
    for group in config.groups:
        ad_subjects = subject_manager.get_subjects_by_group(group)
        print(f"\nSubjects in group {group}: ({len(ad_subjects)} subjects)")
        for subject in ad_subjects:
            print(subject)


# Load subject information from CSV file
def load_content():
    # Load subject information from CSV file
    subject_manager = SubjectLoader()

    # Load subject data from directory
    subject_manager.load_subject_data()

    # print_subject_info(subject_manager)

    if len(subject_manager.subjects) == config.num_subjects:
        print("All" , len(subject_manager.subjects), "subjects loaded successfully.")
    else:
        print("Error loading subjects, expected ", config.num_subjects, " but got ", len(subject_manager.subjects))

    return subject_manager

# Generate barcode representation of the network
def generate_barcode(subject_manager):
    for subject in subject_manager.subjects:
        # Set the barcode mode to config values
        barcode = get_barcode(subject.data, mode=config.barcode_mode)
        plot_barcode(barcode)


if __name__ == '__main__':
    subject_manager = load_content()
