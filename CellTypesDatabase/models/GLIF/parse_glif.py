usage = """

This file can be used to generate LEMS components for each of a number of GLIF models

Usage:

    To test parsing with one model:
        python parse_glif.py -test

    To parse all models:
        python parse_glif.py -all

"""

import sys
import os
import json

from pyneuroml import pynml

from neuromllite import Network, Cell, InputSource, Population, SingleLocation, Location
from neuromllite import Input, Simulation
from neuromllite.NetworkGenerator import check_to_generate_or_run


def generate_lems(glif_dir, sweep_number, show_plot=True):

    os.chdir(glif_dir)

    with open("model_metadata.json", "r") as json_file:
        model_metadata = json.load(json_file)

    with open("neuron_config.json", "r") as json_file:
        neuron_config = json.load(json_file)[f"{glif_dir}"]

    with open("ephys_sweeps.json", "r") as json_file:
        ephys_sweeps = json.load(json_file)

    ephys_sweep = next(s for s in ephys_sweeps if s["sweep_number"] == sweep_number)
    curr_pA = int(ephys_sweep["stimulus_absolute_amplitude"])

    template_cell = """<Lems>
      <Include file="../GLIFs.xml"/>

      <%s %s/>

    </Lems>
    """

    type = "???"
    print(model_metadata["name"])
    if "(LIF)" in model_metadata["name"]:
        type = "glifCell"
    if "(LIF-ASC)" in model_metadata["name"]:
        type = "glifAscCell"
    if "(LIF-R)" in model_metadata["name"]:
        type = "glifRCell"
    if "(LIF-R-ASC)" in model_metadata["name"]:
        type = "glifRAscCell"
    if "(LIF-R-ASC-A)" in model_metadata["name"]:
        type = "glifRAscATCell"

    cell_id = "GLIF_%s" % glif_dir

    attributes = ""

    attributes += ' id="%s"' % cell_id
    attributes += '\n            C="%s F"' % neuron_config["C"]
    attributes += '\n            leakReversal="%s V"' % neuron_config["El"]
    attributes += '\n            reset="%s V"' % neuron_config["El"]
    attributes += '\n            thresh="%s V"' % (
        float(neuron_config["th_inf"]) * float(neuron_config["coeffs"]["th_inf"])
    )
    attributes += '\n            leakConductance="%s S"' % (
        1 / float(neuron_config["R_input"])
    )

    if "Asc" in type:
        attributes += '\n            tau1="%s s"' % neuron_config["asc_tau_array"][0]
        attributes += '\n            tau2="%s s"' % neuron_config["asc_tau_array"][1]
        attributes += '\n            amp1="%s A"' % (
            float(neuron_config["asc_amp_array"][0])
            * float(neuron_config["coeffs"]["asc_amp_array"][0])
        )
        attributes += '\n            amp2="%s A"' % (
            float(neuron_config["asc_amp_array"][1])
            * float(neuron_config["coeffs"]["asc_amp_array"][1])
        )

    if "glifR" in type:
        attributes += (
            '\n            bs="%s per_s"'
            % neuron_config["threshold_dynamics_method"]["params"]["b_spike"]
        )
        attributes += (
            '\n            deltaThresh="%s V"'
            % neuron_config["threshold_dynamics_method"]["params"]["a_spike"]
        )
        attributes += (
            '\n            fv="%s"'
            % neuron_config["voltage_reset_method"]["params"]["a"]
        )
        attributes += (
            '\n            deltaV="%s V"'
            % neuron_config["voltage_reset_method"]["params"]["b"]
        )

    if "glifRAscATCell" in type:
        attributes += (
            '\n            bv="%s per_s"'
            % neuron_config["threshold_dynamics_method"]["params"]["b_voltage"]
        )
        attributes += (
            '\n            a="%s per_s"'
            % neuron_config["threshold_dynamics_method"]["params"]["a_voltage"]
        )

    file_contents = template_cell % (type, attributes)

    print(file_contents)

    cell_file_name = "%s__lems.xml" % (cell_id)
    cell_file = open(cell_file_name, "w")
    cell_file.write(file_contents)
    cell_file.close()

    net = Network(id="Test_%s" % glif_dir)
    net.notes = model_metadata["name"]
    net.temperature = 32.0
    net.seed = 1234

    cell = Cell(id="GLIF_%s" % glif_dir, lems_source_file="%s__lems.xml" % (cell_id))
    net.cells.append(cell)

    pop = Population(
        id="pop_%s" % glif_dir,
        size=1,
        component=cell.id,
        single_location=SingleLocation(location=Location(x=0, y=0, z=0)),
    )

    net.populations.append(pop)

    input_source = InputSource(
        id="pg0",
        neuroml2_input="pulseGenerator",
        parameters={
            "delay": "100ms",
            "duration": "1000ms",
            "amplitude": "%s pA" % curr_pA,
        },
    )

    net.input_sources.append(input_source)

    net.inputs.append(
        Input(
            id="Stim0", input_source=input_source.id, population=pop.id, percentage=100
        )
    )

    new_file = net.to_json_file("%s.json" % net.id)

    thresh = "thresh"
    if "glifR" in type:
        thresh = "threshTotal"

    sim = Simulation(
        id="Sim_Test_%s" % glif_dir,
        network=new_file,
        duration="1200",
        dt="0.01",
        record_traces={"all": "*"},
        record_variables={thresh: {"all": "*"}},
    )
    sim.to_json_file("Sim_Test_%s.nmllite.json" % glif_dir)

    check_to_generate_or_run(["-jnml"], sim)

    simulation_model_v = f"Sim_Test_{glif_dir}.pop_{glif_dir}.v.dat"
    if os.path.isfile(simulation_model_v):
        data, indices = pynml.reload_standard_dat_file(simulation_model_v)
        times = [data["t"]]
        vs = [data[0]]
        labels = ["LEMS - jNeuroML"]

    info = "Model %s; %spA stimulation" % (glif_dir, curr_pA)
    original_model_v = f"sweep_{sweep_number}.v.dat"
    if os.path.isfile(original_model_v):
        data, indices = pynml.reload_standard_dat_file(original_model_v)
        times.append(data["t"])
        vs.append(data[0])
        labels.append("Allen SDK")

    pynml.generate_plot(
        times,
        vs,
        "Membrane potential; %s" % info,
        xaxis="Time (s)",
        yaxis="Voltage (V)",
        labels=labels,
        grid=True,
        show_plot_already=False,
        save_figure_to="Comparison_%ipA.png" % (curr_pA),
    )

    simulation_model_thresh = f"pop_{glif_dir}_0.{thresh}.dat"
    if os.path.isfile(simulation_model_thresh):
        data, indices = pynml.reload_standard_dat_file(simulation_model_thresh)
        times = [data["t"]]
        vs = [data[0]]
        labels = ["LEMS - jNeuroML"]

    original_model_th = f"sweep_{sweep_number}.thresh.dat"
    if os.path.isfile(original_model_th):
        data, indeces = pynml.reload_standard_dat_file(original_model_th)
        times.append(data["t"])
        vs.append(data[0])
        labels.append("Allen SDK")

    pynml.generate_plot(
        times,
        vs,
        "Threshold; %s" % info,
        xaxis="Time (s)",
        yaxis="Voltage (V)",
        labels=labels,
        grid=True,
        show_plot_already=show_plot,
        save_figure_to="Comparison_Threshold_%ipA.png" % (curr_pA),
    )

    readme = """
## Model: %(id)s

### Original model

%(name)s

[Allen Cell Types DB electrophysiology page for specimen](http://celltypes.brain-map.org/mouse/experiment/electrophysiology/%(spec)s)

[Neuron configuration](neuron_config.json); [model metadata](model_metadata.json); [electrophysiology summary](ephys_sweeps.json)

#### Original traces:

**Membrane potential**

Current injection of %(curr)s pA

![Original](MembranePotential_%(curr)spA.png)

**Threshold**

![Threshold](Threshold_%(curr)spA.png)

### Conversion to NeuroML 2

LEMS version of this model: [GLIF_%(id)s.xml](GLIF_%(id)s.xml)

[Definitions of LEMS Component Types](../GLIFs.xml) for GLIFs.

This model can be run locally by installing [jNeuroML](https://github.com/NeuroML/jNeuroML) and running:

    jnml LEMS_Test_%(id)s.xml

#### Comparison:

**Membrane potential**

Current injection of %(curr)s pA

![Comparison](Comparison_%(curr)spA.png)

**Threshold**

![Comparison](Comparison_Threshold_%(curr)spA.png)"""

    readme_file = open("README.md", "w")
    curr_str = str(curr_pA)
    # @type curr_str str
    if curr_str.endswith(".0"):
        curr_str = curr_str[:-2]
    readme_file.write(
        readme
        % {
            "id": glif_dir,
            "name": model_metadata["name"],
            "spec": model_metadata["specimen_id"],
            "curr": curr_str,
        }
    )
    readme_file.close()

    os.chdir("..")

    return model_metadata, neuron_config, ephys_sweeps, curr_str


