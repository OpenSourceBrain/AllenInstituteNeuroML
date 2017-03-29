
import sys
import os
import neuroml
from pyneuroml import pynml

import shutil

from pyneuroml.analysis import generate_current_vs_frequency_curve
from pyneuroml.lems import generate_lems_file_for_neuroml

from generate_nets import generate_network_for_sweeps

sys.path.append("../data")
from data_summary import get_if_iv_for_dataset

def analyse_cell(dataset_id, type, nogui = False):
    
    
    reference = '%s_%s'%(type,dataset_id)
    cell_file = '%s.cell.nml'%(reference)
    
    print("====================================\n\n   Analysing cell: %s, dataset %s\n"%(cell_file,dataset_id))
    
    nml_doc = pynml.read_neuroml2_file(cell_file)
    notes = nml_doc.cells[0].notes if len(nml_doc.cells)>0 else nml_doc.izhikevich2007_cells[0].notes
    meta = eval(notes[notes.index('{'):])
    info = "Fitness: %s (max evals: %s, pop: %s)"%(meta['fitness'],meta['max_evaluations'],meta['population_size'])
    print info
    
    images = 'summary/%s_%s.png'
    
    data, v_sub, curents_sub, v, curents_spike = get_if_iv_for_dataset('../../data/%s_analysis.json'%dataset_id)
    
    traces_ax, if_ax, iv_ax = generate_current_vs_frequency_curve(cell_file, 
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
                                        show_plot_already = False,
                                        return_axes = True)
    
                                
    iv_ax.plot(curents_sub, v_sub,color='#ff2222',marker='o', linestyle='',zorder=1)   
    if_ax.plot(curents_spike, v,color='#ff2222',marker='o', linestyle='',zorder=1)
    
    iv_ax.get_figure().savefig(images%(reference, 'iv'),bbox_inches='tight')
    if_ax.get_figure().savefig(images%(reference, 'if'),bbox_inches='tight')
               
    temp_dir = 'temp/'
    
    print("Copying %s to %s"%(cell_file, temp_dir))
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
                info, 
                xaxis = "Time (ms)", 
                yaxis = "Membrane potential (mV)",
                show_plot_already=False,
                ylim = [-120, 60],
                save_figure_to = images%(reference, 'traces'),
                title_above_plot=True)
    

if __name__ == '__main__':

    os.chdir('tuned_cells')
    
    nogui = '-nogui' in sys.argv
    
    sys.path.append("../data")
    import data_helper as DH

    dataset_ids = DH.CURRENT_DATASETS
    #dataset_ids = [486111903]

    for dataset_id in dataset_ids:

        type = 'HH'

        analyse_cell(dataset_id, type, nogui)

        type = 'Izh'

        analyse_cell(dataset_id, type, nogui)

    
    if not nogui:
        import matplotlib.pyplot as plt
        plt.show()
    
    
    

