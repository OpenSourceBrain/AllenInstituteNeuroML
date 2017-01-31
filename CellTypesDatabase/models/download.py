from allensdk.api.queries.biophysical_api import BiophysicalApi

#from allensdk.api.queries.cell_types_api import CellTypesApi

import sys
import os
import json

import tables

import pprint
pp = pprint.PrettyPrinter(indent=4)
    
def download():
    neuronal_model_ids = ['478047737', '472430904', '479234506', '478513451', '472352327', '478043748', '480633088', '478513443', '489931963', '478513224', 
                          '478047816', '480632594', '472440759', '485694403', '478513459', '471081668', '477840124', '479234530', '473835796', '329322394', 
                          '486557284', '479234670', '478513445', '472306616', '486509010', '478045347', '486509232', '480051220', '485611914', '480631402', 
                          '472451419', '483108201', '496930338', '482525264', '479427516', '488461970', '477876583', '479427369', '472306544', '478810017', 
                          '482657381', '478513187', '486511108', '479694721', '476630478', '486052412', '482655070', '472306460', '472442377', '478513396', 
                          '482525598', '476637699', '487245869', '485510685', '478513398', '477494382', '482657528', '478513461', '485507735', '478513411', 
                          '480629276', '473863510', '485591806', '488462820', '472447460', '480633809', '476637723', '478047588', '482524837', '477839613', 
                          '478809991', '486556597', '480624051', '473465456', '472300877', '476679102', '480630211', '480633479', '480631048', '479427443', 
                          '478045081', '477313251', '483156585', '329321704', '472299363', '480613522', '482934212', '485591776', '472434498', '472304676', 
                          '488462783', '489932435', '473863578', '486052435', '486508758', '486556811', '473834758', '477880244', '478047618', '485602029', 
                          '478513407', '485513184', '472421285', '477510985', '480631286', '491517388', '483066358', '479234441', '488763268', '473872986', 
                          '488462965', '472455509', '489932597', '480624251', '480056382', '477876559', '478809612', '473863035', '480632564', '473862421', 
                          '486556714', '485909152', '486508647', '473871773', '471086533', '482529696', '478045202', '489931686', '473465774', '471085845', 
                          '480624414', '480631187', '480624126', '485476031', '480630857', '473862496', '471087975', '485909125', '472912177', '478513437', 
                          '477838913', '478045226', '486558444', '478048947', '486909496', '477878284', '476630516', '484628276', '479694359', '485513255', 
                          '484620556', '479694384', '483106906', '489932183', '485510712', '477510918', '472363762', '473862845', '486144663', '479695152', 
                          '483109057', '478513415', '482583564', '488759006', '472912107', '485904766', '480630395', '480361288', '485720616', '477878554', 
                          '476637796', '479694856', '478049069', '476637747', '472450023', '478513441', '472299294']

    neuronal_model_ids = [472450023, 483108201, 486556811]
    
    print("---- Downloading %i cell models..."%len(neuronal_model_ids))

    for neuronal_model_id in neuronal_model_ids:
        print("---- Downloading cell model: %s..."%neuronal_model_id)
        try:

            bp = BiophysicalApi('http://api.brain-map.org')
            bp.cache_stimulus = False # change to False to not download the large stimulus NWB file
            working_directory='%i'%neuronal_model_id
            bp.cache_data(neuronal_model_id, working_directory=working_directory)
            print("---- Saved model into %s, included NWB file: %s"%(working_directory,bp.cache_stimulus))
            
            with open(working_directory+'/manifest.json', "r") as json_file:
                manifest_info = json.load(json_file)
                
            metadata={}
            exp_id = int(manifest_info["biophys"][0]["model_file"][1][:9])
            metadata['exp_id'] = exp_id
            
            metadata['URL'] = 'http://celltypes.brain-map.org/mouse/experiment/electrophysiology/%s'%exp_id
            
            for m in manifest_info['manifest']:
                if m['key']=="output_path":
                    nwb_file = working_directory+'/'+m['spec']
                    
            if os.path.isfile(nwb_file):
                print("---- Extracting metadate from NWB file: %s"%(nwb_file))
                h5file=tables.open_file(nwb_file,mode='r')
                metadata['aibs_dendrite_type'] = str(h5file.root.general.aibs_dendrite_type.read())
                metadata['aibs_cre_line'] = str(h5file.root.general.aibs_cre_line.read())
                metadata['aibs_specimen_id'] = str(h5file.root.general.aibs_specimen_id.read())
                metadata['aibs_specimen_name'] = str(h5file.root.general.aibs_specimen_name.read())
                metadata['intracellular_ephys:Electrode 1:location'] = str(h5file.root.general.intracellular_ephys._v_children['Electrode 1'].location.read())
                metadata['session_id'] = str(h5file.root.general.session_id.read())
                metadata['subject:age'] = str(h5file.root.general.subject.age.read())
                metadata['subject:description'] = str(h5file.root.general.subject.description.read())
                metadata['subject:genotype'] = str(h5file.root.general.subject.genotype.read())
                metadata['subject:sex'] = str(h5file.root.general.subject.sex.read())
                metadata['subject:species'] = str(h5file.root.general.subject.species.read())
            else:
                print("---- Can't find NWB file: %s!"%(nwb_file))
                
            print('    Metadata:')
            pp.pprint(metadata)
            with open(working_directory+'/metadata.json', 'w') as f:
                json.dump(metadata, f, indent=4)
            
            
                
        except IndexError:
            print("Problem!")



