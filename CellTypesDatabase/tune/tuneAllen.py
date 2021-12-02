'''

    Still under developemnt!!

    Subject to change without notice!!

'''

from pyneuroml.tune.NeuroMLTuner import run_optimisation, run_2stage_optimization

from pyneuroml.tune.NeuroMLController import NeuroMLController

import neuroml

import sys
from collections import OrderedDict

import json
import os


import random

import pprint
pp = pprint.PrettyPrinter(indent=4)


from pyneuroml import pynml

sys.path.append("../data")
import data_helper as DH
sys.path.append("../data/bulk_analysis")
import bulk_data_helper as BDH

#####    Pospischil et al 2008
              
parameters_hh = ['cell:RS/channelDensity:LeakConductance_all/mS_per_cm2',
              'cell:RS/erev_id:LeakConductance_all/mV',
              'cell:RS/specificCapacitance:all/uF_per_cm2',
              'cell:RS/channelDensity:Na_all/mS_per_cm2',
              'cell:RS/channelDensity:Kd_all/mS_per_cm2',
              'cell:RS/channelDensity:IM_all/mS_per_cm2',
              'cell:RS/erev_id:Na_all/mV',
              'cell:RS/erev_id:Kd_all/mV+cell:RS/erev_id:IM_all/mV',
              'cell:RS/vShift_channelDensity:Na_all/mV']


max_constraints_hh = [0.2,   -60,  4,  80, 30, 5,    60, -70, 10]
min_constraints_hh = [0.01, -100, 0.2, 10, 1, 1e-3, 50, -90, -10]



# Need to be updated...
#max_constraints_ahh = [1e-3, 1,  0.1 ]
#min_constraints_ahh = [1e-5, .1, 0.01]


#  typical (tuned) spiking cell
example_vars_hh = {'cell:RS/channelDensity:IM_all/mS_per_cm2': 0.18764779330203835,
                'cell:RS/channelDensity:Kd_all/mS_per_cm2': 16.95202053476659,
                'cell:RS/channelDensity:LeakConductance_all/mS_per_cm2': 0.09988609723098822,
                'cell:RS/channelDensity:Na_all/mS_per_cm2': 30.229674358155705,
                'cell:RS/erev_id:IM_all/mV': -81.1091911447433,
                'cell:RS/erev_id:Kd_all/mV': -70,
                'cell:RS/erev_id:LeakConductance_all/mV': -77.62455951121044,
                'cell:RS/erev_id:Na_all/mV': 55.053832510995626,
                'cell:RS/specificCapacitance:all/uF_per_cm2': 1.9607901262899832}

#####    Izhikevich 2007 cell model

parameters_iz = ['izhikevich2007Cell:RS/a/per_ms',
                 'izhikevich2007Cell:RS/b/nS',
                 'izhikevich2007Cell:RS/c/mV',
                 'izhikevich2007Cell:RS/d/pA',
                 'izhikevich2007Cell:RS/C/pF',
                 'izhikevich2007Cell:RS/vr/mV',
                 'izhikevich2007Cell:RS/vt/mV',
                 'izhikevich2007Cell:RS/vpeak/mV',
                 'izhikevich2007Cell:RS/k/nS_per_mV']

# Example parameter ranges for above
#                     a,     b,  c,  d,   C,    vr,  vt, vpeak, k
min_constraints_iz = [0.01, -5, -65, 10,  30,  -90, -60, 0,    0.1]
max_constraints_iz = [0.4,  20, -10, 400, 300, -70,  50, 70,   1]

#  typical (tuned) spiking cell
example_vars_iz = {'izhikevich2007Cell:RS/C/pF': 121.89939137782264,
                    'izhikevich2007Cell:RS/a/per_ms': 0.08048276778661327,
                    'izhikevich2007Cell:RS/b/nS': 0.42252877652260556,
                    'izhikevich2007Cell:RS/c/mV': -45.823508919072445,
                    'izhikevich2007Cell:RS/d/pA': 214.2736731101308,
                    'izhikevich2007Cell:RS/k/nS_per_mV': 0.22246514332222897,
                    'izhikevich2007Cell:RS/vpeak/mV': 32.332261968942376,
                    'izhikevich2007Cell:RS/vr/mV': -78.1568627395237,
                    'izhikevich2007Cell:RS/vt/mV': -21.563700799975003}
                   
                   


####  Test target data

ref = 'Pop0/6/RS/v:'
average_maximum = ref+'average_maximum'
average_minimum = ref+'average_minimum'
mean_spike_frequency = ref+'mean_spike_frequency'
#first_spike_time = ref+'first_spike_time'
average_last_1percent = ref+'average_last_1percent'

weights = {average_maximum: 1,
           average_minimum: 1,
           mean_spike_frequency: 5,
           average_last_1percent: 1}

target_data = {average_maximum: 39.264008,
               average_minimum: -46.123882,
               mean_spike_frequency: 26.042480494182108,
               average_last_1percent: -70}



####     Target data


