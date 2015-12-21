
import sys
import os
import neuroml
from pyneuroml import pynml

import shutil

from pyneuroml.analysis import generate_current_vs_frequency_curve
from pyneuroml.lems import generate_lems_file_for_neuroml

from generate_nets import generate_network_for_sweeps


def analyse_cell(dataset_id, type, nogui = False):
    
    
    reference = '%s_%s'%(type,dataset_id)
    cell_file = '%s.cell.nml'%(reference)
    
    images = 'summary/%s_%s.png'
    
    generate_current_vs_frequency_curve(cell_file, 
                                        reference, 
                                        simulator = 'jNeuroML_NEURON',
                                        start_amp_nA =         -0.1, 
                                        end_amp_nA =           0.4, 
                                        step_nA =              0.01, 
                                        analysis_duration =    1000, 
                                        analysis_delay =       50,
                                        plot_voltage_traces =  False,
                                        plot_if =              not nogui,
                                        plot_iv =              not nogui, 
                                        xlim_if =              [-200, 400],
                                        ylim_if =              [-10, 120],
                                        xlim_iv =              [-200, 400],
                                        ylim_iv =              [-120, -40],
                                        save_if_figure_to=images%(reference, 'if'), 
                                        save_iv_figure_to=images%(reference, 'iv'),
                                        show_plot_already = False)
               
    temp_dir = 'temp/'
    
    shutil.copy(cell_file, temp_dir)
    
    net_file = generate_network_for_sweeps(type, dataset_id, '%s.cell.nml'%(reference), reference, temp_dir)
    
    lems_file_name = 'LEMS_Test_%s_%s.xml'%(type,dataset_id)
    
    generate_lems_file_for_neuroml('Test_%s_%s'%(dataset_id,type),
                                   net_file,
                                   'network_%s_%s'%(dataset_id,type), 
                                   1500, 
                                   0.01, 
                                   lems_file_name,
                                   temp_dir,
                                   gen_plots_for_all_v=False,
                                   copy_neuroml = False)
    
    simulator = "jNeuroML_NEURON"
    
    if simulator == "jNeuroML":
        results = pynml.run_lems_with_jneuroml(temp_dir+lems_file_name, 
                                                nogui=True, 
                                                load_saved_data=True, 
                                                plot=False,
                                                show_plot_already=False)
    elif simulator == "jNeuroML_NEURON":
        results = pynml.run_lems_with_jneuroml_neuron(temp_dir+lems_file_name, 
                                                nogui=True, 
                                                load_saved_data=True, 
                                                plot=False,
                                                show_plot_already=False)
                                                
    x = []
    y = []
    
    print results.keys()
    
    tt = [t*1000 for t in results['t']]
    for i in range(len(results)-1):
        x.append(tt)
        y.append([v*1000 for v in results['Pop0/%i/%s_%s/v'%(i,type,dataset_id)]])
        
    pynml.generate_plot(x,
                y, 
                "Cell: %s"%dataset_id, 
                xaxis = "Time (ms)", 
                yaxis = "Membrane potential (mV)",
                show_plot_already=False,
                ylim = [-120, 60],
                save_figure_to = images%(reference, 'traces'))
    

if __name__ == '__main__':

    os.chdir('tuned_cells')
    
    nogui = '-nogui' in sys.argv
    
    sys.path.append("../data")
    import data_helper as DH

    dataset_ids = DH.CURRENT_DATASETS

    for dataset_id in dataset_ids:

        type = 'Izh'

        analyse_cell(dataset_id, type, nogui)


        type = 'HH'

        analyse_cell(dataset_id, type, nogui)
    
    if not nogui:
        import matplotlib.pyplot as plt
        plt.show()
    
    
    

