
import os
import os.path
import json
import sys

import neuroml
from pyneuroml import pynml

sys.path.append("../data")
import data_helper as DH
sys.path.append("../data/bulk_analysis")
import bulk_data_helper as BDH


def generate_network_for_sweeps(cell_type, dataset_id, cell_file_name, cell_id, target_dir, data_dir="../../data"):

    target_sweep_numbers = BDH.DATASET_TARGET_SWEEPS[dataset_id]

    net_id = "network_%s_%s"%(dataset_id, cell_type)
    net = neuroml.Network(id=net_id, type="networkWithTemperature", temperature=DH.SIMULATION_TEMPERATURE)


    net_doc = neuroml.NeuroMLDocument(id=net.id)
    net_doc.networks.append(net)

    net_doc.includes.append(neuroml.IncludeType(cell_file_name))
    if type=='AllenHH':
        net_doc.includes.append(neuroml.IncludeType("CaDynamics.nml"))


    number_cells = len(target_sweep_numbers)
    pop = neuroml.Population(id="Pop0",
                        component=cell_id,
                        size=number_cells,
                        type="populationList")
                        
    net.populations.append(pop)
    for i in range(number_cells):
        location = neuroml.Location(x=100*i,y=0,z=0)
        pop.instances.append(neuroml.Instance(id=i,location=location))

    print target_sweep_numbers
    f = "%s/%s_analysis.json"%(data_dir,dataset_id)
    with open(f, "r") as json_file:
        data = json.load(json_file) 

    id = data['data_set_id']
    sweeps = data['sweeps']

    print("Looking at data analysis in %s (dataset: %s)"%(f,id))

    index = 0
    for s in target_sweep_numbers:
        current = float(sweeps['%i'%s]["sweep_metadata"]["aibs_stimulus_amplitude_pa"])
        print("Sweep %s (%s pA)"%(s, current))

        stim_amp = "%s pA"%current
        input_id = ("input_%i"%s)
        pg = neuroml.PulseGenerator(id=input_id,
                                    delay="270ms",
                                    duration="1000ms",
                                    amplitude=stim_amp)
        net_doc.pulse_generators.append(pg)

        input_list = neuroml.InputList(id=input_id,
                                 component=pg.id,
                                 populations=pop.id)
        input = neuroml.Input(id='0', 
                              target="../%s/%i/%s"%(pop.id, index, cell_id), 
                              destination="synapses")
        index+=1
        input_list.input.append(input)
        net.input_lists.append(input_list)

    net_file_name = '%s/%s.net.nml'%(target_dir,net_id)
    
    print("Saving generated network to: %s"%net_file_name)
    pynml.write_neuroml2_file(net_doc, net_file_name)
    
    return net_file_name

if __name__ == '__main__':
    
    cell_id = "RS"
    #cell_id = "L23_Retuned"

    cell_types = ['Izh', 'HH']
    cell_types = ['HH']
    cell_types = ['Izh']
    cell_types = ['AllenHH']
    cell_types = ['HH2']
    #cell_types = ['L23_Retuned']
    loc = 'prototypes/SmithEtAl2013'
    loc = 'prototypes/AllenHH'
    loc = 'prototypes/HH2'

    for cell_type in cell_types:

        for dataset_id in DH.CURRENT_DATASETS:
            
            generate_network_for_sweeps(cell_type, dataset_id, '%s.cell.nml'%cell_type, cell_id, loc, '../data')