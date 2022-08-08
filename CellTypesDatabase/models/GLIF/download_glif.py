from allensdk.api.queries.glif_api import GlifApi
from allensdk.core.cell_types_cache import CellTypesCache
import allensdk.core.json_utilities as json_utilities
import os

GLIF_MODEL_IDS = [
    566282032,
    566283538,
    566283879,
    566288171,
    486557295,
    566291893,
    566291897,
    566302725,
]

for neuronal_model_id in GLIF_MODEL_IDS:

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