def get_2stage_target_values(dataset_id):

    
    if os.path.isfile("../data/%s_analysis.json"%dataset_id):
        print("Core test example %s"%dataset_id)
        target_sweep_numbers = DH.DATASET_TARGET_SWEEPS
        sweep_numbers = target_sweep_numbers[dataset_id]
        
        with open("../data/%s_analysis.json"%dataset_id, "r") as json_file:
            metadata = json.load(json_file)
    else:
        
        print("Bulk test example %s"%dataset_id)
        target_sweep_numbers = BDH.DATASET_TARGET_SWEEPS
        sweep_numbers = target_sweep_numbers[dataset_id]
        
        with open("../data/bulk_analysis/%s_analysis.json"%dataset_id, "r") as json_file:
            metadata = json.load(json_file)

    ref0 = 'Pop0/0/RS/v:'
    ref1 = 'Pop0/1/RS/v:'
    ref2 = 'Pop0/2/RS/v:'
    ref3 = 'Pop0/3/RS/v:'
    ref5 = 'Pop0/5/RS/v:'
    ref6 = 'Pop0/6/RS/v:'

    steady_average = 'average_1000_1200'
    steady0 = ref0+steady_average
    steady_pre0 = ref0+'average_100_200'
    ref0_280 = ref0+'value_280'
    steady1 = ref1+steady_average
    steady2 = ref2+steady_average
    steady3 = ref3+steady_average

    '''
    weights_1 = {steady0: 2,
                 steady_pre0: 1,
                 ref0_280: 1,
                 steady1: 1,
                 steady2: 1,
                 steady3: 1}'''
                 
    weights_1 = {steady0: 2,
                 steady_pre0: 1,
                 ref0_280: 1,
                 steady1: 1}

    sw0 = "%s"%sweep_numbers[0]
    sw1 = "%s"%sweep_numbers[1]
    sw2 = "%s"%sweep_numbers[2]
    sw3 = "%s"%sweep_numbers[3]
    sw4 = "%s"%sweep_numbers[4]
    sw5 = "%s"%sweep_numbers[5]
    sw6 = "%s"%sweep_numbers[6]

    '''target_data_1 = {steady0:                metadata['sweeps'][sw0]["pyelectro_iclamp_analysis"][sw0+":"+steady_average],
                     steady_pre0:            metadata['sweeps'][sw0]["pyelectro_iclamp_analysis"][sw0+":average_100_200"],
                     ref0_280:               metadata['sweeps'][sw0]["pyelectro_iclamp_analysis"][sw0+":value_280"],
                     steady1:                metadata['sweeps'][sw1]["pyelectro_iclamp_analysis"][sw1+":"+steady_average],
                     steady2:                metadata['sweeps'][sw2]["pyelectro_iclamp_analysis"][sw2+":"+steady_average],
                     steady3:                metadata['sweeps'][sw3]["pyelectro_iclamp_analysis"][sw3+":"+steady_average]}'''

    target_data_1 = {steady0:                metadata['sweeps'][sw0]["pyelectro_iclamp_analysis"][sw0+":"+steady_average],
                     steady_pre0:            metadata['sweeps'][sw0]["pyelectro_iclamp_analysis"][sw0+":average_100_200"],
                     ref0_280:               metadata['sweeps'][sw0]["pyelectro_iclamp_analysis"][sw0+":value_280"],
                     steady1:                metadata['sweeps'][sw1]["pyelectro_iclamp_analysis"][sw1+":"+steady_average]}

    average_maximum6 = ref6+'average_maximum'
    average_minimum6 = ref6+'average_minimum'
    mean_spike_frequency6 = ref6+'mean_spike_frequency'
    mean_spike_frequency5 = ref5+'mean_spike_frequency'
    max_peak_no3 = ref3+'max_peak_no' # should be zero


    target_data_2 = {average_maximum6:      metadata['sweeps'][sw6]["pyelectro_iclamp_analysis"][sw6+":average_maximum"],
                     average_minimum6:      metadata['sweeps'][sw6]["pyelectro_iclamp_analysis"][sw6+":average_minimum"],
                     mean_spike_frequency6: metadata['sweeps'][sw6]["pyelectro_iclamp_analysis"][sw6+":mean_spike_frequency"],
                     mean_spike_frequency5: metadata['sweeps'][sw5]["pyelectro_iclamp_analysis"][sw5+":mean_spike_frequency"],
                     max_peak_no3:          metadata['sweeps'][sw3]["pyelectro_iclamp_analysis"][sw3+":max_peak_no"]} 

    weights_2 = {}
    
    for td in target_data_2.keys():
        weights_2[td] = 1
        
        
    for td in target_data_1.keys():
        target_data_2[td] = target_data_1[td]
        weights_2[td] = 1
        
    for t in weights_2.keys():
        
        passive_weights = 10
        
        if '1000_1200' in t:
            weights_2[t] = passive_weights
            
        if 'average_100_200' in t:
            weights_2[t] = passive_weights
            
        if 'value_280' in t:
            weights_2[t] = passive_weights
            
            
        

    return sweep_numbers, weights_1, target_data_1, weights_2, target_data_2
    
    
def run_one_optimisation(ref,
                     seed,
                     population_size,
                     max_evaluations,
                     num_selected,
                     num_offspring,
                     mutation_rate,
                     num_elites,
                     simulator,
                     nogui,
                     parameters,
                     max_constraints,
                     min_constraints,
                     neuroml_file =     'prototypes/RS/AllenTest.net.nml',
                     target =           'network_RS',
                     weights =          weights,
                     target_data =      target_data,
                     dt =               0.025,
                     num_parallel_evaluations = 1):

    ref = '%s__s%s_p%s_m%s_s%s_o%s_m%s_e%s'%(ref,
                     seed,
                     population_size,
                     max_evaluations,
                     num_selected,
                     num_offspring,
                     mutation_rate,
                     num_elites)           

    return run_optimisation(prefix =           ref, 
                     neuroml_file =     neuroml_file,
                     target =           target,
                     parameters =       parameters,
                     max_constraints =  max_constraints,
                     min_constraints =  min_constraints,
                     weights =          weights,
                     target_data =      target_data,
                     sim_time =         1500,
                     dt =               dt,
                     seed =             seed,
                     population_size =  population_size,
                     max_evaluations =  max_evaluations,
                     num_selected =     num_selected,
                     num_offspring =    num_offspring,
                     mutation_rate =    mutation_rate,
                     num_elites =       num_elites,
                     simulator =        simulator,
                     nogui =            nogui,
                     num_parallel_evaluations = num_parallel_evaluations)



def scale(scale, number, min_=1, max_=sys.maxsize):
    num = max(min_, int(scale*number))
    return min(max_, num)





def compare(sim_data_file, show_plot_already=True, dataset=471141261):
    dat_file_name = '../data/%s.dat'%dataset
    
    x = []
    y = []
    colors = []
    linestyles = []

    data, indeces = pynml.reload_standard_dat_file(dat_file_name)

    for ii in indeces:
        x.append(data['t'])
        y.append(data[ii])
        colors.append('lightgrey')
        linestyles.append('-')

    data, indeces = pynml.reload_standard_dat_file(sim_data_file)

    r = lambda: random.randint(0,255)

    for ii in indeces:
        print("Adding %s from %s"%(ii,sim_data_file))
        x.append(data['t'])
        y.append(data[ii])
        c = '#%02X%02X%02X' % (r(),r(),r())
        colors.append(c)
        linestyles.append('-')

    pynml.generate_plot(x,
                        y, 
                        "Comparing tuned cell (in %s) to data: %s"%(sim_data_file, dataset), 
                        xaxis = 'Input current (nA)', 
                        yaxis = 'Membrane potential (mV)', 
                        colors = colors, 
                        linestyles = linestyles, 
                        show_plot_already=show_plot_already)


