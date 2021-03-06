from allensdk.api.queries.glif_api import GlifApi
import random
import pprint
import os

pp = pprint.PrettyPrinter(indent=4)

api = GlifApi()

models = api.list_neuronal_models()

max = 5

def write_to_file(directory, file_name, jstring):
    
    file_path = '%s/%s'%(directory, file_name)
    print("Writing to: %s"%file_path)
    if not os.path.isdir(directory):
        os.mkdir(directory)
    
    f = open(file_path,'w')
    #info = str(jstring)
    pretty = pp.pformat(jstring)
    pretty = pretty.replace('\'', '"')
    pretty = pretty.replace('u"', '"')
    pretty = pretty.replace('None', 'null')
    pretty = pretty.replace('False', 'false')
    pretty = pretty.replace('True', 'true')
    f.write(pretty)
    f.close()

random.seed(123)

models_to_use = random.sample(models,max)
extras = [472308324]

for model in models:
    if model['id'] in extras:
        models_to_use.append(model)

for model in models_to_use:

    model_id = str(model['id'])

    print("\n=====================================")
    print("Model %s: %s"%(model_id,model['name']))
    
    info = api.get_neuronal_model(model['id'])

    write_to_file(model_id, 'ephys_sweeps.json',info['ephys_sweeps'])
    write_to_file(model_id, 'model_metadata.json',info['neuronal_model'])

    api.get_neuron_config(output_file_name='%s/neuron_config.json'%model_id)

print("Done with %i models"%len(models))