# config.py
# Configuration file for the project
# Author: Boqian Shi
# Store all the global variables and configurations here

# Separation mode
# 1. mixed_separation:
#    AD + MCI + LMCI vs CN + EMCI
# 2. strict_binary:
#    AD vs CN (ignore the rest)
separation_mode = "strict_binary"

# Group names
groups = ['AD', 'CN', 'LMCI', 'EMCI', 'MCI']

# Total number of subjects
num_subjects = 117
num_strict_binary = 59

# Barcode mode
# Controls the way the barcode is computed
# attached mode: component + cycle
# options: 1. "component" 
#          2. "cycle"
#          3. "attached"
barcode_mode = "attached"

# adjacancy matrix mode
# options: 1. "original"
#          2. "ignore_negative"
#          3. "absolute"
adj_mode = "original"

# Geometry mode
# Controls the way the geometric information is included
# options: 1. "geo_included" -  geometric info included
#          2. "topo" -  geometric info excluded
geo_mode = "geo_included"


# Label mode
# options: 1. "original"
#          2. "binary"
label_mode = "original"

# Directory containing the subject data files
data_dir = './data'

# CSV file containing subject information
subject_csv_file = './matrix_subjects.csv'

# debug flag
debug = 0

# Random seed
# Best for strict binary separation = 2957; ari = 0.4271
# Best for mixed_separation = 86, ari = 0.154
random_seed = 2957