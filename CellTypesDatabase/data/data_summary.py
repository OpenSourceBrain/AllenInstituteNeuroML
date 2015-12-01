
import os
import os.path
import json

import matplotlib.pyplot as plt

analysed = []

analysed = [ f for f in os.listdir('.') if (f.endswith('_analysis.json')) ]

analysed.sort()

for f in analysed:
    
    with open(f, "r") as json_file:
        data = json.load(json_file)
        
    id = data['data_set_id']
    sweeps = data['sweeps']
    
    print("Looking at data analysis in %s (dataset: %s)"%(f,id))
    
    currents_v_sub = {}
    currents_rate_spike = {}
    
    for s in sweeps.keys():
        current = float(sweeps[s]["sweep_metadata"]["aibs_stimulus_amplitude_pa"])
        print("Sweep %s (%s pA)"%(s, current))
        
        freq_key = '%s:mean_spike_frequency'%(s)
        steady_state_key = '%s:average_1000_1200'%(s)
        
        if sweeps[s]["pyelectro_iclamp_analysis"].has_key(freq_key):
            currents_rate_spike[current] = sweeps[s]["pyelectro_iclamp_analysis"][freq_key]
        else:
            currents_rate_spike[current] = 0
            currents_v_sub[current] = sweeps[s]["pyelectro_iclamp_analysis"][steady_state_key]
            
    plt.figure()
    curents = currents_v_sub.keys()
    curents.sort()
    plt.plot(curents, [currents_v_sub[c] for c in curents], color='k', linestyle='-', marker='o')
    
    plt.figure()
    curents = currents_rate_spike.keys()
    curents.sort()
    plt.plot(curents, [currents_rate_spike[c] for c in curents], color='k', linestyle='-', marker='o')

    
plt.show()