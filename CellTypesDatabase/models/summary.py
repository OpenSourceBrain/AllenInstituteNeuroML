import matplotlib.pyplot as plt
from pyneuroml import pynml
from pyneuroml.pynml import run_lems_with_jneuroml_neuron
import numpy as np
import os
import sys
import json


import airspeed

sys.path.append('../data')
from data_helper import get_test_sweep
from download import ALL_ACTIVE_MODEL_IDS
from run_one import _get_dataset_id, run


MD_TEMPLATE_FILE = "./template.md"

OUTPUT_DIR = os.getcwd()


def merge_with_template(model, templfile):
    if not os.path.isfile(templfile):
        templfile = os.path.join(os.path.dirname(sys.argv[0]), templfile)
    with open(templfile) as f:
        templ = airspeed.Template(f.read())
    return templ.merge(model)


def make_md_file(cell_dirs=None):
    data = []
    for model in cell_dirs:
        this_data = {}
        with open(f"{model}/metadata.json") as f:
            metadata = json.load(f)
        if int(model) in ALL_ACTIVE_MODEL_IDS:
            this_data["URL"] = f'http://celltypes.brain-map.org/mouse/experiment/electrophysiology/{metadata["AIBS:aibs_specimen_id"]}'
        else:
            this_data["URL"] = metadata["URL"]
        this_data["location"] = metadata[
            "AIBS:intracellular_ephys:Electrode 1:location"
        ]
        this_data["dendrite"] = metadata["AIBS:aibs_dendrite_type"]
        this_data["description"] = metadata["AIBS:aibs_cre_line"]
        this_data["id"] = model
        data.append(this_data)

    info = {"models": data}
    merged = merge_with_template(info, MD_TEMPLATE_FILE)
    new_md_file = os.path.join(OUTPUT_DIR, "README.md")
    lf = open(new_md_file, "w")
    lf.write(merged)
    lf.close()


def main():

    cell_dirs = [
        f
        for f in os.listdir(".")
        if (os.path.isdir(f) and os.path.isfile(f + "/manifest.json"))
    ]
    for model in cell_dirs:
        print(f"Generating figs for model {model}...")
        # 3d stucture
        print(f"Generating 3d structure fig for model {model}...")
        NML_FILE = f"NeuroML2/Cell_{model}.cell.nml"
        if not os.path.isfile(f"NeuroML2/Cell_{model}.cell.png"):
            pynml.nml2_to_png(NML_FILE)

        # simulate NEURON mods
        print(f"Generating NEURON simulation fig for model {model}...")
        
        DAT_FILE = f"{model}/sweep_{get_test_sweep(_get_dataset_id(model))}.v.dat"
        if not os.path.isfile(DAT_FILE):
            run(model)

        data, _ = pynml.reload_standard_dat_file(DAT_FILE)
        v = np.array(data[0])
        t = np.array(data["t"])
        plt.figure(figsize=(8, 5))

        plt.plot(t * 1000, v * 1000, label="NEURON mod")
        plt.xlim([750, 2250])
        plt.xlabel("Time (ms)")
        plt.ylabel("Membrane Potential (mV)")
        plt.legend()
        plt.savefig(f"summary/NEURON_{model}.png")

        # simulate LEMS
        print(f"Generating LEMS simulation fig for model {model}...")
        LEMS_DAT_FILE = f"NeuroML2/{model}.Pop_Cell_{model}.v.dat"
        if not os.path.isfile(LEMS_DAT_FILE):
            run_lems_with_jneuroml_neuron(f"NeuroML2/LEMS_{model}.xml")

    
        data, i = pynml.reload_standard_dat_file(LEMS_DAT_FILE)
        v_lems = np.array(data[0])
        t_lems = np.array(data["t"])
        plt.figure(figsize=(8, 5))
        plt.plot(t_lems * 1000, v_lems * 1000, label="LEMS")
        plt.xlim([750, 2250])

        plt.xlabel("Time (ms)")
        plt.ylabel("Membrane Potential (mV)")
        plt.legend()
        plt.savefig(f"summary/LEMS_{model}.png")

        print("Done!")

    make_md_file(cell_dirs)


if __name__ == "__main__":
    main()
