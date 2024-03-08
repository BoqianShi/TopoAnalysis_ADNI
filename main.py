# main.py
import config
from src.subject import Subject, SubjectLoader
from src.barcode import get_barcode, plot_barcode

def write_current():
    # Load subject information from CSV file
    subject_manager = SubjectLoader()
    subject_manager.load_subject_data()
    subject_manager.save_subjects_to_csv("./matrix_subjects.csv")

def load_content():
    # Load subject information from CSV file
    subject_manager = SubjectLoader()

    # Load subject data from directory
    subject_manager.load_subject_data()

    # Get subjects belonging to a specific group
    for group in config.groups:
        ad_subjects = subject_manager.get_subjects_by_group(group)
        print(f"\nSubjects in group {group}: ({len(ad_subjects)} subjects)")
        for subject in ad_subjects:
            print(subject)

if __name__ == '__main__':
    write_current()
