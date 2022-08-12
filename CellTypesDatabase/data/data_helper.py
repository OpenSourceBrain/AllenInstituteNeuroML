# This is subject to change and may disappear without notice...

DATASET_TARGET_SWEEPS = {}
MODEL_IDS = {}
TEST_SWEEP = {}
TEST_CURRENTS = {}


#################################### Layer 5 ####################################

#        No longer has biophys detailed cell model..?
###       Layer 5, spiny http://celltypes.brain-map.org/mouse/experiment/electrophysiology/471141261
##        DATASET_TARGET_SWEEPS[471141261] = [34,38,42,46,50,54,58] # range(54,58)

#  Layer 5, spiny http://celltypes.brain-map.org/mouse/experiment/electrophysiology/486111903
DATASET_TARGET_SWEEPS[486111903] = [35, 37, 41, 44, 51, 54, 57]
# Perisomatic biophys model: http://celltypes.brain-map.org/neuronal_model/download/486556811
MODEL_IDS[486111903] = 486556811
TEST_SWEEP[486111903] = 51
TEST_CURRENTS[486556811] = 230

DATASET_TARGET_SWEEPS[480169178] = [24, 26, 31, 33, 38, 40, 42]
DATASET_TARGET_SWEEPS[480351780] = [24, 33, 34, 47, 42, 44, 46]
DATASET_TARGET_SWEEPS[480353286] = [32, 35, 40, 42, 46, 49, 51]
DATASET_TARGET_SWEEPS[468120757] = [43, 46, 51, 54, 62, 63, 65]

DATASET_TARGET_SWEEPS[476686112] = [23, 24, 25, 26, 37, 31, 36]
DATASET_TARGET_SWEEPS[477127614] = [22, 25, 27, 38, 30, 32, 35]


#  Layer 5, aspiny http://celltypes.brain-map.org/mouse/experiment/electrophysiology/464198958
DATASET_TARGET_SWEEPS[464198958] = [20, 24, 36, 28, 30, 32, 34]
# Perisomatic biophys model: http://celltypes.brain-map.org/neuronal_model/download/472450023
MODEL_IDS[464198958] = [472450023, 497233223]
TEST_SWEEP[464198958] = 28
TEST_CURRENTS[472450023] = 50

#  Layer 5, spiny https://celltypes.brain-map.org/mouse/experiment/electrophysiology/485574832
DATASET_TARGET_SWEEPS[485574832] = [59, 58]
MODEL_IDS[485574832] = [486052412, 497232312]
# Biophysical all active model: https://celltypes.brain-map.org/neuronal_model/download/497232312
TEST_SWEEP[485574832] = 56
TEST_CURRENTS[497232312] = 270

## No longer has biophys detailed cell model..?
#  Layer 5, spiny http://celltypes.brain-map.org/mouse/experiment/electrophysiology/325941643
###DATASET_TARGET_SWEEPS[325941643] = [34,35,37,39,42,44,48]

#################################### Layer 4 ####################################

#  Layer 4, spiny http://celltypes.brain-map.org/mouse/experiment/electrophysiology/479704527
DATASET_TARGET_SWEEPS[479704527] = [36, 40, 44, 45, 60, 52, 55]
# Perisomatic biophys model: http://celltypes.brain-map.org/neuronal_model/download/483108201
MODEL_IDS[479704527] = 483108201
TEST_SWEEP[479704527] = 55
TEST_CURRENTS[483108201] = 270


#  Layer 4, aspiny http://celltypes.brain-map.org/mouse/experiment/electrophysiology/485058595
DATASET_TARGET_SWEEPS[485058595] = [25, 28, 31, 40, 34, 37, 38]
# Perisomatic biophys model: http://celltypes.brain-map.org/neuronal_model/download/485904766
MODEL_IDS[485058595] = 485904766

# DATASET_TARGET_SWEEPS[464326095] = [14,18,21,24,30,32,34]

CURRENT_DATASETS = DATASET_TARGET_SWEEPS.keys()

DATASET = "data_set_id"
COMMENT = "comment"
PYELECTRO_VERSION = "pyelectro_version"
ALLENSDK_VERSION = "allensdk_version"

SWEEPS = "sweeps"
SWEEP = "sweep_id"
ICLAMP_ANALYSIS = "pyelectro_iclamp_analysis"
METADATA = "sweep_metadata"


SIMULATION_TEMPERATURE = "34 degC"


def get_test_current(model_id):
    if int(model_id) in TEST_CURRENTS:
        return TEST_CURRENTS[int(model_id)]
    else:
        raise Exception(
            "Cannot find test current to apply to NeuroML model for model id: %s (known ones: %s)"
            % (model_id, TEST_CURRENTS.keys())
        )
    # else:
    #    return 270


def get_test_sweep(dataset_id):
    if int(dataset_id) in TEST_SWEEP:
        return TEST_SWEEP[int(dataset_id)]
    else:
        raise Exception(
            "Cannot find test sweep to generate for NEURON model for dataset_id: %s"
            % dataset_id
        )
    # else:
    # return 55
