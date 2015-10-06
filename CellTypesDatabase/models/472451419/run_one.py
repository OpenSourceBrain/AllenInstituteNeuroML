#Based on example code at: http://alleninstitute.github.io/AllenSDK/biophysical_perisomatic_script.html
    
from allensdk.model.biophysical_perisomatic.utils import Utils
from allensdk.model.biophysical_perisomatic.runner import load_description

    
description = load_description('manifest.json')

# configure NEURON
utils = Utils(description)
h = utils.h

print("NEURON configured")

# configure model
manifest = description.manifest
morphology_path = description.manifest.get_path('MORPHOLOGY')
utils.generate_morphology(morphology_path.encode('ascii', 'ignore'))
utils.load_cell_parameters()

print("Cell loaded from: %s"%morphology_path)

# configure stimulus and recording
stimulus_path = description.manifest.get_path('stimulus_path')

run_params = description.data['runs'][0]
sweeps = [23, 57, 60]

junction_potential = description.data['fitting'][0]['junction_potential']
mV = 1.0e-3

for sweep in sweeps:
    utils.setup_iclamp(stimulus_path, sweep=sweep)
    vec = utils.record_values()

    print("Running sweep: %i"%(sweep))
    h.finitialize()
    h.psection()
    h.run()

    print("Finished running sweep: %i, %i data points saved"%(sweep, len(vec['v'])))
    s_file = open('sweep_%i.v.dat'%(sweep),'w')
    for i in range(len(vec['v'])):
        s_file.write('%s\t%s\n'%(vec['t'][i],vec['v'][i]))
    s_file.close()