from allensdk.api.queries.biophysical_perisomatic_api import \
    BiophysicalPerisomaticApi
    
    
neuronal_model_ids = [472451419]


for neuronal_model_id in neuronal_model_ids:
    print("---- Downloading cell model: %s..."%neuronal_model_id)
    bp = BiophysicalPerisomaticApi('http://api.brain-map.org')
    bp.cache_stimulus = True # change to False to not download the large stimulus NWB file
    bp.cache_data(neuronal_model_id, working_directory='%i'%neuronal_model_id)


