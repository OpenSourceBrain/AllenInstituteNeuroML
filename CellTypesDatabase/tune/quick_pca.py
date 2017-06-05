import numpy

type = 'HH'
type = 'Izh'

info_str = open('tuned_cells/tuned_cell_info.txt','r').read()

columns = ['IM','Kd','pas','Na','ek','ena','epas','Cm']

if type == 'Izh':
    info_str = open('tuned_cells/tuned_cell_info_izh.txt','r').read()

    columns = ['C','a','b','c','d','k','vpeak','vr','vt']
    

info = eval(info_str)

row_names = []
data = []

markers=[]
colours=[]

fitness_cutoff = 0.01

for ref in info['datasets']:
    tuned_cell_info = info['datasets'][ref]['tuned_cell_info']
    
    row = []
    
    spiny = info['datasets'][ref]['aibs_dendrite_type']
    location = info['datasets'][ref]['location']
    
    
    if 'ayer 2' in location:
        colour='b'
    elif 'ayer 4' in location:
        colour='k'
    elif 'ayer 5' in location:
        colour='r'
    elif 'ayer 6' in location:
        colour='c'
    else:
        colour='g'
        
    if spiny=='spiny':
        marker='x'
    else:
        marker='o'
        
    
    print("Checking %s, %s %s"%(ref,marker,colour))
    
    for col in range(len(columns)):
        col_name = columns[col]
        if col_name=='pas':
            col_name = 'LeakConductance'
        if col_name=='Cm':
            col_name = 'specific_capacitance_all'
            
        
        val = tuned_cell_info[col_name]
        if isinstance(val,dict):
            val = val['max']
            
        row.append(val)
        
    if info['datasets'][ref]['fitness']<=fitness_cutoff:
        data.append(row)
        markers.append(marker)
        colours.append(colour)
        row_names.append(ref)
    

from matplotlib.mlab import PCA

myData = numpy.array(data) 
results = PCA(myData) 

print("***** Input data *****")
print myData

print("***** Fracts *****")
#this will return an array of variance percentages for each component
print results.fracs


print("***** Y values *****")
#this will return a 2d array of the data projected into PCA space
print results.Y 

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


x = []
y = []
z = []
for item in results.Y:
 x.append(item[0])
 y.append(item[1])
 z.append(item[2])

plt.close('all') # close all latent plotting windows
fig1 = plt.figure() # Make a plotting figure
ax = Axes3D(fig1) # use the plotting figure to create a Axis3D object.
pltData = [x,y,z] 

for i in range(len(row_names)):
    ax.scatter(pltData[0][i], pltData[1][i], pltData[2][i], marker=markers[i], color=colours[i], label=row_names[i]) # make a scatter plot of blue dots from the data
 
# make simple, bare axis lines through space:
xAxisLine = ((min(pltData[0]), max(pltData[0])), (0, 0), (0,0)) # 2 points make the x-axis line at the data extrema along x-axis 
ax.plot(xAxisLine[0], xAxisLine[1], xAxisLine[2], 'r') # make a red line for the x-axis.
yAxisLine = ((0, 0), (min(pltData[1]), max(pltData[1])), (0,0)) # 2 points make the y-axis line at the data extrema along y-axis
ax.plot(yAxisLine[0], yAxisLine[1], yAxisLine[2], 'r') # make a red line for the y-axis.
zAxisLine = ((0, 0), (0,0), (min(pltData[2]), max(pltData[2]))) # 2 points make the z-axis line at the data extrema along z-axis
ax.plot(zAxisLine[0], zAxisLine[1], zAxisLine[2], 'r') # make a red line for the z-axis.
 
 
plt.legend(loc='upper left')


# label the axes 
ax.set_xlabel("x-axis label") 
ax.set_ylabel("y-axis label")
ax.set_zlabel("z-axis label")
ax.set_title("Plotting %s cells; fitness<=%s"%(len(data),fitness_cutoff))
plt.show() # show the plot


