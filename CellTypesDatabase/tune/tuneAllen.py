'''

    Still under developemnt!!

    Subject to change without notice!!

'''

from pyneuroml.tune.NeuroMLTuner import run_optimisation, run_2stage_optimization

from pyneuroml.tune.NeuroMLController import NeuroMLController

import sys
from collections import OrderedDict

import json

import matplotlib.pyplot as plt


#####    Pospischil et al 2008

parameters_hh = ['cell:RS/channelDensity:Na_all/mS_per_cm2',
              'cell:RS/channelDensity:Kd_all/mS_per_cm2',
              'cell:RS/channelDensity:IM_all/mS_per_cm2',
              'cell:RS/channelDensity:LeakConductance_all/mS_per_cm2',
              'cell:RS/erev_id:LeakConductance_all/mV',
              'cell:RS/erev_id:Na_all/mV',
              'cell:RS/erev_id:Kd_all/mV',
              'cell:RS/erev_id:IM_all/mV']

# Example parameter ranges for above
min_constraints = [20,   1,    1e-6,  0.001, -100, 50, -100, -100]
max_constraints = [100,  25,   4,     0.1,     -70,  60, -70,  -70]

#  typical spiking cell
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
max_constraints_iz = [0.2,  20, -10, 400, 300, -70,  50, 70,   1]

#  typical spiking cell
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

ref = 'Pop0/0/RS/v:'
average_maximum = ref+'average_maximum'
average_minimum = ref+'average_minimum'
mean_spike_frequency = ref+'mean_spike_frequency'
#first_spike_time = ref+'first_spike_time'
average_last_1percent = ref+'average_last_1percent'

weights = {average_maximum: 1,
           average_minimum: 1,
           mean_spike_frequency: 5,
           average_last_1percent: 1}

target_data = {average_maximum: 33.320915,
               average_minimum: -44.285,
               mean_spike_frequency: 26.6826,
               average_last_1percent: -80}



####     Improved target data

sweep_numbers = [34,38,42,46,50,54,58]


with open("../data/471141261_analysis.json", "r") as json_file:
    metadata = json.load(json_file)

ref0 = 'Pop0/0/RS/v:'
ref1 = 'Pop0/1/RS/v:'
ref2 = 'Pop0/2/RS/v:'
ref3 = 'Pop0/3/RS/v:'
ref5 = 'Pop0/5/RS/v:'
ref6 = 'Pop0/6/RS/v:'

minimum0 = ref0+'minimum'
average_last_1percent0 = ref0+'average_last_1percent'
ref0_280 = ref0+'value_280'
minimum1 = ref1+'minimum'
ref2_1000 = ref2+'value_1000'
ref3_1000 = ref3+'value_1000'


weights_1 = {minimum0: 1,
             average_last_1percent0: 1,
             ref0_280: 1,
             minimum1: 1,
             ref2_1000: 1,
             ref3_1000: 1}

sw0 = "%s"%sweep_numbers[0]
sw1 = "%s"%sweep_numbers[1]
sw2 = "%s"%sweep_numbers[2]
sw3 = "%s"%sweep_numbers[3]
sw4 = "%s"%sweep_numbers[4]
sw5 = "%s"%sweep_numbers[5]
sw6 = "%s"%sweep_numbers[6]

target_data_1 = {minimum0:               metadata['sweeps'][sw0]["pyelectro_iclamp_analysis"][sw0+":minimum"],
                 average_last_1percent0: metadata['sweeps'][sw0]["pyelectro_iclamp_analysis"][sw0+":average_last_1percent"],
                 ref0_280:               metadata['sweeps'][sw0]["pyelectro_iclamp_analysis"][sw0+":value_280"],
                 minimum1:               metadata['sweeps'][sw1]["pyelectro_iclamp_analysis"][sw1+":minimum"],
                 ref2_1000:              metadata['sweeps'][sw2]["pyelectro_iclamp_analysis"][sw2+":value_1000"],
                 ref3_1000:              metadata['sweeps'][sw3]["pyelectro_iclamp_analysis"][sw3+":value_1000"]}

average_maximum6 = ref6+'average_maximum'
average_minimum6 = ref6+'average_minimum'
mean_spike_frequency6 = ref6+'mean_spike_frequency'
mean_spike_frequency5 = ref5+'mean_spike_frequency'

weights_2 = {average_maximum6: 1,
           average_minimum6: 1,
           mean_spike_frequency6: 1,
           mean_spike_frequency5: 1}
           
for w in weights_1.keys():
    weights_2[w] = weights_1[w]*0.5

