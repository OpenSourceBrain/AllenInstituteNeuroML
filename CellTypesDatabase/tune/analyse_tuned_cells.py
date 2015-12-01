
import sys
import neuroml
from pyneuroml import pynml


from pyneuroml.analysis import generate_current_vs_frequency_curve


def analyse_cell(dataset_id, type, nogui = False):
    
    reference = '%s_%s'%(type,dataset_id)
    cell_file = 'tuned_cells/%s.cell.nml'%(reference)
    net_file = 'prototypes/RS/network_%s_%s.net.nml'%(type, dataset_id)
    
    images = 'tuned_cells/summary/%s_%s.png'
    
    generate_current_vs_frequency_curve(cell_file, 
                                        reference, 
                                        simulator = 'jNeuroML_NEURON',
                                        start_amp_nA =         -0.1, 
                                        end_amp_nA =           0.4, 
                                        step_nA =              0.01, 
                                        analysis_duration =    1000, 
                                        analysis_delay =       50,
                                        plot_voltage_traces =  not nogui,
                                        plot_if =              not nogui,
                                        plot_iv =              not nogui, 
                                        save_if_figure_to=images%(reference, 'if'), 
                                        save_iv_figure_to=images%(reference, 'iv'))

if __name__ == '__main__':

    nogui = '-nogui' in sys.argv

    dataset_id = 471141261
    type = 'Izh'
    analyse_cell(dataset_id, type, nogui)
    
    
    

