import sys
import math
import os

sys.path.append("..")
import data_helper as DH 

from pyelectro import utils
from collections import OrderedDict
import operator

nwbs = [ f for f in os.listdir('.') if (f.endswith('data.nwb')) ]
dataset_ids = []
for n in nwbs:
    dataset_ids.append(int(n.split('_')[0]))


#dataset_ids = [464198958, 477135941]
##dataset_ids = [464198958]

file_bd = open('bulk_data_helper.py','w')
file_bd.write('\nDATASET_TARGET_SWEEPS = {}\n')

import matplotlib.pyplot as plt
import numpy as np

for dataset_id in dataset_ids:

    raw_ephys_file_name = '%d_raw_data.nwb' % dataset_id

    info = {}
 
    import h5py
    import numpy as np
    h5f = h5py.File(raw_ephys_file_name, "r")
    metas = ['aibs_cre_line','aibs_dendrite_type','intracellular_ephys/Electrode 1/location']
    for m in metas:
        d = h5f.get('/general/%s'%m)
        print("%s = \t%s"%(m,d.value))
        info[m.split('/')[-1]]=str(d.value)
    h5f.close()
    
    from allensdk.core.nwb_data_set import NwbDataSet
    data_set = NwbDataSet(raw_ephys_file_name)


    sweep_numbers = data_set.get_experiment_sweep_numbers()
    
    #sweep_numbers = [33,45]
        
    sweep_numbers.sort()

    print("All sweeps for %s: %s"%(dataset_id, sweep_numbers))
    subthreshs = {}
    spikings = {}
    spike_count = {}
    
    chosen = {}
    stimuli = {}

    for sweep_number in sweep_numbers:

        sweep_data = data_set.get_sweep(sweep_number)
        
        if data_set.get_sweep_metadata(sweep_number)['aibs_stimulus_name'] == "Long Square":
            sweep_info = {}
            sweep_info[DH.METADATA] = data_set.get_sweep_metadata(sweep_number)
            
            amp = float(sweep_info[DH.METADATA]['aibs_stimulus_amplitude_pa'])
            if abs(amp-math.ceil(amp))<1e-5:
                amp=int(math.ceil(amp))
            if abs(amp-math.floor(amp))<1e-5:
                amp=int(math.floor(amp))
            print("Sweep: %s (%s pA): %s"%(sweep_number,amp,sweep_info[DH.METADATA]))
            

            # start/stop indices that exclude the experimental test pulse (if applicable)
            index_range = sweep_data['index_range']

            # stimulus is a numpy array in amps
            stimulus = sweep_data['stimulus'][index_range[0]:index_range[-1]]
            stimuli[sweep_number] = stimulus
            
            # response is a numpy array in volts
            response = sweep_data['response'][index_range[0]:index_range[-1]]*1000
            chosen[sweep_number] = response
            
            # sampling rate is in Hz
            sampling_rate = sweep_data['sampling_rate']

            # define some time points in seconds (i.e., convert to absolute time)
            time_pts = np.arange(0,len(stimulus)/sampling_rate,1./sampling_rate)*1000
            chosen['t'] = time_pts

            comment = 'Sweep: %i in %i; %sms -> %sms; %sA -> %sA; %smV -> %smV'%(sweep_number, dataset_id, time_pts[0], time_pts[-1], np.amin(stimulus), np.amax(stimulus), np.amin(response), np.amax(response))
            print(comment)
            
            analysis = utils.simple_network_analysis({sweep_number:response}, 
                                                     time_pts, 
                                                     end_analysis=1500, 
                                                     plot=False, 
                                                     show_plot_already=False,
                                                     verbose=False)
            spike_count[sweep_number] = analysis['%s:max_peak_no'%sweep_number]             
            subthresh = analysis['%s:max_peak_no'%sweep_number] == 0
            if subthresh:
                subthreshs[sweep_number] = amp
            else:
                spikings[sweep_number] = amp

    subthreshs = OrderedDict(sorted(subthreshs.items(), key=operator.itemgetter(1)))
    spikings = OrderedDict(sorted(spikings.items(), key=operator.itemgetter(1)))
    
    print("Subthreshold sweeps: %s"%subthreshs)
    print("Spiking sweeps: %s"%spikings)
    
    chosen_sweeps = []
    
    add_this = True
    if dataset_id in DH.DATASET_TARGET_SWEEPS:
        chosen_sweeps = DH.DATASET_TARGET_SWEEPS[dataset_id]
        
        print("Reusing chosen sweeps: %s"%chosen_sweeps)
    else:
        if len(subthreshs)<4:
            print("Cannot pick 4 subthreshold values")
            add_this = False
        elif len(spikings)<4:
            print("Cannot pick 4 spiking values")
            add_this = False
        else:
            i1 = -1 
            i2 = -1
            if len(subthreshs)==4 :
                i1=1
                i2=2
            elif len(subthreshs)==5 or len(subthreshs)==6:
                i1=1
                i2=3
            else:
                q = int(math.ceil(len(subthreshs)/4.))
                i1 = q
                i2 = len(subthreshs)-q
            print("Picking subthresh indices 0, %s, %s, %s"%(i1,i2,len(subthreshs)-1))
            chosen_sweeps.append(subthreshs.keys()[0])
            chosen_sweeps.append(subthreshs.keys()[i1])
            chosen_sweeps.append(subthreshs.keys()[i2])
            chosen_sweeps.append(subthreshs.keys()[-1])

            i1 = int(math.ceil(len(spikings)/2.))
            print("Picking spiking indices 0, %s, %s"%(i1,len(spikings)-1))

            i0 = 1
            i2 = -1
            min_spike_count = 3
            chosen_sweeps.append(spikings.keys()[i0]) #!!!!!!!
            if spike_count[spikings.keys()[i0]] < min_spike_count: add_this = False
            chosen_sweeps.append(spikings.keys()[i1])
            if spike_count[spikings.keys()[i1]] < min_spike_count: add_this = False
            chosen_sweeps.append(spikings.keys()[i2])
            if spike_count[spikings.keys()[i1]] < min_spike_count: add_this = False

            print("Chosen sweeps: %s"%chosen_sweeps)
            print("Retrieved sweep traces: %s"%chosen.keys())

    if add_this:
        file_bd.write("\nDATASET_TARGET_SWEEPS[%s] = %s\n"%(dataset_id,chosen_sweeps))


    volts_file = open('%s.dat'%dataset_id, 'w')
    max = 1500 # s

    imax =-1
    for i in range(len(chosen['t'])):
        t = chosen['t'][i]
        if t <= max:
            line = '%s '%t
            for s in chosen_sweeps:
                line += '%s '% (float(chosen[s][i])/1000)
            volts_file.write(line+'\n')
            imax=i
    volts_file.close()

    fig = plt.figure()

    for s in chosen_sweeps:
        # plot the stimulus and the voltage response for the random trial
        plt.subplot(2,1,1)
        tt = chosen['t'][:imax]
        vv = chosen[s][:imax]
        print("Plotting t: %s->%s #%s vs %s->%s #%s"%(tt[0],tt[-1],len(tt),vv[0],vv[-1],len(vv)))
        plt.plot(tt,vv)
        plt.ylabel('Stimulus (A)')
        plt.subplot(2,1,2)
        ss = stimuli[s][:imax]
        plt.plot(tt,ss, label = 'S %s, %s pA'%(sweep_number, spikings[s] if s in spikings else subthreshs[s]))

    plt.ylabel('Membrane voltage (mV)')
    plt.xlabel('Time (s)')
    fig.canvas.set_window_title("Dataset: %s"%dataset_id)
    plt.legend()
        
        
file_bd.write("\nCURRENT_DATASETS = DATASET_TARGET_SWEEPS.keys()\n")
        
file_bd.close()

plt.show()