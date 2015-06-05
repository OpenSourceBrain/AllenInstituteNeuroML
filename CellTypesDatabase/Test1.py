# Based on example from Shreejoy Tripathy

from allensdk.api.queries.cell_types_api import CellTypesApi

import pprint
import subprocess

pp = pprint.PrettyPrinter(indent=4)

ct = CellTypesApi()

# use the SDK API to get a list of single cells and corresponding metadata
cell_metadata_list = ct.list_cells(require_reconstruction=True)

# convert that list of cells' metadata to a python dictionary for easy access
cell_meta_dict = {}
dataset_ids = []

for i in range(len(cell_metadata_list)):
    id = cell_metadata_list[i]['id']
    dataset_ids.append(id)
    cell_meta_dict[id] = cell_metadata_list[i]
    
cells = ['467703703', '323452245']

for dataset_id in dataset_ids:
    if cells == None or str(dataset_id) in cells:
        # print some summary metadata for the cell
        print('\n-----------------------------------------------\nCell name: %s' % cell_meta_dict[dataset_id]['name'])
        print('  Cell ID: %i' % cell_meta_dict[dataset_id]['id'])
        print('  Brain region: %s' % cell_meta_dict[dataset_id]['structure']['name'])
        print('  Dendrite info: ')
        for tag in cell_meta_dict[dataset_id]['specimen_tags']:
            print('    %s'%tag['name'])
            x = cell_meta_dict[dataset_id]['cell_soma_locations'][0]['x']
            y = cell_meta_dict[dataset_id]['cell_soma_locations'][0]['y']
            z = cell_meta_dict[dataset_id]['cell_soma_locations'][0]['z']
        print('  Soma loc: (%s, %s, %s)'%(x,y,z))

        #pp.pprint(cell_meta_dict[dataset_id])

        morphology_file_name = '%d.swc' % dataset_id
        ct.save_reconstruction(dataset_id, morphology_file_name)
        
        # Requires: https://github.com/pgleeson/Cvapp-NeuroMorpho.org
        command = 'java -cp ../../../Cvapp-NeuroMorpho.org/build/ cvapp.main %s -exportnml2'%morphology_file_name
        print("Executing: %s"%command)
        return_string = subprocess.check_output(command, cwd='.', shell=True)
        
    else:
        print('Skipping cell: %s'%(dataset_id))
        
