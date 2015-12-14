
from pyneuroml import pynml


import matplotlib.pyplot as plt

files = ['NaV.states.dat', '../NEURON/Soma.states.dat']

for file in files:
    data, indices = pynml.reload_standard_dat_file(file)
    x = []
    y = []
    for i in indices:
        x.append(data['t'])
        y.append(data[i])

    totals = []
    for j in range(len(data['t'])):
        tot = 0
        for i in indices:
            tot+=data[i][j]
        totals.append(tot)

    labels = indices
    x.append(data['t'])
    y.append(totals)
    labels.append('total')

    pynml.generate_plot(x,
                        y, 
                        "States from file: %s"%file, 
                        xaxis = "Time (ms)", 
                        yaxis = "State occupancy",
                        labels = labels,
                        show_plot_already=False,
                        save_figure_to = None,
                        cols_in_legend_box = 6)


plt.show()