def run_2_stage_hh(dataset, simulator  = 'jNeuroML_NEURON', scale1=1, scale2=1,seed = 1234678, nogui=False,mutation_rate = 0.9, tail=1):
    
        print("Running 2 stage hh optimisation")
        
        type = 'HH'
        ref = 'network_%s_%s'%(dataset, type)

        max_constraints_1 = [1,     -50,  5,   0, 0, 0, 55, -80, 0]
        min_constraints_1 = [0.001, -100, 0.2, 0, 0, 0, 55, -80, 0]

        # For a quick test...
        # max_constraints_1 = [0.1,   -77.9, 0.51,   0, 0, 0, 55, -80]
        # min_constraints_1 = [0.09,  -77.8, 0.52,   0, 0, 0, 55, -80]

        max_constraints_2 = ['x',   'x',   'x',    100,  35,   5,    60, -70,  10]
        min_constraints_2 = ['x',   'x',   'x',    10,   1,    1e-6, 50, -100, -10]

        sweep_numbers, weights_1, target_data_1, weights_2, target_data_2 = get_2stage_target_values(dataset)


        r1, r2 = run_2stage_optimization('Allen2stage',
                                neuroml_file = 'prototypes/RS/%s.net.nml'%ref,
                                target =        ref,
                                parameters = parameters_hh,
                                max_constraints_1 = max_constraints_1,
                                max_constraints_2 = max_constraints_2,
                                min_constraints_1 = min_constraints_1,
                                min_constraints_2 = min_constraints_2,
                                delta_constraints = 0.05,
                                weights_1 = weights_1,
                                weights_2 = weights_2,
                                target_data_1 = target_data_1,
                                target_data_2 = target_data_2,
                                sim_time = 1500,
                                dt = 0.01,
                                population_size_1 = scale(scale1,100,10),
                                population_size_2 = scale(scale2,100,10),
                                max_evaluations_1 = scale(scale1,1000,20),
                                max_evaluations_2 = scale(scale2,1000,10)*tail,
                                num_selected_1 = scale(scale1,30,5),
                                num_selected_2 = scale(scale2,30,5),
                                num_offspring_1 = scale(scale1,30,5),
                                num_offspring_2 = scale(scale2,30,5),
                                mutation_rate = mutation_rate,
                                num_elites = scale(scale2,3,1, 5),
                                simulator = simulator,
                                nogui = nogui,
                                show_plot_already = False,
                                seed = seed,
                                known_target_values = {},
                                dry_run = False,
                                num_parallel_evaluations = 16,
                                extra_report_info = {'dataset':dataset,"Prototype":"HH"})
        
        if not nogui:
            compare('%s/%s.Pop0.v.dat'%(r1['run_directory'], r1['reference']), show_plot_already=False,    dataset=dataset)
            compare('%s/%s.Pop0.v.dat'%(r2['run_directory'], r2['reference']), show_plot_already=not nogui,dataset=dataset)
        
        
        final_network = '%s/%s.net.nml'%(r2['run_directory'], ref)
        
        nml_doc = pynml.read_neuroml2_file(final_network)
        
        cell = nml_doc.cells[0]
        
        print("Extracted cell: %s from tuned model"%cell.id)
        
        new_id = '%s_%s'%(type, dataset)
        new_cell_doc = neuroml.NeuroMLDocument(id=new_id)
        cell.id = new_id
        
        cell.notes = "Cell model tuned to Allen Institute Cell Types Database, dataset: "+ \
                     "%s\n\nTuning procedure metadata:\n\n%s\n"%(dataset, pp.pformat(r2))
        
        new_cell_doc.cells.append(cell)
        new_cell_file = 'tuned_cells/%s/%s.cell.nml'%(type,new_id)
        
        channel_files = ['IM.channel.nml', 'Kd.channel.nml', 'Leak.channel.nml', 'Na.channel.nml']
        for ch in channel_files:
            new_cell_doc.includes.append(neuroml.IncludeType(ch))
            
        pynml.write_neuroml2_file(new_cell_doc, new_cell_file)



def run_2_stage_hh2(dataset, simulator  = 'jNeuroML_NEURON', scale1=1, scale2=1,seed = 12346789, nogui=False,mutation_rate = 0.9, tail=1):
    
        print("Running 2 stage hh2 optimisation")
        
        type = 'HH2'
        ref = 'network_%s_%s'%(dataset, type)
        


        parameters_hh2 = ['cell:RS/channelDensity:LeakConductance_all/mS_per_cm2',
                      'cell:RS/erev_id:LeakConductance_all/mV',
                      'cell:RS/specificCapacitance:all/uF_per_cm2',
                      'cell:RS/channelDensity:Na_all/mS_per_cm2',
                      'cell:RS/channelDensity:Kd_all/mS_per_cm2',
                      'cell:RS/channelDensity:IM_all/mS_per_cm2',
                      'cell:RS/channelDensity:IL_all/mS_per_cm2',
                      'cell:RS/erev_id:Na_all/mV',
                      'cell:RS/erev_id:Kd_all/mV+cell:RS/erev_id:IM_all/mV',
                      'cell:RS/erev_id:IL_all/mV',
                      'cell:RS/vShift_channelDensity:Na_all/mV']

        max_constraints_1 = [2,     -50,  10,   100, 35, 0, 0, 60, -70,  100, 10]
        min_constraints_1 = [0.005, -100, 0.2, 10,  1,  0, 0, 50, -100, 100, -10]

        # For a quick test...
        # max_constraints_1 = [0.1,   -77.9, 0.51,   0, 0, 0, 55, -80]
        # min_constraints_1 = [0.09,  -77.8, 0.52,   0, 0, 0, 55, -80]

        max_constraints_2 = ['x', 'x', 'x', 'x', 'x', 5,    1,    'x', 'x', 100, 'x']
        min_constraints_2 = ['x', 'x', 'x', 'x', 'x', 1e-7, 1e-7, 'x', 'x', 40, 'x']

        sweep_numbers, weights_1, target_data_1, weights_2, target_data_2 = get_2stage_target_values(dataset)


        r1, r2 = run_2stage_optimization('HH2_2stage',
                                neuroml_file = 'prototypes/HH2/%s.net.nml'%ref,
                                target =        ref,
                                parameters = parameters_hh2,
                                max_constraints_1 = max_constraints_1,
                                max_constraints_2 = max_constraints_2,
                                min_constraints_1 = min_constraints_1,
                                min_constraints_2 = min_constraints_2,
                                delta_constraints = 0.1,
                                weights_1 = weights_2,
                                weights_2 = weights_2,
                                target_data_1 = target_data_2,
                                target_data_2 = target_data_2,
                                sim_time = 1500,
                                dt = 0.01,
                                population_size_1 = scale(scale1,100,10),
                                population_size_2 = scale(scale2,100,10),
                                max_evaluations_1 = scale(scale1,1000,20),
                                max_evaluations_2 = scale(scale2,1000,10)*tail,
                                num_selected_1 = scale(scale1,30,5),
                                num_selected_2 = scale(scale2,30,5),
                                num_offspring_1 = scale(scale1,30,5),
                                num_offspring_2 = scale(scale2,30,5),
                                mutation_rate = mutation_rate,
                                num_elites = scale(scale2,3,1, 5),
                                simulator = simulator,
                                nogui = nogui,
                                show_plot_already = False,
                                seed = seed,
                                known_target_values = {},
                                dry_run = False,
                                num_parallel_evaluations = 16,
                                extra_report_info = {'dataset':dataset,"Prototype":"HH2"})
        
        if not nogui:
            compare('%s/%s.Pop0.v.dat'%(r1['run_directory'], r1['reference']), show_plot_already=False,    dataset=dataset)
            compare('%s/%s.Pop0.v.dat'%(r2['run_directory'], r2['reference']), show_plot_already=not nogui,dataset=dataset)
        
        
        final_network = '%s/%s.net.nml'%(r2['run_directory'], ref)
        
        nml_doc = pynml.read_neuroml2_file(final_network)
        
        cell = nml_doc.cells[0]
        
        print("Extracted cell: %s from tuned model"%cell.id)
        
        new_id = '%s_%s'%(type, dataset)
        new_cell_doc = neuroml.NeuroMLDocument(id=new_id)
        cell.id = new_id
        
        cell.notes = "Cell model tuned to Allen Institute Cell Types Database, dataset: "+ \
                     "%s\n\nTuning procedure metadata:\n\n%s\n"%(dataset, pp.pformat(r2))
        
        new_cell_doc.cells.append(cell)
        new_cell_file = 'tuned_cells/%s/%s.cell.nml'%(type,new_id)
        
        channel_files = ['IM.channel.nml', 'Kd.channel.nml', 'Leak.channel.nml', 'Na.channel.nml', 'IL.channel.nml']
        for ch in channel_files:
            new_cell_doc.includes.append(neuroml.IncludeType(ch))
            
        pynml.write_neuroml2_file(new_cell_doc, new_cell_file)




