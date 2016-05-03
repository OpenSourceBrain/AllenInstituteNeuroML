import allensdk.core.json_utilities as json_utilities
from allensdk.model.glif.glif_neuron import GlifNeuron

# initialize the neuron
neuron_config = json_utilities.read('neuron_config.json')
neuron = GlifNeuron.from_dict(neuron_config)

# important! set the neuron's dt value for your stimulus in seconds
neuron.dt = 5e-6

# make a short square pulse. stimulus units should be in Amps.
stimulus = [ 0.0 ] * int(0.1/neuron.dt) + [ 50e-12 ] * int(1/neuron.dt) + [ 0.0 ] * int(0.1/neuron.dt)


# simulate the neuron
output = neuron.run(stimulus)

print "run.."

voltage = output['voltage']
threshold = output['threshold']
spike_times = output['interpolated_spike_times']

print spike_times
