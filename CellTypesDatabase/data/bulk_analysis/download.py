'''
Downloading numerous datasets from CellTypes Database

Criteria for search:
  - Has images
  - Has reconstruction
  - Has GLIF
  - Has Biophysical - perisomatic
  
  on 13/4/17 this resulted in 117 datasets, see cell_data.csv
  
'''


from allensdk.api.queries.cell_types_api import CellTypesApi
import os


ct = CellTypesApi()


cell_data_file = 'cell_data.csv'

MODEL_IDS = {}
locs = {}

for line in open(cell_data_file):
    line = line.replace('area,','area:')
    entries = line.split(',')
    if not entries[0]=='line_name':
        dataset = int(entries[1])
        loc = entries[6][1:-1]
        print("Found %s in %s"%(dataset, loc))
        if not loc in locs:
            locs[loc]=[]
        locs[loc].append(dataset)
        
        MODEL_IDS[dataset] = '???'
        
print("\nFound %s datasets"%len(MODEL_IDS))
for l in locs:
    print("  %s in %s"%(len(locs[l]),l))
    
for dataset_id in MODEL_IDS.keys():
    
    raw_ephys_file_name = '%d_raw_data.nwb' % dataset_id

    if not os.path.isfile(raw_ephys_file_name):
        print('Downloading data: %s'%raw_ephys_file_name)
        ct.save_ephys_data(dataset_id, raw_ephys_file_name)

        print('Saved: %s'%raw_ephys_file_name)
    else:
        print('File: %s already present...'%raw_ephys_file_name)
