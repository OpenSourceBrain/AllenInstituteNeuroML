import allensdk.core.json_utilities as json_utilities
from allensdk.model.glif.glif_neuron import GlifNeuron


from pyneuroml import pynml

# initialize the neuron
neuron_config = json_utilities.read('neuron_config.json')
neuron = GlifNeuron.from_dict(neuron_config)

# important! set the neuron's dt value for your stimulus in seconds
neuron.dt = 5e-6

# make a short square pulse. stimulus units should be in Amps.
stimulus = [ 0.0 ] * int(0.1/neuron.dt) + [ 150e-12 ] * int(1/neuron.dt) + [ 0.0 ] * int(0.1/neuron.dt)
times = [ i*neuron.dt for i in range(len(stimulus)) ]

# simulate the neuron
output = neuron.run(stimulus)

print "run.."

voltage = output['voltage']
threshold = output['threshold']
spike_times = output['interpolated_spike_times']

print spike_times


pynml.generate_plot([times],
                        [voltage], 
                        "vv", 
                        colors = ['k'], 
                        linestyles=['-'],
                        xaxis = "Time (s)", 
                        yaxis = "Voltage (mV)", 
                        grid = True,
                        show_plot_already=True)
