# subject.py
# Functions for read the adjacency matrix of the network
# Store in class Subject
# Author: Boqian Shi

import config
import os
import csv
import numpy as np

class Subject:
    def __init__(self, subject_id, group=None):
        self.subject_id = subject_id
        self.group = group
        self.sex = None
        self.age = None
        self.data = None
        self.barcode = None

    def load_data(self, data_dir):
        """
        Loads the data for the subject from the specified directory.

        Args:
            data_dir (str): Directory containing the subject's data file.
        """
        file_name = f"sub-{self.subject_id}.npy"
        file_path = os.path.join(data_dir, file_name)
        if os.path.exists(file_path):
            self.data = np.load(file_path)

    def set_barcode(self, barcode):
        """
        Sets the barcode representation of the network for the subject.

        Args:
            barcode (numpy.ndarray): Barcode representation of the network.
        """
        self.barcode = barcode

    def __str__(self):
        return f"Subject ID: {self.subject_id}, Group: {self.group}"

class SubjectLoader:
    def __init__(self):
        self.subjects = []
        self.load_subjects_from_data_dir()
        self.load_subjects_from_csv(config.subject_csv_file)

    def load_subjects_from_data_dir(self):
        """
        Loads subjects from the data directory.
        """
        for file_name in os.listdir(config.data_dir):
            if file_name.endswith('.npy'):
                subject_id = file_name[4:12]  # Extract the subject ID from the file name
                subject = Subject(subject_id)
                self.subjects.append(subject)

    def load_subjects_from_csv(self, csv_file):
        """
        Updates subject information from a CSV file for existing subjects.

        Args:
            csv_file (str): Path to the CSV file containing subject information.
        """
        subject_ids_in_data_dir = set(subject.subject_id for subject in self.subjects)

        with open(csv_file, 'r') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                subject_id = row.get('participant_id')
                if subject_id in subject_ids_in_data_dir:
                    subject = self.get_subject_by_id(subject_id)
                    if subject:
                        subject.group = row.get('group')

    def save_subjects_to_csv(self, output_file):
        """
        Saves subject information and data file paths to a CSV file.

        Args:
            output_file (str): Path to the output CSV file.
        """
        fieldnames = ['participant_id', 'group', 'data_file']

        with open(output_file, 'w', newline='') as file:
            csv_writer = csv.DictWriter(file, fieldnames=fieldnames)
            csv_writer.writeheader()

            for subject in self.subjects:
                data_file = os.path.join(config.data_dir, f"sub-{subject.subject_id}.npy")
                if os.path.exists(data_file):
                    row = {
                        'participant_id': subject.subject_id,
                        'group': subject.group,
                        'data_file': data_file
                    }
                    csv_writer.writerow(row)
                    
    def load_subject_data(self):
        """
        Loads data for all subjects from the data directory.
        """
        for subject in self.subjects:
            subject.load_data(config.data_dir)

    def strict_binary_label(self):
        """
        Discard all EMCI, MCI, LMCI subjects.
        """
        temp = []
        for subject in self.subjects:
            if subject.group != 'MCI' and subject.group != 'EMCI' and subject.group != 'LMCI':
                temp.append(subject)
        self.subjects = temp


    def binary_label(self):
        """
        Convert the label to binary.
        """
        for subject in self.subjects:
            if subject.group == 'AD' or subject.group == 'LMCI' or subject.group == 'MCI':
                subject.group = 1
            else:
                subject.group = 0

    def original_label(self):
        """
        Convert the label to binary.
        """
        for subject in self.subjects:
            if subject.group == 'AD':
                subject.group = 0
            elif subject.group == 'EMCI':
                subject.group = 1
            elif subject.group == 'LMCI' or subject.group == 'MCI':
                subject.group = 2
            elif subject.group == 'CN':
                subject.group = 3
            else:
                print("Error: Label mismatched on subject: ", subject.subject_id, " Please check the label.")
            

    def get_subject_by_id(self, subject_id):
        """
        Retrieves a subject object by its ID.

        Args:
            subject_id (str): ID of the subject.

        Returns:
            Subject: Subject object with the specified ID, or None if not found.
        """
        for subject in self.subjects:
            if subject.subject_id == subject_id:
                return subject
        return None

    def get_subjects_by_group(self, group):
        """
        Retrieves a list of subject objects belonging to a specific group.

        Args:
            group (str): Group name.

        Returns:
            list: List of Subject objects belonging to the specified group.
        """
        return [subject for subject in self.subjects if subject.group == group]

    def get_labels(self):
        """
        Retrieves the labels of the subjects.

        Returns:
            list: List of labels of the subjects.
        """
        labels_true = []
        for subject in self.subjects:
            labels_true.append(subject.group)
            print("Subject ID: ", subject.subject_id, " Label: ", subject.group)
        return labels_true