if __name__ == "__main__":

    if "-test" in sys.argv:
        models_stims = {"566291893": 28}

    elif "-all" in sys.argv:

        models_stims = {
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

    elif len(sys.argv) == 3:

        glif_dir = sys.argv[1]
        curr_pA = float(sys.argv[2])
        show_plot = "-nogui" not in sys.argv
        generate_lems(glif_dir, curr_pA, show_plot=show_plot)
        exit()

    else:
        print(usage)
        exit()

    readme = """
## Conversion of Allen Cell Types Database GLIF models to NeuroML 2

| Model details | Comparison | Injection Current |
| ----- | -------- | --- |
"""

    for model in models_stims.keys():

        print("\n------- Converting model: %s" % model)

        model_metadata, neuron_config, ephys_sweeps, curr_str = generate_lems(
            model, models_stims[model], show_plot=False
        )

        if curr_str.endswith(".0"):
            curr_str = curr_str[:-2]
        readme += """| [%(id)s](http://celltypes.brain-map.org/mouse/experiment/electrophysiology/%(spec)s) <br> %(name)s <br> [Conversion details](%(id)s/README.md)| <a href="%(id)s/README.md"><img alt="%(id)s" src="%(id)s/Comparison_%(curr)spA.png" height="300"/></a> | %(curr)spA |
""" % {
            "id": model,
            "name": model_metadata["name"],
            "spec": model_metadata["specimen_id"],
            "curr": curr_str,
        }

    readme_file = open("README.md", "w")
    readme_file.write(readme)
    readme_file.close()
    exit()
