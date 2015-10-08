#Based in part on example code at: http://alleninstitute.github.io/AllenSDK/biophysical_perisomatic_script.html
    
from allensdk.model.biophysical_perisomatic.utils import Utils
from allensdk.model.biophysical_perisomatic.runner import load_description

from pyneuroml.neuron import export_to_neuroml2
from pyneuroml.neuron.nrn_export_utils import clear_neuron

import json

from pyneuroml import pynml

import os
import os.path

import neuroml

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
    nml_cell_file0 = "Cell0.cell.nml"
    nml_cell_loc0 = "%s/%s"%(nml2_cell_dir,nml_cell_file0)
    nml_cell_file = "%s.cell.nml"%cell_dir
    nml_cell_loc = "%s/%s"%(nml2_cell_dir,nml_cell_file)


    print(' > Exporting to %s'%(nml_net_loc))

    export_to_neuroml2(None, 
                       nml_net_loc, 
                       separateCellFiles=True,
                       includeBiophysicalProperties=False)

    print(' > Exported to: %s and %s'%(nml_net_loc, nml_cell_loc))

    nml_doc = pynml.read_neuroml2_file(nml_cell_loc0)
        
    cell = nml_doc.cells[0]
        
    print(' > Altering groups')
    
    for sg in cell.morphology.segment_groups:
        print("Found group: %s"%sg.id)
        if (sg.id.startswith('ModelViewParm')) and len(sg.members)==0:
            replace = {}
            replace['soma_'] = 'soma'
            replace['axon_'] = 'axon'
            replace['apic_'] = 'apic'
            replace['dend_'] = 'dend'
            for prefix in replace.keys():
                all_match = True
                for inc in sg.includes:
                    #print inc
                    all_match = all_match and inc.segment_groups.startswith(prefix)
                if all_match:
                    print("Replacing group named %s with %s"%(sg.id,replace[prefix]))
                    sg.id = replace[prefix]
    
    with open('%s_fit.json'%cell_dir, "r") as json_file:
        cell_info = json.load(json_file)
        
    
    membrane_properties = neuroml.MembraneProperties()
    
    for sc in cell_info['passive'][0]['cm']:
        membrane_properties.specific_capacitances.append(neuroml.SpecificCapacitance(value='%s uF_per_cm2'%sc['cm'],
                                            segment_groups=sc['section']))
                                            
    for chan in cell_info['genome']:
        chan_name = chan['mechanism']
        if  chan['name'] == 'g_pas':
            chan_name = 'pas'
        if chan['mechanism'] != 'CaDynamics':
            erev = '??'
            if chan_name == 'pas':
                erev = '%s mV'%cell_info['passive'][0]['e_pas']
            elif chan['mechanism'].startswith('Na'):
                erev = '%s mV'%cell_info['conditions'][0]['erev'][0]['ena']
            elif chan['mechanism'].startswith('K') or chan['mechanism'].startswith('SK'):
                erev = '%s mV'%cell_info['conditions'][0]['erev'][0]['ek']
            elif chan['mechanism'].startswith('I'):
                erev = '-45 mV'
                
            
            if chan['mechanism'] == 'Ca_HVA' or chan['mechanism'] == 'Ca_LVA':
                
                cdn = neuroml.ChannelDensityNernst(id='%s_%s'%(chan_name, chan['section']),
                                            ion_channel=chan_name,
                                            segment_groups=chan['section'],
                                            cond_density='%s S_per_cm2'%float(chan['value']))
                membrane_properties.channel_density_nernsts.append(cdn)
            else:
                cd = neuroml.ChannelDensity(id='%s_%s'%(chan_name, chan['section']),
                                            ion_channel=chan_name,
                                            segment_groups=chan['section'],
                                            cond_density='%s S_per_cm2'%float(chan['value']),
                                            erev=erev)
                membrane_properties.channel_densities.append(cd)
                                            

    resistivities = []
    resistivities.append(neuroml.Resistivity(value="%s ohm_cm"%cell_info['passive'][0]['ra'], segment_groups='all'))
    
    species = []
    species.append(neuroml.Species(id='ca', \
                        ion='ca',  \
                        initial_concentration='0.0001 mM', \
                        initial_ext_concentration='2 mM', \
                        concentration_model="CaDynamics", \
                        segment_groups="soma"))
                        
    intracellular_properties = neuroml.IntracellularProperties(resistivities=resistivities, species=species)

            
    biophysical_properties = neuroml.BiophysicalProperties(id="biophys",
                                          intracellular_properties=intracellular_properties,
                                          membrane_properties=membrane_properties)
                                          
    cell.biophysical_properties = biophysical_properties
    
    
    pynml.write_neuroml2_file(nml_doc, nml_cell_loc)