def run_2_stage_allenhh(dataset, simulator  = 'jNeuroML_NEURON', scale1=1, scale2=1,seed = 1234678, nogui=False,mutation_rate = 0.9, tail=1):
    
        print("Running 2 stage hh optimisation")
        
        type = 'AllenHH'
        ref = 'network_%s_%s'%(dataset, type)
        
        #####    Allen set of channels
              
        parameters_ahh = ['cell:RS/channelDensity:pas_all/S_per_cm2',
                        'cell:RS/erev_id:pas_all/mV',
                        'cell:RS/specificCapacitance:all/uF_per_cm2',

                        'cell:RS/channelDensity:NaTs_all/S_per_cm2',
                        'cell:RS/channelDensity:Nap_all/S_per_cm2',

                        'cell:RS/channelDensity:K_P_all/S_per_cm2',
                        'cell:RS/channelDensity:K_T_all/S_per_cm2',
                        'cell:RS/channelDensity:Kv3_1_all/S_per_cm2',
                        'cell:RS/channelDensity:Im_all/S_per_cm2',
                        'cell:RS/channelDensity:Ih_all/S_per_cm2',

                        'cell:RS/channelDensityNernst:Ca_LVA_all/S_per_cm2',
                        'cell:RS/channelDensityNernst:Ca_HVA_all/S_per_cm2',

                        'cell:RS/erev_id:NaTs_all/mV+cell:RS/erev_id:Nap_all/mV',
                        'cell:RS/erev_id:K_P_all/mV+cell:RS/erev_id:K_T_all/mV+cell:RS/erev_id:Kv3_1_all/mV+cell:RS/erev_id:Im_all/mV']

        max_constraints_1 = [1e-3, -60,  20,   0,  0,       0, 0, 0, 0, 0,       0, 0,          50, -100]
        min_constraints_1 = [1e-6, -100, 0.1,  0,  0,       0, 0, 0, 0, 0,       0, 0,          50, -100]

        max_constraints_2 = ['x', 'x', 'x',    5,  .00001,  1, .3, 1, .1,  0.01,   0.05, 0.005,   60,  -70]
        min_constraints_2 = ['x', 'x', 'x',   .005, 0,      0, 0,  0,  0,  0,      0,    0,       45, -100]
        
        use_2_step = False
        use_2_step = True
        
        if not use_2_step:
            delta_constraints = 1
            for i in [0,1,2]:
                max_constraints_2[i] = max_constraints_1[i]
                min_constraints_2[i] = min_constraints_1[i]
        else:
            delta_constraints = 0.1

        sweep_numbers, weights_1, target_data_1, weights_2, target_data_2 = get_2stage_target_values(dataset)


        r1, r2 = run_2stage_optimization('Allen2stage',
                                neuroml_file = 'prototypes/AllenHH/%s.net.nml'%ref,
                                target =        ref,
                                parameters = parameters_ahh,
                                max_constraints_1 = max_constraints_1,
                                max_constraints_2 = max_constraints_2,
                                min_constraints_1 = min_constraints_1,
                                min_constraints_2 = min_constraints_2,
                                delta_constraints = delta_constraints,
                                weights_1 = weights_1,
                                weights_2 = weights_2,
                                target_data_1 = target_data_1,
                                target_data_2 = target_data_2,
                                sim_time = 1500,
                                dt = 0.025,
                                population_size_1 = scale(scale1,100,10),
                                population_size_2 = scale(scale2,100,10),
                                max_evaluations_1 = scale(scale1,1000,20),
                                max_evaluations_2 = scale(scale2,1000,10)*tail,
                                num_selected_1 = scale(scale1,30,5,30),
                                num_selected_2 = scale(scale2,30,5,30),
                                num_offspring_1 = scale(scale1,30,5),
                                num_offspring_2 = scale(scale2,30,5),
                                mutation_rate = mutation_rate,
                                num_elites = 1,
                                simulator = simulator,
                                nogui = nogui,
                                show_plot_already = False,
                                seed = seed,
                                known_target_values = {},
                                dry_run = False,
                                num_parallel_evaluations = 18,
                                extra_report_info = {'dataset':dataset,"Prototype":"AllenHH"})
        
        if not nogui:
            compare('%s/%s.Pop0.v.dat'%(r1['run_directory'], r1['reference']), show_plot_already=False,    dataset=dataset)
            compare('%s/%s.Pop0.v.dat'%(r2['run_directory'], r2['reference']), show_plot_already=not nogui,dataset=dataset)
        
        
        final_network = '%s/%s.net.nml'%(r2['run_directory'], ref)
        
        nml_doc = pynml.read_neuroml2_file(final_network)
        
        cell = nml_doc.cells[0]
        
        print("Extracted cell: %s from tuned model"%cell.id)
        
        new_id = '%s_%s'%(type, dataset)
        new_cell_doc = neuroml.NeuroMLDocument(id=new_id)
        cell.id = new_id
        
        cell.notes = "Cell model tuned to Allen Institute Cell Types Database, dataset: "+ \
                     "%s\n\nTuning procedure metadata:\n\n%s\n"%(dataset, pp.pformat(r2))
        
        new_cell_doc.cells.append(cell)
        new_cell_file = 'tuned_cells/%s/%s.cell.nml'%(type,new_id)
        
        channel_files = ['NaTs.channel.nml', 'K_P.channel.nml', 'Nap.channel.nml', 'Kv3_1.channel.nml', 'K_T.channel.nml', 'SK.channel.nml', 'Im.channel.nml', 'Ih.channel.nml', 'Ca_LVA.channel.nml', 'Ca_HVA.channel.nml', 'pas.channel.nml', 'CaDynamics.nml']   
        for ch in channel_files:
            new_cell_doc.includes.append(neuroml.IncludeType(ch))
            
        pynml.write_neuroml2_file(new_cell_doc, new_cell_file)



