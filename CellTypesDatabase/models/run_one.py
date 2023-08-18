"""Simulates a specific sweep of a biophysical cell model. """
# Based on example code at: https://allensdk.readthedocs.io/en/latest/biophysical_models.html

from allensdk.model.biophysical.utils import Utils, AllActiveUtils
from allensdk.model.biophysical.runner import load_description

import sys
import json
import os

sys.path.append("../data")
from data_helper import get_test_sweep
from download import ALL_ACTIVE_MODEL_IDS


def _get_dataset_id(model_id, model_path_prefix=""):
    with open(
        os.path.join(model_path_prefix, model_id, "metadata.json"), "r"
    ) as json_file:
        metadata = json.load(json_file)
    if int(model_id) in ALL_ACTIVE_MODEL_IDS:
        dataset_id = int(metadata["AIBS:aibs_specimen_id"])
    else:
        dataset_id = int(metadata["exp_id"])

    return dataset_id


def run(model_id, model_path_prefix=""):
    if os.path.isdir(os.path.join(model_path_prefix, model_id)):
        dataset_id = _get_dataset_id(model_id, model_path_prefix)
        os.chdir(os.path.join(model_path_prefix, model_id))
    else:
        print("Model id is invalid!")
        sys.exit()

    # check if .nwb file is present in the current directory
    print("Checking if .nwb file is present in the current directory...")
    if not next(file for file in os.listdir() if file.endswith('.nwb')):
        print(f"You need the .nwb file to run this model! Can be downloaded using CellTypesDatabase/models/download.py")
        sys.exit()
        
    description = load_description({"manifest_file": "manifest.json"})

    # find cell type
    all_active = (
        True if "all active" in description.data["biophys"][0]["model_type"] else False
    )

    # configure NEURON
    if all_active:
        utils = AllActiveUtils(description, axon_type="stub")
    else:
        utils = Utils(description)
    h = utils.h

    print("NEURON configured")

    # configure model
    morphology_path = description.manifest.get_path("MORPHOLOGY")
    utils.generate_morphology(morphology_path.encode("ascii", "ignore"))
    utils.load_cell_parameters()

    print("Cell loaded from: %s" % morphology_path)

    # configure stimulus and recording
    stimulus_path = description.manifest.get_path("stimulus_path")

    run_params = description.data["runs"][0]

    sweeps = [get_test_sweep(dataset_id)]

    junction_potential = description.data["fitting"][0]["junction_potential"]
    mV = 1.0e-3

    h.load_file("../NEURON/cellCheck.hoc")

    for sweep in sweeps:
        utils.setup_iclamp(stimulus_path, sweep=sweep)
        vec = utils.record_values()

        print("Running sweep: %i for %s ms (dt: %s ms)" % (sweep, h.tstop, h.dt))
        h.finitialize()
        h.psection()
        h("cellInfo()")
        h.run()

        print(
            "Finished running sweep: %i, %i data points saved" % (sweep, len(vec["v"]))
        )
        s_file = open("sweep_%i.v.dat" % (sweep), "w")
        for i in range(len(vec["v"])):
            s_file.write("%s\t%s\n" % (vec["t"][i] / 1000.0, vec["v"][i] / 1000))
        s_file.close()
    os.chdir("..")


if __name__ == "__main__":

    model_ids = []
    if "-test_active" in sys.argv:
        model_ids = ["497232312"]
    elif "-test_perisomatic" in sys.argv:
        model_ids = ["483108201"]
    elif "-test_perisomatic2" in sys.argv:
        model_ids = ["486556811"]
    elif "-test_perisomatic3" in sys.argv:
        model_ids = ["472450023"]
    elif "-all" in sys.argv:
        model_ids = [
            f
            for f in os.listdir(".")
            if (os.path.isdir(f) and os.path.isfile(f + "/manifest.json"))
        ]
    else:
        if len(sys.argv) > 1:
            model_ids = [sys.argv[1]]
        else:
            print("Options:\n")
            print("     python run_one.py -test_active")
            print("     python run_one.py -test_perisomatic")
            print("     python run_one.py -test_perisomatic2")
            print("     python run_one.py <model_id>")
            print("     python run_one.py -all")
            sys.exit()

    print(model_ids)
    for model_id in model_ids:
        print("Running model: %s" % model_id)
        run(model_id)
