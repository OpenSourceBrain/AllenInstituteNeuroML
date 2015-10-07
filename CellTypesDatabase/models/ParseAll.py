#Based in part on example code at: http://alleninstitute.github.io/AllenSDK/biophysical_perisomatic_script.html
    
from allensdk.model.biophysical_perisomatic.utils import Utils
from allensdk.model.biophysical_perisomatic.runner import load_description

from pyneuroml.neuron import export_to_neuroml2
from pyneuroml.neuron.nrn_export_utils import clear_neuron

from pyneuroml import pynml

import os
import os.path

cell_dirs = []

cell_dirs = [ f for f in os.listdir('.') if (os.path.isdir(f) and os.path.isfile(f+'/manifest.json')) ]

nml2_cell_dir = '../NeuroML2/'

count = 0
for cell_dir in cell_dirs:
    
    if os.path.isdir(cell_dir):
        os.chdir(cell_dir)
    else:
        os.chdir('../'+cell_dir)
        
    print('\n\n************************************************************\n\n    Parsing %s (cell %i/%i)\n'%(cell_dir, count, len(cell_dirs)))
    
    description = load_description('manifest.json')

    # configure NEURON
    utils = Utils(description)
    h = utils.h

    print("NEURON configured")

    # configure model
    manifest = description.manifest
    morphology_path = description.manifest.get_path('MORPHOLOGY')
    utils.generate_morphology(morphology_path.encode('ascii', 'ignore'))
    utils.load_cell_parameters()

    print("Cell loaded from: %s"%morphology_path)
    
    h.finitialize()
    h.psection()
    
    nml_file_name = "%s.net.nml"%cell_dir
    nml_net_loc = "%s/%s"%(nml2_cell_dir,nml_file_name)
    nml_cell_file = "Cell0.cell.nml"
    nml_cell_loc = "%s/%s"%(nml2_cell_dir,nml_cell_file)


    print(' > Exporting to %s'%(nml_net_loc))

    export_to_neuroml2(None, 
                       nml_net_loc, 
                       separateCellFiles=True,
                       includeBiophysicalProperties=False)

    print(' > Exported to: %s and %s'%(nml_net_loc, nml_cell_loc))

    nml_doc = pynml.read_neuroml2_file(nml_cell_loc)
        
    cell = nml_doc.cells[0]
        
    print(' > Altering groups')
    
    for sg in cell.morphology.segment_groups:
        print("Found group: %s"%sg.id)
    
    pynml.write_neuroml2_file(nml_doc, nml_cell_loc)