def run_2_stage_smith(dataset, simulator  = 'jNeuroML_NEURON', scale1=1, scale2=1,seed = 1234678, nogui=False,mutation_rate = 0.9):
    
        
        type = 'L23_Retuned'
        
        ref = 'network_%s_%s'%(dataset, type)
        
        print("Running 2 stage optimisation: " + 'prototypes/SmithEtAl2013/%s.net.nml'%ref)
        
        parameters_smith = ['cell:RS/channelDensity:pas_all/S_per_cm2',
                          'cell:RS/erev_id:pas_all/mV',
                          'cell:RS/specificCapacitance:all/uF_per_cm2',
                          
                          'cell:RS/channelDensity:na_soma/S_per_cm2+cell:RS/channelDensity:na_axon/S_per_cm2',
                          
                          'cell:RS/channelDensity:kv_soma/S_per_cm2+cell:RS/channelDensity:kv_axon/S_per_cm2']
                          

        max_constraints_1 = [5e-4, -70,  3,   0, 0]
        min_constraints_1 = [5e-5, -100, 0.3,  0, 0]

        max_constraints_2 = ['x', 'x', 'x',    2  , 0.2]
        min_constraints_2 = ['x', 'x', 'x',   .05, 0.005]
        
        
        '''
        
        <channelDensity ionChannel="pas" id="pas_all"  condDensity = "0.000142857 S_per_cm2" ion="non_specific" erev="-75 mV" />
        <channelDensity ionChannel="kca" id="kca_dends"  condDensity = "3.0e-4 S_per_cm2" ion="k" segmentGroup="dendrite_group" erev="-90 mV" />
        <channelDensity ionChannel="kca" id="kca_soma"  condDensity = "3.0e-4 S_per_cm2" ion="k" segmentGroup="soma_group" erev="-90 mV" />
        <channelDensity ionChannel="km" id="km_dends"  condDensity = "1e-4 S_per_cm2" ion="k" segmentGroup="dendrite_group" erev="-90 mV" />
        <channelDensity ionChannel="km" id="km_soma"  condDensity = "2.2e-4 S_per_cm2" ion="k" segmentGroup="soma_group" erev="-90 mV" />
        <channelDensity ionChannel="kv" id="kv_dends"  condDensity = "0.0003 S_per_cm2" ion="k" segmentGroup="dendrite_group" erev="-90 mV" />
        <channelDensity ionChannel="kv" id="kv_soma"  condDensity = "0.01 S_per_cm2" ion="k" segmentGroup="soma_group" erev="-90 mV" />
        <channelDensity ionChannel="kv" id="kv_axon"  condDensity = "0.01 S_per_cm2" ion="k" segmentGroup="axon_group" erev="-90 mV" />
        <channelDensity ionChannel="na" id="na_dends"  condDensity = "0.008 S_per_cm2" ion="na" segmentGroup="dendrite_group"  erev="60 mV" />
        <channelDensity ionChannel="na" id="na_soma"  condDensity = "0.5 S_per_cm2" ion="na" segmentGroup="soma_group" erev="60 mV" />
        <channelDensity ionChannel="na" id="na_axon"  condDensity = "0.5 S_per_cm2" ion="na" segmentGroup="axon_group" erev="60 mV" />
        <channelDensity ionChannel="it" id="it_dends" condDensity = "0.00015 S_per_cm2" ion="ca" segmentGroup="dendrite_group" erev="140.67523 mV" />       
        <channelDensity ionChannel="it" id="it_soma"  condDensity = "0.0003 S_per_cm2" ion="ca" segmentGroup="soma_group" erev="140.67523 mV" /> 
        <channelDensity ionChannel="ca" id="ca_dends" condDensity = "5e-5 S_per_cm2" ion="ca" segmentGroup="dendrite_group"  erev="140.67523 mV"/>
        <channelDensity ionChannel="ca" id="ca_soma" condDensity = "5e-5 S_per_cm2" ion="ca" segmentGroup="soma_group" erev="140.67523 mV"/>
        
        parameters_smith = ['cell:RS/channelDensity:pas_all/S_per_cm2',
                          'cell:RS/erev_id:pas_all/mV',
                          'cell:RS/specificCapacitance:all/uF_per_cm2',

                          'cell:RS/channelDensity:NaTs_all/S_per_cm2',
                          'cell:RS/channelDensity:Nap_all/S_per_cm2',

                          'cell:RS/channelDensity:K_P_all/S_per_cm2',
                          'cell:RS/channelDensity:K_T_all/S_per_cm2',
                          'cell:RS/channelDensity:Kv3_1_all/S_per_cm2',
                          'cell:RS/channelDensity:Im_all/S_per_cm2',
                          'cell:RS/channelDensity:Ih_all/S_per_cm2',

                          'cell:RS/channelDensityNernst:Ca_LVA_all/S_per_cm2',
                          'cell:RS/channelDensityNernst:Ca_HVA_all/S_per_cm2',

                          'cell:RS/erev_id:NaTs_all/mV+cell:RS/erev_id:Nap_all/mV',
                          'cell:RS/erev_id:K_P_all/mV+cell:RS/erev_id:K_T_all/mV+cell:RS/erev_id:Kv3_1_all/mV+cell:RS/erev_id:Im_all/mV']'''

        
        dt = 0.05
        
        use_2_step = False
        use_2_step = False
        if not use_2_step:
            for i in [0,1,2]:
                max_constraints_2[i] = max_constraints_1[i]
                min_constraints_2[i] = min_constraints_1[i]

        sweep_numbers, weights_1, target_data_1, weights_2, target_data_2 = get_2stage_target_values(dataset)


        r1, r2 = run_2stage_optimization('Smith2stage',
                                neuroml_file = 'prototypes/SmithEtAl2013/%s.net.nml'%ref,
                                target =        ref,
                                parameters = parameters_smith,
                                max_constraints_1 = max_constraints_1,
                                max_constraints_2 = max_constraints_2,
                                min_constraints_1 = min_constraints_1,
                                min_constraints_2 = min_constraints_2,
                                delta_constraints = 0.1,
                                weights_1 = weights_1,
                                weights_2 = weights_2,
                                target_data_1 = target_data_1,
                                target_data_2 = target_data_2,
                                sim_time = 1500,
                                dt = dt,
                                population_size_1 = scale(scale1,100,10),
                                population_size_2 = scale(scale2,100,10),
                                max_evaluations_1 = scale(scale1,500,20),
                                max_evaluations_2 = scale(scale2,500,10),
                                num_selected_1 = scale(scale1,30,5),
                                num_selected_2 = scale(scale2,30,5),
                                num_offspring_1 = scale(scale1,30,5),
                                num_offspring_2 = scale(scale2,30,5),
                                mutation_rate = mutation_rate,
                                num_elites = scale(scale2,5,2),
                                simulator = simulator,
                                nogui = nogui,
                                show_plot_already = False,
                                seed = seed,
                                known_target_values = {},
                                dry_run = False,
                                num_parallel_evaluations = 18,
                                extra_report_info = {'dataset':dataset,"Prototype":"SmithEtAl2013"})
        
        if not nogui:
            compare('%s/%s.Pop0.v.dat'%(r1['run_directory'], r1['reference']), show_plot_already=False,    dataset=dataset)
            compare('%s/%s.Pop0.v.dat'%(r2['run_directory'], r2['reference']), show_plot_already=not nogui,dataset=dataset)
        
        
        final_network = '%s/%s.net.nml'%(r2['run_directory'], ref)
        
        nml_doc = pynml.read_neuroml2_file(final_network)
        
        cell = nml_doc.cells[0]
        
        print("Extracted cell: %s from tuned model"%cell.id)
        
        new_id = '%s_%s'%(type, dataset)
        new_cell_doc = neuroml.NeuroMLDocument(id=new_id)
        cell.id = new_id
        
        cell.notes = "Cell model tuned to Allen Institute Cell Types Database, dataset: "+ \
                     "%s\n\nTuning procedure metadata:\n\n%s\n"%(dataset, pp.pformat(r2))
        
        new_cell_doc.cells.append(cell)
        new_cell_file = 'tuned_cells/%s/%s.cell.nml'%(type,new_id)
        
        
        channel_files = ['pas.channel.nml',"ca.channel.nml","it.channel.nml","kca.channel.nml","km.channel.nml","kv.channel.nml","na.channel.nml"]   
        for ch in channel_files:
            new_cell_doc.includes.append(neuroml.IncludeType(ch))
            
        pynml.write_neuroml2_file(new_cell_doc, new_cell_file)



