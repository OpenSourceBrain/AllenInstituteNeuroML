from allensdk.api.queries.biophysical_perisomatic_api import BiophysicalPerisomaticApi
    
neuronal_model_ids = [472300877, 472363762, 472442377, 473561660, 473863035, 473561729, 472421285, 472301074, \
                      473872986, 472306616, 329321704, 472912107, 472352327, 471085845, 472912177, 472304676, \
                      473860269, 472447460, 472427533, 472304539, 473465774, 472430904, 473862845, 472450023, \
                      473862496, 473863578, 473871773, 329322394, 472299363, 472455509, 472349114, 471081668, \
                      472451419, 471087975, 472424854, 473863510, 473871592, 472299294, 473835796, 473871429, \
                      473465456, 472306460, 472440759, 472434498, 472915634, 472306544, 473862421, 471086533, \
                      473834758]
                      
#neuronal_model_ids = [472451419]

print("---- Downloading %i cell models..."%len(neuronal_model_ids))
    
for neuronal_model_id in neuronal_model_ids:
    print("---- Downloading cell model: %s..."%neuronal_model_id)
    try:
        
        bp = BiophysicalPerisomaticApi('http://api.brain-map.org')
        bp.cache_stimulus = False # change to False to not download the large stimulus NWB file
        bp.cache_data(neuronal_model_id, working_directory='%i'%neuronal_model_id)
    except IndexError:
        print("Problem!")