target_data_2 = {average_maximum6:      metadata['sweeps'][sw6]["pyelectro_iclamp_analysis"][sw6+":average_maximum"],
                 average_minimum6:      metadata['sweeps'][sw6]["pyelectro_iclamp_analysis"][sw6+":average_minimum"],
                 mean_spike_frequency6: metadata['sweeps'][sw6]["pyelectro_iclamp_analysis"][sw6+":mean_spike_frequency"],
                 mean_spike_frequency5: metadata['sweeps'][sw5]["pyelectro_iclamp_analysis"][sw5+":mean_spike_frequency"]} 

for td in target_data_1.keys():
    target_data_2[td] = target_data_1[td]
    
    
    
    
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
                     neuroml_file =     'prototypes/RS/AllenTest.net.nml',
                     target =           'network_RS',
                     parameters =       parameters_hh,
                     max_constraints =  max_constraints,
                     min_constraints =  min_constraints,
                     weights =          weights,
                     target_data =      target_data,
                     dt =               0.025):

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
                     nogui =            nogui)



def scale(scale, number, min=1):
    return max(min, int(scale*number))



def reload_standard_dat_file(file_name):

    dat_file = open(file_name)
    data = {}
    indeces = []
    for line in dat_file:
        words = line.split()

        if not data.has_key('t'):
            data['t'] = []
            for i in range(len(words)-1):
                data[i] = []
                indeces.append(i)
        data['t'].append(float(words[0]))
        for i in range(len(words)-1):
            data[i].append(float(words[i+1]))

    print("Loaded data from %s, %s"%(file_name, indeces))

    return data, indeces


