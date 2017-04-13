
import sys
import bulk_data_helper as BDH


sys.path.append("..")
from extract_data import extract_info_from_nwb_file

dataset_ids = BDH.CURRENT_DATASETS


for dataset_id in dataset_ids:
    
    raw_ephys_file_name = '%d_raw_data.nwb' % dataset_id
    print("Extracting from: "+raw_ephys_file_name)
    extract_info_from_nwb_file(dataset_id, raw_ephys_file_name)

