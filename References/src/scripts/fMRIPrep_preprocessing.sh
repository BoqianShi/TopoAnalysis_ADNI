#!/bin/bash
BASEDIR=$(readlink -f "$0")
ROOTDIR=${BASEDIR%/src/scripts/fMRIPrep_preprocessing.sh}
BIDSDIR=$ROOTDIR/data/01_bids
DERIVSDIR=$ROOTDIR/data/02_fmriprep
FSlicense=$ROOTDIR/src/references/FSlicense/license.txt
echo subject ID:
read subid
sudo docker run -ti --rm \
	-v $BIDSDIR:/bids_dataset:ro \
	-v $DERIVSDIR:/outputs \
	-v $FSlicense:/opt/freesurfer/license.txt:ro \
	poldracklab/fmriprep /bids_dataset /outputs \
	participant --participant_label $subid \
	--notrack \
	--output-spaces {MNI152NLin2009cAsym,fsaverage5} \
	--ignore {fieldmaps,slicetiming} 
