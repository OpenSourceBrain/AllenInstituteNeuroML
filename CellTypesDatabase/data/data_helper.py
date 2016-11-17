# This is subject to change and may disappear without notice...

DATASET_TARGET_SWEEPS = {}
MODEL_IDS = {}
TEST_SWEEP = {}
TEST_CURRENTS = {}

#  Layer 5, spiny http://celltypes.brain-map.org/mouse/experiment/electrophysiology/471141261
DATASET_TARGET_SWEEPS[471141261] = [34,38,42,46,50,54,58] # range(54,58)

#  Layer 5, spiny http://celltypes.brain-map.org/mouse/experiment/electrophysiology/486111903
DATASET_TARGET_SWEEPS[486111903] = [35,37,41,44,51,54,57]
# Detailed model: http://celltypes.brain-map.org/neuronal_model/download/486556811
MODEL_IDS[486111903] = 486556811
TEST_SWEEP[486111903] = 54
TEST_CURRENTS[486556811] = 290

#  Layer 5, aspiny http://celltypes.brain-map.org/mouse/experiment/electrophysiology/464198958
DATASET_TARGET_SWEEPS[464198958] = [20,24,36,28,30,32,34]

#  Layer 5, spiny http://celltypes.brain-map.org/mouse/experiment/electrophysiology/325941643
DATASET_TARGET_SWEEPS[325941643] = [34,35,37,39,42,44,48] 

#  Layer 4, spiny http://celltypes.brain-map.org/mouse/experiment/electrophysiology/479704527
DATASET_TARGET_SWEEPS[479704527] = [36,40,44,45,60,52,55] 

#DATASET_TARGET_SWEEPS[464326095] = [14,18,21,24,30,32,34]

CURRENT_DATASETS = DATASET_TARGET_SWEEPS.keys()

DATASET = 'data_set_id'
COMMENT = 'comment'
PYELECTRO_VERSION = 'pyelectro_version'
ALLENSDK_VERSION = 'allensdk_version'

SWEEPS = 'sweeps' 
SWEEP = 'sweep_id' 
ICLAMP_ANALYSIS = 'pyelectro_iclamp_analysis' 
METADATA = 'sweep_metadata' 


SIMULATION_TEMPERATURE = '34 degC'

def get_test_current(model_id):
    if TEST_CURRENTS.has_key(model_id):
        return TEST_CURRENTS[model_id]
    else:
        return 270
    
def get_test_sweep(model_id):
    if TEST_SWEEP.has_key(model_id):
        return TEST_SWEEP[model_id]
    else:
        return 55