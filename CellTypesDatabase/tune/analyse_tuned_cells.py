
import sys
import neuroml
from pyneuroml import pynml


from pyneuroml.analysis import generate_current_vs_frequency_curve
from pyneuroml.lems import generate_lems_file_for_neuroml


def analyse_cell(dataset_id, type, nogui = False):
    
    reference = '%s_%s'%(type,dataset_id)
    cell_file = 'tuned_cells/%s.cell.nml'%(reference)
    net_file = 'prototypes/RS/network_%s_%s.net.nml'%(dataset_id,type)
    
    images = 'tuned_cells/summary/%s_%s.png'
    '''
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
                                        save_if_figure_to=images%(reference, 'if'), 
                                        save_iv_figure_to=images%(reference, 'iv'),
                                        show_plot_already = False)'''
                                        
    lems_file_name = 'LEMS_Test_%s_%s.xml'%(type,dataset_id)
    temp_dir = 'temp/'
    generate_lems_file_for_neuroml('Test_%s_%s'%(dataset_id,type),
                                   net_file,
                                   'network_%s_%s'%(dataset_id,type), 
                                   1500, 
                                   0.01, 
                                   lems_file_name,
                                   temp_dir,
                                   gen_plots_for_all_v=False)
    
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
    
    for i in range(len(results)-1):
        x.append(results['t'])
        y.append(results['Pop0/%i/RS/v'%i])
        
    pynml.generate_plot(x,
                y, 
                "Cell: %s"%dataset_id, 
                xaxis = "Time (ms)", 
                yaxis = "Membrane potential (mV)",
                show_plot_already=False,
                save_figure_to = None)
    

if __name__ == '__main__':

    nogui = '-nogui' in sys.argv
    type = 'Izh'

    dataset_id = 471141261
    analyse_cell(dataset_id, type, nogui)

    dataset_id = 464198958
    analyse_cell(dataset_id, type, nogui)
    
    if not nogui:
        import matplotlib.pyplot as plt
        plt.show()
    
    
    