if __name__ == '__main__':
    
    
    test = '-test' in sys.argv
    
    if test:
        '''
        dataset_ids = []
        ct = CellTypesApi()
        
        all_cells = ct.list_cells(require_morphology=True, require_reconstruction=True, reporter_status=None)
        
        count = 0
        for cell in all_cells:
            id = cell['id']
            print("===============================\nCell %i/%i (%s):"%(count, len(all_cells), id))
            dataset_ids.append(id)
            pp.pprint(cell)
            count+=1
            

        print("Found %i datasets: %s"%(len(dataset_ids),dataset_ids))
        '''
        all_biophys_models = []

        
        count = 0
        
        dataset_ids = [471141261,464198958,325941643,479704527]
        
        for dataset_id in dataset_ids:
        
            url = 'http://celltypes.brain-map.org/api/v2/data/Specimen/query.xml?criteria=model::Specimen,rma::criteria,%5Bid$eq' + \
                  str(dataset_id) + \
                  '%5D,specimen_types%5Bid$eq305008011%5D,rma::include,donor(transgenic_lines%5Btransgenic_line_type_code$eq%27D%27%5D),structure,cell_soma_locations,ephys_features,ephys_sweeps,ephys_result(well_known_files),neuronal_models(neuronal_model_template,neuronal_model_runs(well_known_files%5Bwell_known_file_type_id$eq481007198%5D))'

            import urllib2
            xml = urllib2.urlopen(url).read()

            #print xml

            import xml.etree.ElementTree as ET

            root = ET.fromstring(xml)

            print("\n\n Got XML: %s for dataset %s (%i/%i)"%(root.tag, dataset_id,count,len(dataset_ids)))
            for model in root.findall('./specimens/specimen/neuronal-models/neuronal-model'):
                for child in model:
                    print child.tag, child.attrib, child.text
                id = model.find('./id').text
                name = model.find('./name').text
                print("===========\n  Model: %s, %s"%(id,name))
                if 'Biophysical - perisomatic' in name:
                    print("Has biophysical/perisomatic model!")
                    all_biophys_models.append(id)
            count+=1
                
        print("Found %i biophysical models: %s"%(len(all_biophys_models),all_biophys_models))
        
    else:
                    
        download()
