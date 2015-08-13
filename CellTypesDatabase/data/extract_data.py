# Based on https://github.com/stripathy/AIBS_cell_types/blob/master/Allen_ephys_playground.ipynb

import matplotlib.pyplot as plt
import numpy as np

from allensdk.api.queries.cell_types_api import CellTypesApi
import os

ct = CellTypesApi()

dataset_ids = [471141261]
dataset_id = 471141261

raw_ephys_file_name = '%d_raw_data.nwb' % dataset_id


from allensdk.core.nwb_data_set import NwbDataSet
data_set = NwbDataSet(raw_ephys_file_name)


sweep_numbers = data_set.get_experiment_sweep_numbers()
sweep_numbers.sort()

for sweep_number in sweep_numbers:
    
    sweep_data = data_set.get_sweep(sweep_number)

    # start/stop indices that exclude the experimental test pulse (if applicable)
    index_range = sweep_data['index_range']

    # stimulus is a numpy array in amps
    stimulus = sweep_data['stimulus'][index_range[0]:index_range[-1]]

    # response is a numpy array in volts
    response = sweep_data['response'][index_range[0]:index_range[-1]]*1000

    # sampling rate is in Hz
    sampling_rate = sweep_data['sampling_rate']

    # define some time points in seconds (i.e., convert to absolute time)
    time_pts = np.arange(0,len(stimulus)/sampling_rate,1./sampling_rate)
    
    print('Looking at sweep number: %i, from %ss to %ss, stim %sA -> %sA, response %smV -> %smV'%(sweep_number, time_pts[0], time_pts[-1], np.amin(stimulus), np.amax(stimulus), np.amin(response), np.amax(response)))