def run_2_stage_izh(dataset, simulator  = 'jNeuroML_NEURON', scale1=1, scale2=1,seed = 1234678, nogui=False,mutation_rate = 0.9):
    
    type = 'Izh'
    ref = 'network_%s_%s'%(dataset, type)

    #                     a,   b,  c,  d,   C,    vr,  vt, vpeak, k
    min_constraints_1 = [0.1, 1, -50, 300,  30,  -90, -30, 30,   0.01]
    max_constraints_1 = [0.1, 1, -50, 300, 300,  -70, -30, 30,   1]


    #                     a,     b,  c,  d,   C,    vr,  vt, vpeak, k
    min_constraints_2 = [0.01, -5, -65, 10,  'x',  'x', -60, 0,   'x']
    max_constraints_2 = [0.2,  20, -10, 400, 'x',  'x',  50, 70,  'x']

    sweep_numbers, weights_1, target_data_1, weights_2, target_data_2 = get_2stage_target_values(dataset)

    num_elites = scale(scale2,8,2,10)
    

    use_2_step = False
    #use_2_step = True

    if not use_2_step:
        delta_constraints = 1
        for i in [4,5,8]:
            max_constraints_2[i] = max_constraints_1[i]
            min_constraints_2[i] = min_constraints_1[i]
    else:
        delta_constraints = 0.05


    r1, r2 = run_2stage_optimization('AllenIzh2stage',
                            neuroml_file = 'prototypes/RS/%s.net.nml'%ref,
                            target = ref,
                            parameters = parameters_iz,
                            max_constraints_1 = max_constraints_1,
                            max_constraints_2 = max_constraints_2,
                            min_constraints_1 = min_constraints_1,
                            min_constraints_2 = min_constraints_2,
                            delta_constraints = delta_constraints,
                            weights_1 = weights_1,
                            weights_2 = weights_2,
                            target_data_1 = target_data_1,
                            target_data_2 = target_data_2,
                            sim_time = 1500,
                            dt = 0.05,
                            population_size_1 = scale(scale1,100,10),
                            population_size_2 = scale(scale2,100,10),
                            max_evaluations_1 = scale(scale1,1200,20),
                            max_evaluations_2 = scale(scale2,1200,10),
                            num_selected_1 = scale(scale1,50,5),
                            num_selected_2 = scale(scale2,50,5),
                            num_offspring_1 = scale(scale1,20,5),
                            num_offspring_2 = scale(scale2,20,5),
                            mutation_rate = mutation_rate,
                            num_elites = num_elites,
                            simulator = simulator,
                            nogui = nogui,
                            show_plot_already = False,
                            seed = seed,
                            known_target_values = {},
                            dry_run = False,
                            num_parallel_evaluations = 18,
                            extra_report_info = {'dataset':dataset,"Prototype":"Izhikevich"})


    if not nogui:       
        compare('%s/%s.Pop0.v.dat'%(r1['run_directory'], r1['reference']), show_plot_already=False,     dataset=dataset)
        compare('%s/%s.Pop0.v.dat'%(r2['run_directory'], r2['reference']), show_plot_already=not nogui, dataset=dataset)

    final_network = '%s/%s.net.nml'%(r2['run_directory'], ref)

    nml_doc = pynml.read_neuroml2_file(final_network)

    cell = nml_doc.izhikevich2007_cells[0]

    print("Extracted cell: %s from tuned model"%cell.id)

    new_id = '%s_%s'%(type, dataset)
    new_cell_doc = neuroml.NeuroMLDocument(id=new_id)
    cell.id = new_id

    cell.notes = "Cell model tuned to Allen Institute Cell Types Database, dataset: "+ \
                 "%s\n\nTuning procedure metadata:\n\n%s\n"%(dataset, pp.pformat(r2))

    new_cell_doc.izhikevich2007_cells.append(cell)
    new_cell_file = 'tuned_cells/%s/%s.cell.nml'%(type,new_id)

    pynml.write_neuroml2_file(new_cell_doc, new_cell_file)



