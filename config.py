# config.py
# Configuration file for the project
# Author: Boqian Shi
# Store all the global variables and configurations here

# Group names
groups = ['AD', 'CN', 'LMCI', 'EMCI', 'MCI']

# Total number of subjects
num_subjects = 117

# Barcode mode
# options: 1. "component" 
#          2. "cycle"
#          3. "attached"
barcode_mode = "attached"

# adjacancy matrix mode
# options: 1. "original"
#          2. "ignore_negative"
#          3. "absolute"
adj_mode = "ignore_negative"

# Geometry mode
# options: 1. "geo_included" -  geometric info included
#          2. "topo" -  geometric info excluded
geo_mode = "topo"


# Label mode
# options: 1. "original"
#          2. "binary"
label_mode = "binary"

# Directory containing the subject data files
data_dir = './data'

# CSV file containing subject information
subject_csv_file = './matrix_subjects.csv'

# debug flag
debug = 0