def compare(sim_data_file):
    dat_file_name = '../data/471141261.dat'

    data, indeces = reload_standard_dat_file(dat_file_name)

    for ii in indeces:
        plt.plot(data['t'],data[ii], color='grey')

    data, indeces = reload_standard_dat_file(sim_data_file)

    for ii in indeces:
        plt.plot(data['t'],data[ii])

    plt.show()



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

        cont = NeuroMLController('AllenTest', 
                                 'prototypes/RS/AllenTestMulti.net.nml',
                                 'network_RS',
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


    ####  Run simulation with multiple Izhikevich cells
    elif '-izhmone' in sys.argv:

        simulator  = 'jNeuroML'
        simulator  = 'jNeuroML_NEURON'

        cont = NeuroMLController('AllenIzhMulti', 
                                 'prototypes/RS/AllenIzhMulti.net.nml',
                                 'network_RS',
                                 1500, 
                                 0.05, 
                                 simulator)

        sim_vars = OrderedDict(example_vars_iz)

        t, v = cont.run_individual(sim_vars, show=(not nogui))



    ####  Run a 'quick' optimisation for Izhikevich cell model
    elif '-izhquick' in sys.argv:

        simulator  = 'jNeuroML_NEURON'

        scale1 = 0.1

        report = run_one_optimisation('AllenIzh',
                            12345,
                            population_size =  scale(scale1,100),
                            max_evaluations =  scale(scale1,500),
                            num_selected =     scale(scale1,30),
                            num_offspring =    scale(scale1,30),
                            mutation_rate =    0.1,
                            num_elites =       2,
                            simulator =        simulator,
                            nogui =            nogui,
                            dt =               0.05,
                            neuroml_file =     'prototypes/RS/AllenIzh.net.nml',
                            target =           'network_RS',
                            parameters =       parameters_iz,
                            max_constraints =  max_constraints_iz,
                            min_constraints =  min_constraints_iz)

        compare('%s/%s.Pop0.v.dat'%(report['run_directory'], report['reference']))


    ####  Run a 2 stage optimisation for Izhikevich cell model

    elif '-izh2stage' in sys.argv:

        print("Running 2 stage optimisation")
        simulator  = 'jNeuroML_NEURON'

        #                     a,   b,  c,  d,   C,    vr,  vt, vpeak, k
        min_constraints_1 = [0.1, 1, -50, 300,  30,  -90, -30, 30,   0.01]
        max_constraints_1 = [0.1, 1, -50, 300, 300,  -70, -30, 30,   1]


        #                     a,     b,  c,  d,   C,    vr,  vt, vpeak, k
        min_constraints_2 = [0.01, -5, -65, 10,  'x',  'x', -60, 0,   'x']
        max_constraints_2 = [0.2,  20, -10, 400, 'x',  'x',  50, 70,  'x']

        scale1 = 0.1
        scale2 = 0.1

        r1, r2 = run_2stage_optimization('AllenIzh2stage',
                                neuroml_file =     'prototypes/RS/AllenIzhMulti.net.nml',
                                target =           'network_RS',
                                parameters = parameters_iz,
                                max_constraints_1 = max_constraints_1,
                                max_constraints_2 = max_constraints_2,
                                min_constraints_1 = min_constraints_1,
                                min_constraints_2 = min_constraints_2,
                                delta_constraints = 0.01,
                                weights_1 = weights_1,
                                weights_2 = weights_2,
                                target_data_1 = target_data_1,
                                target_data_2 = target_data_2,
                                sim_time = 1500,
                                dt = 0.05,
                                population_size_1 = scale(scale1,50,10),
                                population_size_2 = scale(scale2,100,10),
                                max_evaluations_1 = scale(scale1,200,20),
                                max_evaluations_2 = scale(scale2,500,10),
                                num_selected_1 = scale(scale1,30,5),
                                num_selected_2 = scale(scale2,30,5),
                                num_offspring_1 = scale(scale1,20,5),
                                num_offspring_2 = scale(scale2,20,5),
                                mutation_rate = 0.1,
                                num_elites = 2,
                                simulator = simulator,
                                nogui = nogui,
                                show_plot_already = True,
                                seed = 1234,
                                known_target_values = {},
                                dry_run = False)
                                
        compare('%s/%s.Pop0.v.dat'%(r1['run_directory'], r1['reference']))
        compare('%s/%s.Pop0.v.dat'%(r2['run_directory'], r2['reference']))


    ####  Run a 'quick' optimisation for HH cell model
    elif '-quick' in sys.argv:

        simulator  = 'jNeuroML_NEURON'
        
        run_one_optimisation('AllenTestQ',
                            1234,
                            population_size =  10,
                            max_evaluations =  30,
                            num_selected =     5,
                            num_offspring =    5,
                            mutation_rate =    0.9,
                            num_elites =       1,
                            simulator =        simulator,
                            nogui =            nogui)


    ####  Run a 2 stage optimisation for HH cell model
    elif '-2stage' in sys.argv:

        print("Running 2 stage optimisation")
        simulator  = 'jNeuroML_NEURON'


        max_constraints_1 = [0.1,   -70,  2,   0, 0, 0, 55, -80, -80]
        min_constraints_1 = [0.001, -100, 0.2, 0, 0, 0, 55, -80, -80]

        # For a quick test...
        # max_constraints_1 = [0.1,   -77.9, 0.51,   0, 0, 0, 55, -80, -80]
        # min_constraints_1 = [0.09,  -77.8, 0.52,   0, 0, 0, 55, -80, -80]

        max_constraints_2 = ['x',   'x',   'x',    100,  25,   4,    60, -70,  -70]
        min_constraints_2 = ['x',   'x',   'x',    20,   1,    1e-6, 50, -100, -100]


        scale1 = 0.1
        scale2 = 0.1

        r1, r2 = run_2stage_optimization('Allen2stage',
                                neuroml_file =     'prototypes/RS/AllenTestMulti.net.nml',
                                target =           'network_RS',
                                parameters = parameters_hh,
                                max_constraints_1 = max_constraints_1,
                                max_constraints_2 = max_constraints_2,
                                min_constraints_1 = min_constraints_1,
                                min_constraints_2 = min_constraints_2,
                                delta_constraints = 0.01,
                                weights_1 = weights_1,
                                weights_2 = weights_2,
                                target_data_1 = target_data_1,
                                target_data_2 = target_data_2,
                                sim_time = 1500,
                                dt = 0.05,
                                population_size_1 = scale(scale1,50,10),
                                population_size_2 = scale(scale2,100,10),
                                max_evaluations_1 = scale(scale1,200,20),
                                max_evaluations_2 = scale(scale2,500,10),
                                num_selected_1 = scale(scale1,30,5),
                                num_selected_2 = scale(scale2,30,5),
                                num_offspring_1 = scale(scale1,20,5),
                                num_offspring_2 = scale(scale2,20,5),
                                mutation_rate = 0.1,
                                num_elites = 2,
                                simulator = simulator,
                                nogui = nogui,
                                show_plot_already = True,
                                seed = 1234,
                                known_target_values = {},
                                dry_run = False)
                                
        compare('%s/%s.Pop0.v.dat'%(r1['run_directory'], r1['reference']))
        compare('%s/%s.Pop0.v.dat'%(r2['run_directory'], r2['reference']))


    ####  Run an optimisation for HH cell model
    else:

        simulator  = 'jNeuroML_NEURON'
        run_one_optimisation('AllenTest',
                            1234,
                            population_size =  20,
                            max_evaluations =  100,
                            num_selected =     15,
                            num_offspring =    15,
                            mutation_rate =    0.1,
                            num_elites =       1,
                            simulator =        simulator,
                            nogui =            nogui)



