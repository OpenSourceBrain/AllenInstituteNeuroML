# Based on https://github.com/stripathy/AIBS_cell_types/blob/master/Allen_ephys_playground.ipynb

import matplotlib.pyplot as pylab
import numpy as np

from allensdk.api.queries.cell_types_api import CellTypesApi
import time

import info_file as IF

from pyelectro import utils
from pyelectro import __version__ as pyel_ver

import pprint
pp = pprint.PrettyPrinter(indent=4)

ct = CellTypesApi()

dataset_ids = [471141261]

plot = True

for dataset_id in dataset_ids:

    raw_ephys_file_name = '%d_raw_data.nwb' % dataset_id


    from allensdk.core.nwb_data_set import NwbDataSet
    data_set = NwbDataSet(raw_ephys_file_name)


    sweep_numbers = data_set.get_experiment_sweep_numbers()
    sweep_numbers.sort()

    sweep_numbers = range(34,58)  # just for 471141261
    sweep_numbers = range(55,58)  # just for 471141261

    info = {}
    info[IF.DATASET] = dataset_id
    info[IF.COMMENT] = 'Data analysed on %s'%(time.ctime())
    
    info[IF.PYELECTRO_VERSION] = pyel_ver
    info[IF.SWEEPS] = []

    for sweep_number in sweep_numbers:

        sweep_data = data_set.get_sweep(sweep_number)
        
        sweep_info = {}
        info[IF.SWEEPS].append(sweep_info)
        sweep_info[IF.SWEEP] = sweep_number
        

        # start/stop indices that exclude the experimental test pulse (if applicable)
        index_range = sweep_data['index_range']

        # stimulus is a numpy array in amps
        stimulus = sweep_data['stimulus'][index_range[0]:index_range[-1]]

        # response is a numpy array in volts
        response = sweep_data['response'][index_range[0]:index_range[-1]]*1000

        # sampling rate is in Hz
        sampling_rate = sweep_data['sampling_rate']

        # define some time points in seconds (i.e., convert to absolute time)
        time_pts = np.arange(0,len(stimulus)/sampling_rate,1./sampling_rate)*1000

        comment = 'Sweep: %i in %i; %sms -> %sms; %sA -> %sA; %smV -> %smV'%(sweep_number, dataset_id, time_pts[0], time_pts[-1], np.amin(stimulus), np.amax(stimulus), np.amin(response), np.amax(response))
        print(comment)
        
        sweep_info[IF.COMMENT] = comment
        
        analysis = utils.simple_network_analysis({sweep_number:response}, 
                                                 time_pts, 
                                                 end_analysis=1300, 
                                                 plot=plot, 
                                                 show_plot_already=False,
                                                 verbose=True)
        
        sweep_info[IF.ICLAMP_ANALYSIS] = analysis

    analysis_file_name = '%s_analysis.json'%(dataset_id)
    analysis_file = open(analysis_file_name, 'w')
    analysis_file.write(pp.pformat(info))
    analysis_file.close()
    
    print('Written info to %s'%analysis_file_name)
    
if plot:
    pylab.show()
    
    
    