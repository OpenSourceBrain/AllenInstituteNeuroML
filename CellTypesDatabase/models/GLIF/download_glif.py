usage = """

This script is used to download GLIF cell model files using the Allen SDK 

To download all listed models used in this repo run:

    python download_glif.py -all

To download a test model run:
    python download_glif.py -test

"""

from allensdk.api.queries.glif_api import GlifApi
from allensdk.core.cell_types_cache import CellTypesCache
import allensdk.core.json_utilities as json_utilities
import os
import sys

GLIF_MODEL_IDS = [
    566282032,
    566283540,
    566283879,
    566288171,
    486557295,
    566291893,
    566291897,
    566302725,
]

GLIF_MODEL_IDS_FOR_NETWORK_BUILD = [
    566320096,
    489931668,
    486558431,
    566382734,
    486052403,
    485904755,
    566303332,
    566357260,
]


def download_glif_model(neuronal_model_id):

    print("Downloading model: %s" % neuronal_model_id)
    if not os.path.isdir(str(neuronal_model_id)):
        os.mkdir(str(neuronal_model_id))

    # download model metadata
    glif_api = GlifApi()
    nm = glif_api.get_neuronal_models_by_id([neuronal_model_id])[0]
    json_utilities.write(f"{neuronal_model_id}/model_metadata.json", nm)

    # download the model configuration file
    nc = glif_api.get_neuron_configs([neuronal_model_id])[neuronal_model_id]
    neuron_config = glif_api.get_neuron_configs([neuronal_model_id])
    json_utilities.write(f"{neuronal_model_id}/neuron_config.json", neuron_config)

    # download information about the cell
    ctc = CellTypesCache()
    ctc.get_ephys_data(nm["specimen_id"], file_name=f"{neuronal_model_id}/stimulus.nwb")
    ctc.get_ephys_sweeps(
        nm["specimen_id"], file_name=f"{neuronal_model_id}/ephys_sweeps.json"
    )

    print("Done!")


if __name__ == "__main__":

    if "-all" in sys.argv:
        for model in GLIF_MODEL_IDS + GLIF_MODEL_IDS_FOR_NETWORK_BUILD:
            download_glif_model(model)

    elif "-test" in sys.argv:
        download_glif_model(566291893)

    else:
        print(usage)
