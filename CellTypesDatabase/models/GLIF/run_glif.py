usage = """

This script can be used to run a simulation of the GLIF cell model using the Allen SDK 

To run all the models used in this repo type:

    python run_glif.py -all

To run a test type:
    python run_glif.py -test

"""

import allensdk.core.json_utilities as json_utilities
from allensdk.model.glif.glif_neuron import GlifNeuron
from allensdk.core.nwb_data_set import NwbDataSet
from pyneuroml import pynml
import numpy as np
import os
import sys

test_sweep = {
    "566282032": 39,
    "566283540": 33,
    "566283879": 46,
    "566288171": 40,
    "486557295": 36,
    "566291893": 28,
    "566291897": 29,
    "566302725": 40,
    "566320096": 32,
    "489931668": 49,
    "486558431": 41,
    "566382734": 35,
    "486052403": 54,
    "485904755": 34,
    "566303332": 44,
    "566357260": 50,
}


def run_one_cell(neuronal_model_id, show_plot=False):
    print("Simulating model: %s" % neuronal_model_id)
    os.chdir(str(neuronal_model_id))

    neuron_config = json_utilities.read("neuron_config.json")[f"{neuronal_model_id}"]
    ephys_sweeps = json_utilities.read("ephys_sweeps.json")
    ephys_file_name = "stimulus.nwb"

    # pull out the stimulus for the test sweep
    ephys_sweep = next(
        s
        for s in ephys_sweeps
        if s["sweep_number"] == test_sweep[str(neuronal_model_id)]
    )
    ds = NwbDataSet(ephys_file_name)
    data = ds.get_sweep(ephys_sweep["sweep_number"])
    curr_pA = int(ephys_sweep["stimulus_absolute_amplitude"])

    # initialize the neuron
    # important! update the neuron's dt for your stimulus
    neuron = GlifNeuron.from_dict(neuron_config)
    neuron.dt = 1.0 / data["sampling_rate"]
    stimulus = (
        [0.0] * int(0.1 / neuron.dt)
        + [curr_pA * 1e-12] * int(1 / neuron.dt)
        + [0.0] * int(0.1 / neuron.dt)
    )

    # simulate the neuron
    output = neuron.run(stimulus)

    voltage = output["voltage"]
    threshold = output["threshold"]
    spike_times = output["interpolated_spike_times"]

    info = "Model %s; %spA stimulation; %i spikes" % (
        neuronal_model_id,
        ephys_sweep["stimulus_absolute_amplitude"],
        len(spike_times),
    )
    print(info)

    v_file = open(f'sweep_{ephys_sweep["sweep_number"]}.v.dat', "w")
    th_file = open(f'sweep_{ephys_sweep["sweep_number"]}.thresh.dat', "w")
    times = np.arange(len(stimulus)) * neuron.dt

    for i in range(len(times)):
        t = times[i]
        v = voltage[i]
        th = threshold[i]
        v_file.write("%s\t%s\n" % (t, v))
        th_file.write("%s\t%s\n" % (t, th))
    v_file.close()
    th_file.close()

    print("Plotting...")
    pynml.generate_plot(
        [times],
        [voltage],
        "Membrane potential; %s" % info,
        colors=["k"],
        xaxis="Time (s)",
        yaxis="Voltage (V)",
        # xlim=(0.9, 2.1),
        grid=True,
        show_plot_already=show_plot,
        save_figure_to="MembranePotential_%ipA.png" % (curr_pA),
    )

    pynml.generate_plot(
        [times],
        [threshold],
        "Threshold; %s" % info,
        colors=["r"],
        xaxis="Time (s)",
        yaxis="Voltage (V)",
        # xlim=(0.9, 2.1),
        grid=True,
        show_plot_already=show_plot,
        save_figure_to="Threshold_%ipA.png" % (curr_pA),
    )

    os.chdir("../")


if __name__ == "__main__":

    if "-all" in sys.argv:
        from download_glif import GLIF_MODEL_IDS, GLIF_MODEL_IDS_FOR_NETWORK_BUILD

        for model in GLIF_MODEL_IDS + GLIF_MODEL_IDS_FOR_NETWORK_BUILD:
            run_one_cell(model)
        exit()

    if "-test" in sys.argv:
        run_one_cell(566291893)
        exit()

    else:
        print(usage)
