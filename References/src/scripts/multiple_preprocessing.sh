#!/bin/bash

# Base directory is the directory of this script
BASEDIR=$(readlink -f "$0")
# Root directory is the parent of the 'src/scripts' directory
ROOTDIR=${BASEDIR%/src/scripts/fMRIPrep_preprocessing.sh}
# BIDS directory
BIDSDIR=$ROOTDIR/data/01_bids
# Derivatives directory
DERIVSDIR=$ROOTDIR/data/02_fmriprep
# FreeSurfer license file
FSlicense=$ROOTDIR/src/references/FSlicense/license.txt

# Define subject IDs here, separated by spaces
subids=(002S0413 002S0685 002S1261 002S1280 002S2010 002S2043 002S2073 002S4171 002S4213 002S4219 002S4225 002S4229 002S4237 002S4251 002S4262 002S4264 002S4270 002S4447 002S4473 ) # Example subject IDs

# Loop over each subject ID
for subid in "${subids[@]}"; do
    echo "Processing subject: $subid"
    sudo docker run -ti --rm \
        -v $BIDSDIR:/bids_dataset:ro \
        -v $DERIVSDIR:/outputs \
        -v $FSlicense:/opt/freesurfer/license.txt:ro \
        poldracklab/fmriprep /bids_dataset /outputs \
        participant --participant_label $subid \
        --notrack \
        --output-spaces {MNI152NLin2009cAsym,fsaverage5} \
        --ignore {fieldmaps,slicetiming}
done
