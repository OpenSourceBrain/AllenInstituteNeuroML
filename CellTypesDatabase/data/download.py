# Based on https://github.com/stripathy/AIBS_cell_types/blob/master/Allen_ephys_playground.ipynb

from allensdk.api.queries.cell_types_api import CellTypesApi
import os

ct = CellTypesApi()

dataset_ids = [471141261, 464198958]

sweep_numbers_for_data = {}
sweep_numbers_for_data[471141261] = [34,38,42,46,50,54,58] # range(54,58)
sweep_numbers_for_data[464198958] = [20, 24, 36,28,30,32,34] # range(54,58)


for dataset_id in dataset_ids:

    raw_ephys_file_name = '%d_raw_data.nwb' % dataset_id

    if not os.path.isfile(raw_ephys_file_name):
        print('Downloading data: %s'%raw_ephys_file_name)
        ct.save_ephys_data(dataset_id, raw_ephys_file_name)

        print('Saved: %s'%raw_ephys_file_name)
    else:
        print('File: %s already present...'%raw_ephys_file_name)


    print('Loading data from: %s'%raw_ephys_file_name)

    from allensdk.core.nwb_data_set import NwbDataSet
    data_set = NwbDataSet(raw_ephys_file_name)

    import matplotlib.pyplot as plt
    import numpy as np
    plt.figure()

    sweep_numbers = sweep_numbers_for_data[dataset_id]

    subset = {}

    for sweep_number in sweep_numbers:
        sweep_data = data_set.get_sweep(sweep_number)

        # start/stop indices that exclude the experimental test pulse (if applicable)
        index_range = sweep_data['index_range']

        # stimulus is a numpy array in amps
        stimulus = sweep_data['stimulus'][index_range[0]:index_range[-1]]

        # response is a numpy array in volts
        response = sweep_data['response'][index_range[0]:index_range[-1]]*1000
        subset[sweep_number] = response

        # sampling rate is in Hz
        sampling_rate = sweep_data['sampling_rate']

        # define some time points in seconds (i.e., convert to absolute time)
        time_pts = np.arange(0,len(stimulus)/sampling_rate,1./sampling_rate)
        subset['t'] = time_pts

        metadata = data_set.get_sweep_metadata(sweep_number)
        ampl = round(metadata['aibs_stimulus_amplitude_pa'],4)

        # plot the stimulus and the voltage response for the random trial
        plt.subplot(2,1,1)
        plt.plot(time_pts,stimulus)
        plt.ylabel('Stimulus (A)')
        plt.subplot(2,1,2)
        plt.plot(time_pts,response, label = 'S %s, %s pA'%(sweep_number, ampl))

    volts_file = open('%s.dat'%dataset_id, 'w')
    max = 1.5 # s

    for i in range(len(subset['t'])):
        t = subset['t'][i]
        if t <= max:
            line = '%s '%t
            for s in sweep_numbers:
                line += '%s '% (float(subset[s][i])/1000)
            volts_file.write(line+'\n')
    volts_file.close()

    plt.ylabel('Membrane voltage (mV)')
    plt.xlabel('Time (s)')
    plt.legend()
    
plt.show()

