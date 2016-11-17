#Based in part on example code at: http://alleninstitute.github.io/AllenSDK/biophysical_perisomatic_script.html
    
from allensdk.model.biophysical_perisomatic.utils import Utils
from allensdk.model.biophysical_perisomatic.runner import load_description

from pyneuroml.neuron import export_to_neuroml2
from pyneuroml.neuron.nrn_export_utils import clear_neuron
from pyneuroml.lems import generate_lems_file_for_neuroml
from pyneuroml import pynml

import json
import sys

import os
import os.path

import neuroml

sys.path.append('../data')
from data_helper import get_test_current

cell_dirs = []

cell_dirs = [ f for f in os.listdir('.') if (os.path.isdir(f) and os.path.isfile(f+'/manifest.json')) ]

nml2_cell_dir = '../NeuroML2/'


net_ref = "ManyCells"
net_doc = neuroml.NeuroMLDocument(id=net_ref)

net = neuroml.Network(id=net_ref)
net_doc.networks.append(net)

clear_neuron()
    
count = 0

ca_dynamics = {}

for model_id in cell_dirs:
    
    if os.path.isdir(model_id):
        os.chdir(model_id)
    else:
        os.chdir('../'+model_id)
        
    print('\n\n************************************************************\n\n    Parsing %s (cell %i/%i)\n'%(model_id, count, len(cell_dirs)))
    
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
    
    with open('manifest.json', "r") as json_file:
        manifest_info = json.load(json_file)
        
    print("Loaded manifest: %s (fit: %s)"%(manifest_info['biophys'][0]["model_type"], manifest_info['biophys'][0]["model_file"][1]))

    print("Cell loaded from: %s"%morphology_path)
    
    h.finitialize()
    h.psection()
    
    nml_file_name = "%s.net.nml"%model_id
    nml_net_loc = "%s/%s"%(nml2_cell_dir,nml_file_name)
    nml_cell_file0 = "Cell0.cell.nml"
    nml_cell_loc0 = "%s/%s"%(nml2_cell_dir,nml_cell_file0)
    nml_cell_file = "Cell_%s.cell.nml"%model_id
    nml_cell_loc = "%s/%s"%(nml2_cell_dir,nml_cell_file)


    print(' > Exporting to %s'%(nml_net_loc))

    export_to_neuroml2(None, 
                       nml_net_loc, 
                       separateCellFiles=True,
                       includeBiophysicalProperties=False)

    print(' > Exported to: %s and %s'%(nml_net_loc, nml_cell_loc))
    
    
    clear_neuron()

    nml_doc = pynml.read_neuroml2_file(nml_cell_loc0)
        
    cell = nml_doc.cells[0]
    
    cell.id = 'Cell_%s'%model_id
    
    notes = ''
    notes+="\n\nExport of a cell model (%s) obtained from the Allen Institute Cell Types Database into NeuroML2"%model_id + \
            "\n\n******************************************************\n*  This export to NeuroML2 has not yet been fully validated!!"+ \
            "\n*  Use with caution!!\n******************************************************\n\n"


    cell.notes = notes
        
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
    
    with open(manifest_info['biophys'][0]["model_file"][1], "r") as json_file:
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
            ion = '??'
            if chan_name == 'pas':
                erev = '%s mV'%cell_info['passive'][0]['e_pas']
                ion = 'non_specific'
            elif chan['mechanism'].startswith('Na'):
                erev = '%s mV'%cell_info['conditions'][0]['erev'][0]['ena']
                ion = 'na'
            elif chan['mechanism'].startswith('K') or chan['mechanism'] == 'SK' or chan['mechanism'].startswith('Im'):
                erev = '%s mV'%cell_info['conditions'][0]['erev'][0]['ek']
                ion = 'k'
            elif chan['mechanism'] == 'Ih':
                erev = '-45 mV'
                ion = 'hcn'
            elif chan['mechanism'].startswith('Ca'):
                ion = 'ca'
                
            if chan['mechanism'] == 'Ca_HVA' or chan['mechanism'] == 'Ca_LVA':
                
                cdn = neuroml.ChannelDensityNernst(id='%s_%s'%(chan_name, chan['section']),
                                            ion_channel=chan_name,
                                            segment_groups=chan['section'],
                                            cond_density='%s S_per_cm2'%float(chan['value']),
                                            ion = ion)
                membrane_properties.channel_density_nernsts.append(cdn)
            else:
                cd = neuroml.ChannelDensity(id='%s_%s'%(chan_name, chan['section']),
                                            ion_channel=chan_name,
                                            segment_groups=chan['section'],
                                            cond_density='%s S_per_cm2'%float(chan['value']),
                                            erev=erev,
                                            ion = ion)
                membrane_properties.channel_densities.append(cd)
        else:
            if not ca_dynamics.has_key(model_id):
                ca_dynamics[model_id] = {}
            ca_dynamics[model_id][str(chan['name'])] = chan['value']
                
   
    inc_chans =[]
    for cd in membrane_properties.channel_densities:
        if not cd.ion_channel in inc_chans:
            nml_doc.includes.append(
                    neuroml.IncludeType(href="%s.channel.nml" % cd.ion_channel))
            inc_chans.append(cd.ion_channel)
    for cdn in membrane_properties.channel_density_nernsts:
        if not cdn.ion_channel in inc_chans:
            nml_doc.includes.append(
                    neuroml.IncludeType(href="%s.channel.nml" % cdn.ion_channel))
            inc_chans.append(cdn.ion_channel)

    resistivities = []
    resistivities.append(neuroml.Resistivity(value="%s ohm_cm"%cell_info['passive'][0]['ra'], segment_groups='all'))
    
    species = []
    species.append(neuroml.Species(id='ca', \
                        ion='ca',  \
                        initial_concentration='0.0001 mM', \
                        initial_ext_concentration='2 mM', \
                        concentration_model="CaDynamics_%s"%model_id, \
                        segment_groups="soma"))
                        
    
                        
    nml_doc.includes.append(
                    neuroml.IncludeType(href="%s.nml" % 'CaDynamics_all'))
                       
    xml = '''<?xml version="1.0" encoding="ISO-8859-1"?>
<neuroml xmlns="http://www.neuroml.org/schema/neuroml2" 
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
        xsi:schemaLocation="http://www.neuroml.org/schema/neuroml2 https://raw.githubusercontent.com/NeuroML/NeuroML2/development/Schemas/NeuroML2/NeuroML_v2beta3.xsd" 
        id="CaDynamics_all">
    
    <notes>A set of concentration models for various cells exported to NeuroML, with specific values for gamma and delay</notes>
    
    <!-- This file contains the definition of the ComponentType concentrationModelHayEtAl -->
    <include href="CaDynamics.nml"/>
    
'''     
    # @type ca_dynamics dict
    for key, values in ca_dynamics.iteritems():

        xml += '    <concentrationModel id="CaDynamics_%s" type="concentrationModelHayEtAl" minCai="1e-4 mM" decay="%s ms" depth="0.1 um" gamma="%s" ion="ca"/>\n\n'%(key,values["decay_CaDynamics"],values["gamma_CaDynamics"])
         
    xml += '''
</neuroml>'''
         
    ca_file = open(nml2_cell_dir+'CaDynamics_all.nml','w')
    ca_file.write(xml)
    ca_file.close()
        
         
                        
    intracellular_properties = neuroml.IntracellularProperties(resistivities=resistivities, species=species)

            
    biophysical_properties = neuroml.BiophysicalProperties(id="biophys",
                                          intracellular_properties=intracellular_properties,
                                          membrane_properties=membrane_properties)
                                          
    cell.biophysical_properties = biophysical_properties
    
    
    pynml.write_neuroml2_file(nml_doc, nml_cell_loc)
    
    
    pynml.nml2_to_svg(nml_cell_loc)
    
    
    

    new_nml_file_name = "Network_%s.net.nml"%model_id
    
    new_net_loc = "%s/%s"%(nml2_cell_dir, new_nml_file_name)
    new_net_doc = pynml.read_neuroml2_file(nml_net_loc)
    new_net = new_net_doc.networks[0]
    new_net_doc.notes = notes
    
    new_net_doc.includes[0].href = nml_cell_file
    
    pop_id = 'Pop_Cell_%s'%model_id
    pop_comp = 'Cell_%s'%model_id
    new_net.populations[0].id = pop_id
    new_net.populations[0].component = pop_comp

    stim_ref = "stim"
    stim = neuroml.PulseGenerator(id=stim_ref, 
                                  delay="1020ms", 
                                  duration="1000ms", 
                                  amplitude="%spA"%get_test_current(model_id))
    new_net_doc.pulse_generators.append(stim)
    
    input_list = neuroml.InputList(id="%s_input"%stim_ref,
                         component=stim_ref,
                         populations=pop_id)

    input = neuroml.Input(id=0, 
                          target="../%s/0/%s"%(pop_id, pop_comp), 
                          destination="synapses")  

    input_list.input.append(input)
    new_net.input_lists.append(input_list)
    
    pynml.write_neuroml2_file(new_net_doc, new_net_loc)

    generate_lems_file_for_neuroml(model_id,
                                   new_net_loc,
                                   "network",
                                   2500,
                                   0.005, # used in Allen Neuron runs
                                   "LEMS_%s.xml"%model_id,
                                   nml2_cell_dir,
                                   copy_neuroml = False,
                                   seed=1234)
    
    
    net_doc.includes.append(neuroml.IncludeType(nml_cell_file))

    pop = neuroml.Population(id="Pop_%s"%model_id, component=cell.id, type="populationList")

    net.populations.append(pop)

    inst = neuroml.Instance(id="0")
    pop.instances.append(inst)

    width = 7
    X = count%width
    Z = (count -X) / width
    inst.location = neuroml.Location(x=300*X, y=0, z=300*Z)

    count+=1
    

net_file = '%s/%s.net.nml'%(nml2_cell_dir,net_ref)
neuroml.writers.NeuroMLWriter.write(net_doc, net_file)

print("Written network with %i cells in network to: %s"%(count,net_file))

pynml.nml2_to_svg(net_file)