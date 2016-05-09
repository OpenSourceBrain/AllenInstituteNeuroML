import sys
import os
import json

def generate_lems(glif_dir, curr_pA, show_plot=True):

    os.chdir(glif_dir)
    
    with open('model_metadata.json', "r") as json_file:
        model_metadata = json.load(json_file)

    with open('neuron_config.json', "r") as json_file:
        neuron_config = json.load(json_file)

    with open('ephys_sweeps.json', "r") as json_file:
        ephys_sweeps = json.load(json_file)

    template_cell = '''<Lems>

      <%s %s/>

    </Lems>
    '''

    type = 'glifCell'
    cell_id = 'GLIF_%s'%glif_dir

    attributes = ""

    attributes +=' id="%s"'%cell_id
    attributes +='\n        C="%s F"'%neuron_config["C"]
    attributes +='\n        leakReversal="%s V"'%neuron_config["El"]
    attributes +='\n        reset="%s V"'%neuron_config["El"]
    attributes +='\n        thresh="%s V"'%( float(neuron_config["th_inf"]) * float(neuron_config["coeffs"]["th_inf"]))
    attributes +='\n        leakConductance="%s S"'%(1/float(neuron_config["R_input"]))

    file_contents = template_cell%(type, attributes)

    print(file_contents)

    cell_file_name = '%s.xml'%(cell_id)
    cell_file = open(cell_file_name,'w')
    cell_file.write(file_contents)
    cell_file.close()


    import opencortex.build as oc

    nml_doc, network = oc.generate_network("Test_%s"%glif_dir)

    pop = oc.add_single_cell_population(network,
                                         'pop_%s'%glif_dir,
                                         cell_id)


    pg = oc.add_pulse_generator(nml_doc,
                           id="pg0",
                           delay="100ms",
                           duration="1000ms",
                           amplitude="%s pA"%curr_pA)


    oc.add_inputs_to_population(network,
                                "Stim0",
                                pop,
                                pg.id,
                                all_cells=True)



    nml_file_name = '%s.net.nml'%network.id
    oc.save_network(nml_doc, nml_file_name, validate=True)

    oc.generate_lems_simulation(nml_doc, 
                                network, 
                                nml_file_name, 
                                include_extra_files = [cell_file_name,'../GLIFs.xml'],
                                duration =      1200, 
                                dt =            0.01)

    os.chdir('..')
                            
if __name__ == '__main__':
    
    glif_dir = sys.argv[1]
    curr_pA = float(sys.argv[2])
    show_plot = '-nogui' not in sys.argv
    generate_lems(glif_dir, curr_pA, show_plot=show_plot)