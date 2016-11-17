#Based on example code at: http://alleninstitute.github.io/AllenSDK/biophysical_perisomatic_script.html
    
from allensdk.model.biophysical_perisomatic.utils import Utils
from allensdk.model.biophysical_perisomatic.runner import load_description

import sys
import json

sys.path.append('../../data')
from data_helper import get_test_sweep
    
description = load_description('manifest.json')

# configure NEURON
utils = Utils(description)
h = utils.h

print("NEURON configured")

# configure model
morphology_path = description.manifest.get_path('MORPHOLOGY')
utils.generate_morphology(morphology_path.encode('ascii', 'ignore'))
utils.load_cell_parameters()

print("Cell loaded from: %s"%morphology_path)

# configure stimulus and recording
stimulus_path = description.manifest.get_path('stimulus_path')

run_params = description.data['runs'][0]

with open('manifest.json', "r") as json_file:
    manifest_info = json.load(json_file)
dataset_id = int(manifest_info['biophys'][0]["model_file"][1].split('_')[0])

sweeps = [get_test_sweep(dataset_id)]

junction_potential = description.data['fitting'][0]['junction_potential']
mV = 1.0e-3

h.load_file("../NEURON/cellCheck.hoc")

for sweep in sweeps:
    utils.setup_iclamp(stimulus_path, sweep=sweep)
    vec = utils.record_values()

    print("Running sweep: %i for %s ms (dt: %s ms)"%(sweep,h.tstop, h.dt))
    h.finitialize()
    h.psection()
    h("cellInfo()")
    h.run()

    print("Finished running sweep: %i, %i data points saved"%(sweep, len(vec['v'])))
    s_file = open('sweep_%i.v.dat'%(sweep),'w')
    for i in range(len(vec['v'])):
        s_file.write('%s\t%s\n'%(vec['t'][i]/1000.,vec['v'][i]/1000))
    s_file.close()
    