if __name__ == '__main__':

    nogui = '-nogui' in sys.argv

    if '-compare' in sys.argv:

        compare('NT_AllenIzh__s12345_p200_m600_s80_o60_m0.1_e2_Mon_Nov_30_12.30.28_2015/AllenIzh__s12345_p200_m600_s80_o60_m0.1_e2.Pop0.v.dat')


    ####  Run simulation with one HH cell
    elif '-one' in sys.argv:   

        simulator  = 'jNeuroML_NEURON'
        #simulator  = 'jNeuroML'

        cont = NeuroMLController('AllenTest', 
                                 'prototypes/RS/AllenTest.net.nml',
                                 'network_RS',
                                 1500, 
                                 0.01, 
                                 simulator)

        sim_vars = OrderedDict(example_vars_hh)
        
        t, v = cont.run_individual(sim_vars, show=(not nogui))


    ####  Run simulation with multiple HH cells
    elif '-mone' in sys.argv:

        simulator  = 'jNeuroML_NEURON'
        #simulator  = 'jNeuroML'
        dataset = 471141261

        ref = 'network_%s_HH'%(dataset)
        cont = NeuroMLController('AllenTest', 
                                 'prototypes/RS/%s.net.nml'%ref,
                                 ref,
                                 1500, 
                                 0.01, 
                                 simulator)

        sim_vars = OrderedDict(example_vars_hh)
        
        t, v = cont.run_individual(sim_vars, show=(not nogui))


    ####  Run simulation with one Izhikevich cell
    elif '-izhone' in sys.argv:

        simulator  = 'jNeuroML'
        simulator  = 'jNeuroML_NEURON'

        cont = NeuroMLController('AllenIzhTest', 
                                 'prototypes/RS/AllenIzh.net.nml',
                                 'network_RS',
                                 1500, 
                                 0.05, 
                                 simulator)


        sim_vars = OrderedDict(example_vars_iz)

        t, v = cont.run_individual(sim_vars, show=(not nogui))

    ####  Run simulation with one AllenHH cell
    elif '-allenone' in sys.argv:

        simulator  = 'jNeuroML'
        simulator  = 'jNeuroML_NEURON'

        cont = NeuroMLController('AllenHHTest', 
                                 'prototypes/AllenHH/AllenHH.net.nml',
                                 'network_AllenHH',
                                 1500, 
                                 0.05, 
                                 simulator)


        sim_vars = OrderedDict()

        t, v = cont.run_individual(sim_vars, show=(not nogui))

    ####  Run simulation with one AllenHH cell
    elif '-smithone' in sys.argv:

        simulator  = 'jNeuroML'
        simulator  = 'jNeuroML_NEURON'

        cont = NeuroMLController('SmithTest', 
                                 'prototypes/SmithEtAl2013/L23_IV.net.nml',
                                 'L23_IV',
                                 400, 
                                 0.05, 
                                 simulator)


        sim_vars = OrderedDict()

        t, v = cont.run_individual(sim_vars, show=(not nogui))


    ####  Run simulation with multiple Izhikevich cells
    elif '-izhmone' in sys.argv:

        simulator  = 'jNeuroML'
        simulator  = 'jNeuroML_NEURON'
        
        dataset = 471141261
        #dataset = 464198958
        
        ref = 'network_%s_Izh'%(dataset)
        cont = NeuroMLController('AllenIzhMulti', 
                                 'prototypes/RS/%s.net.nml'%ref,
                                 ref,
                                 1500, 
                                 0.05, 
                                 simulator)

        sim_vars = OrderedDict(example_vars_iz)

        t, v = cont.run_individual(sim_vars, show=(not nogui))



    ####  Run a 'quick' optimisation for Izhikevich cell model
    elif '-izhquick' in sys.argv:

        simulator  = 'jNeuroML_NEURON'

        scale1 = 0.1
        
        dataset = 479704527
        ref = 'network_%s_Izh'%(dataset)

        report = run_one_optimisation('AllenIzh',
                            12345,
                            parameters =       parameters_iz,
                            max_constraints =  max_constraints_iz,
                            min_constraints =  min_constraints_iz,
                            population_size =  scale(scale1,100),
                            max_evaluations =  scale(scale1,500),
                            num_selected =     scale(scale1,30),
                            num_offspring =    scale(scale1,30),
                            mutation_rate =    0.1,
                            num_elites =       2,
                            simulator =        simulator,
                            nogui =            nogui,
                            dt =               0.05,
                            neuroml_file =     'prototypes/RS/%s.net.nml'%ref,
                            target =           ref)

        compare('%s/%s.Pop0.v.dat'%(report['run_directory'], report['reference']), dataset=dataset)


    ####  Run a 'quick' optimisation for Izhikevich cell model
    elif '-allenquick' in sys.argv:

        simulator  = 'jNeuroML_NEURON'

        scale1 = 2
        
        dataset = 479704527
        dataset = 480351780
        ref = 'network_%s_AllenHH'%(dataset)

        report = run_one_optimisation('AllenHH',
                            123456,
                            parameters =       parameters_ahh,
                            max_constraints =  max_constraints_ahh,
                            min_constraints =  min_constraints_ahh,
                            population_size =  scale(scale1,100),
                            max_evaluations =  scale(scale1,500),
                            num_selected =     scale(scale1,30),
                            num_offspring =    scale(scale1,30),
                            mutation_rate =    0.1,
                            num_elites =       2,
                            simulator =        simulator,
                            nogui =            nogui,
                            dt =               0.025,
                            neuroml_file =     'prototypes/AllenHH/%s.net.nml'%ref,
                            target =           ref,
                            num_parallel_evaluations = 10)

        compare('%s/%s.Pop0.v.dat'%(report['run_directory'], report['reference']), dataset=dataset)


    ####  Testing scaling...
    elif '-test' in sys.argv:

        simulator  = 'jNeuroML'

        scale1 = .2
        
        dataset = 464198958
        ref = 'network_%s_Izh'%(dataset)

        report = run_one_optimisation('AllenIzh',
                            123,
                            parameters =       parameters_iz,
                            max_constraints =  max_constraints_iz,
                            min_constraints =  min_constraints_iz,
                            population_size =  scale(scale1,100),
                            max_evaluations =  scale(scale1,500),
                            num_selected =     scale(scale1,30),
                            num_offspring =    scale(scale1,30),
                            mutation_rate =    0.1,
                            num_elites =       2,
                            simulator =        simulator,
                            nogui =            nogui,
                            dt =               0.05,
                            neuroml_file =     'prototypes/RS/%s.net.nml'%ref,
                            target =           ref,
                            num_parallel_evaluations = 10)

        compare('%s/%s.Pop0.v.dat'%(report['run_directory'], report['reference']), dataset=dataset)


    ####  Run a 2 stage optimisation for Izhikevich cell model

    elif '-izh2stage' in sys.argv:

        print("Running 2 stage optimisation")
        simulator  = 'jNeuroML_NEURON'
        dataset = 471141261
        dataset = 325941643
        dataset = 479704527
        dataset = 485058595
        dataset = 480169178
        dataset = 480351780
        dataset = 480353286
        dataset = 464198958
        dataset = 468120757
        dataset = 477127614  # L23 spiny
        dataset = 476686112  # l23 aspiny
        
        scale1 = .1
        scale2 = 8
        seed = 123456789
        mutation_rate = .1
        
        if len(sys.argv)>2:
            print("Parsing args: %s"%sys.argv)
            dataset = int(sys.argv[3])
            simulator = sys.argv[4]
            scale1 = float(sys.argv[5])
            scale2 = float(sys.argv[6])
            seed = float(sys.argv[7])
        
        run_2_stage_izh(dataset, simulator, scale1, scale2,seed, nogui=nogui, mutation_rate=mutation_rate)

    ####  Run a 2 stage optimisation for AllenHH cell model

    elif '-allenhh2stage' in sys.argv:
        
        print("Running 2 stage optimisation")
        simulator  = 'jNeuroML_NEURON'
        dataset = 471141261
        dataset = 325941643
        dataset = 464198958
        dataset = 485058595
        dataset = 480169178
        dataset = 480351780
        dataset = 480353286
        dataset = 468120757
        #dataset = 480351780 
        dataset = 477127614  # L23 spiny
        #dataset = 476686112  # l23 aspiny
        #dataset = 479704527
        
        scale1 = 8
        scale2 = 10
        tail= 3
        seed = 123345
        mutation_rate = [0.5, 0.15]
    
         
        if len(sys.argv)>2:
            print("Parsing args: %s"%sys.argv)
            dataset = int(sys.argv[3])
            simulator = sys.argv[4]
            scale1 = float(sys.argv[5])
            scale2 = float(sys.argv[6])
            seed = float(sys.argv[7])
        
        run_2_stage_allenhh(dataset, simulator, scale1, scale2,seed, nogui=nogui, mutation_rate=mutation_rate, tail=tail)
        
    ####  Run a 2 stage optimisation for AllenHH cell model

    elif '-hh2_2stage' in sys.argv:
        
        print("Running 2 stage optimisation")
        simulator  = 'jNeuroML_NEURON'
        dataset = 471141261
        dataset = 325941643
        dataset = 464198958
        dataset = 485058595
        dataset = 480169178
        dataset = 480351780
        dataset = 480353286
        dataset = 468120757
        #dataset = 480351780 
        dataset = 477127614  # L23 spiny
        #dataset = 476686112  # l23 aspiny
        #dataset = 479704527
        
        scale1 = 1
        scale2 = 1
        tail= 1
        seed = 123345
        mutation_rate = [0.5, 0.15]
        mutation_rate = 0.9
    
         
        if len(sys.argv)>2:
            print("Parsing args: %s"%sys.argv)
            dataset = int(sys.argv[3])
            simulator = sys.argv[4]
            scale1 = float(sys.argv[5])
            scale2 = float(sys.argv[6])
            seed = float(sys.argv[7])
        
        run_2_stage_hh2(dataset, simulator, scale1, scale2,seed, nogui=nogui, mutation_rate=mutation_rate, tail=tail)
        
        
    ####  Run a 2 stage optimisation for Smith 2013 cell model

    elif '-smith2stage' in sys.argv:
        
        print("Running 2 stage optimisation")
        simulator  = 'jNeuroML_NEURON'
        dataset = 471141261
        dataset = 325941643
        dataset = 464198958
        dataset = 485058595
        dataset = 480169178
        dataset = 480351780
        dataset = 480353286
        dataset = 468120757
        dataset = 479704527
        dataset = 479704527
        dataset = 477127614
        #dataset = 480351780 
        
        scale1 = 2
        scale2 = 3
        seed = 123
    
         
        if len(sys.argv)>2:
            print("Parsing args: %s"%sys.argv)
            dataset = int(sys.argv[3])
            simulator = sys.argv[4]
            scale1 = float(sys.argv[5])
            scale2 = float(sys.argv[6])
            seed = float(sys.argv[7])
        
        run_2_stage_smith(dataset, simulator, scale1, scale2,seed, nogui=nogui)
        


    ####  Run a 'quick' optimisation for HH cell model
    elif '-quick' in sys.argv:

        simulator  = 'jNeuroML_NEURON'
        
        dataset = 471141261
        ref = 'network_%s_HH'%(dataset)
        
        report = run_one_optimisation('AllenTestQ',
                            1234,
                            parameters =       parameters_hh,
                            max_constraints =  max_constraints_hh,
                            min_constraints =  min_constraints_hh,
                            population_size =  10,
                            max_evaluations =  30,
                            num_selected =     5,
                            num_offspring =    5,
                            mutation_rate =    0.9,
                            num_elites =       1,
                            neuroml_file =     'prototypes/RS/%s.net.nml'%ref,
                            target =           ref,
                            simulator =        simulator,
                            dt =               0.025,
                            nogui =            nogui)

        compare('%s/%s.Pop0.v.dat'%(report['run_directory'], report['reference']))


    ####  Run a 2 stage optimisation for HH cell model
    elif '-2stage' in sys.argv:

        print("Running 2 stage hh optimisation")
        simulator  = 'jNeuroML_NEURON'
        dataset = 471141261
        dataset = 479704527
        dataset = 325941643
        dataset = 464198958
        dataset = 485058595
        dataset = 486111903
        dataset = 464198958
        dataset = 476686112  # l23 aspiny
        dataset = 477127614  # L23 spiny
        
        scale1 = 6
        scale2 = 10
        tail = 3
        seed = 1111
        mutation_rate = [0.5, 0.15]
        
        if len(sys.argv)>2:
            print("Parsing args: %s"%sys.argv)
            dataset = int(sys.argv[3])
            simulator = sys.argv[4]
            scale1 = float(sys.argv[5])
            scale2 = float(sys.argv[6])
            seed = float(sys.argv[7])
        
        run_2_stage_hh(dataset, simulator, scale1, scale2,seed, nogui=nogui,mutation_rate = mutation_rate, tail = tail)
        
    elif '-all' in sys.argv:
        

        simulator  = 'jNeuroML_NEURON'
        
        scale1 = 3
        scale2 = 3
        seed = 1234
        
        sys.path.append("../data")
        import data_helper as DH

        dataset_ids = DH.CURRENT_DATASETS
        #dataset_ids = [477127614]
        
        f = open('tuneAll.sh','w')

        for dataset_id in dataset_ids:
            #f.write('python tuneAllen.py -2stage -nogui %s %s %s %s %s\n'%(dataset_id,simulator, scale1, scale2,seed))
            f.write('python tuneAllen.py -hh2_2stage -nogui %s %s %s %s %s\n'%(dataset_id,simulator, scale1, scale2,seed))
            #f.write('python tuneAllen.py -allenhh2stage -nogui %s %s %s %s %s\n'%(dataset_id,simulator, scale1, scale2,seed))
            #f.write('python tuneAllen.py -izh2stage -nogui %s %s %s %s %s\n'%(dataset_id,simulator, scale1, scale2,seed))
            #run_2_stage_hh(dataset_id, simulator, scale1, scale2, seed, nogui=True)
            #run_2_stage_izh(dataset_id, simulator, scale1, scale2, seed, nogui=True)
            f.write('swapoff -a\n')
            f.write('swapon -a\n\n')
        f.close()
        
    elif '-bulk' in sys.argv:
        

        simulator  = 'jNeuroML_NEURON'
        
        scale1 = 3
        scale2 = 3
        seed = 123
        
        sys.path.append("../data")
        import data_helper as DH
        sys.path.append("../data/bulk_analysis")
        import bulk_data_helper as BDH

        dataset_ids = BDH.CURRENT_DATASETS
        #dataset_ids = [485058595]
        
        f = open('tuneBulk.sh','w')

        for dataset_id in dataset_ids:
            #if not dataset_id in DH.CURRENT_DATASETS:
            ###f.write('python tuneAllen.py -2stage -nogui %s %s %s %s %s\n'%(dataset_id,simulator, scale1, scale2,seed))
            #f.write('python tuneAllen.py -izh2stage -nogui %s %s %s %s %s\n'%(dataset_id,simulator, scale1, scale2,seed))
            f.write('python tuneAllen.py -hh2_2stage -nogui %s %s %s %s %s\n'%(dataset_id,simulator, scale1, scale2,seed))
            #run_2_stage_hh(dataset_id, simulator, scale1, scale2, seed, nogui=True)
            #run_2_stage_izh(dataset_id, simulator, scale1, scale2, seed, nogui=True)
            f.write('swapoff -a\n')
            f.write('swapon -a\n\n')
        f.close()

    else:

        print("Options to try:\n\n   (Izhikevich cell model)")
        print("     python tuneAllen.py -izhone     (run one Izhikevich cell with typical values)")
        print("     python tuneAllen.py -izhmone    (run multiple Izhikevich cells with different current inputs)")
        print("     python tuneAllen.py -izhquick   (quick optimisation example using Izhikevich cell)")
        print("     python tuneAllen.py -izh2stage  (2 stage optimisation example using Izhikevich cell)")
        print("\n   (HH cell model, based on Pospischil et al 2008)")
        print("     python tuneAllen.py -one    (run one HH cell with typical values)")
        print("     python tuneAllen.py -mone   (run multiple HH cells with different current inputs)")
        print("     python tuneAllen.py -quick  (quick optimisation example using HH cell)")
        print("     python tuneAllen.py -2stage  (2 stage optimisation example using HH cell)\n")



