# Based on https://github.com/stripathy/AIBS_cell_types/blob/master/Allen_ephys_playground.ipynb

from allensdk.api.queries.cell_types_api import CellTypesApi
import os

ct = CellTypesApi()

dataset_id = 471141261

raw_ephys_file_name = '%d_raw_data.nwb' % dataset_id

if not os.path.isfile(raw_ephys_file_name):
    print('Downloading data: %s'%raw_ephys_file_name)
    ct.save_ephys_data(dataset_id, raw_ephys_file_name)

    print('Saved: %s'%raw_ephys_file_name)
    
print('Loading data from: %s'%raw_ephys_file_name)

from allensdk.core.nwb_data_set import NwbDataSet
data_set = NwbDataSet(raw_ephys_file_name)

import matplotlib.pyplot as plt
import numpy as np

sweep_numbers = range(54,58)
sweep_numbers = [34,38,42,46,50,54,58]

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

    metadata = data_set.get_sweep_metadata(sweep_number)
    ampl = round(metadata['aibs_stimulus_amplitude_pa'],4)

    # plot the stimulus and the voltage response for the random trial
    plt.subplot(2,1,1)
    plt.plot(time_pts,stimulus)
    plt.ylabel('Stimulus (A)')
    plt.subplot(2,1,2)
    plt.plot(time_pts,response, label = 'S %s, %s pA'%(sweep_number, ampl))

plt.ylabel('Membrane voltage (mV)')
plt.xlabel('Time (s)')
plt.legend()
plt.show()

