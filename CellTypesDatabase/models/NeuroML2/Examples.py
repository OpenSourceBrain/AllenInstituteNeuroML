
from pyneuroml import pynml
from neuroml import *
import os
import math


max_per_layer = 100
layers = ['L23', 'L4', 'L5', 'L6']


t1=-0
t2=-100
t3=-100
t4=-190.0
t5=-300.0
t6=-300.0
ys = {}

ys['L1']=[0,t1]
ys['L23']=[t1,t1+t2+t3]
ys['L4']=[t1+t2+t3,t1+t2+t3+t4]
ys['L5']=[t1+t2+t3+t4,t1+t2+t3+t4+t5]
ys['L6']=[t1+t2+t3+t4+t5,t1+t2+t3+t4+t5+t6]


def rotate_z(x, y, theta):
    
    x_ = x * math.cos(theta) - y * math.sin(theta)
    y_ = x * math.sin(theta) + y * math.cos(theta)
    
    return x_, y_

net_ref = "CellTypesPerLayer"
net_doc = NeuroMLDocument(id=net_ref)

net = Network(id=net_ref)
net_doc.networks.append(net)

count = 0

cells = {}



cells['L23'] = ['Cell_473862496.cell.nml']
cells['L4'] =  ['Cell_472427533.cell.nml']
cells['L5'] = ['Cell_473871773.cell.nml']
cells['L6'] = ['Cell_473871592.cell.nml']

for layer in ['L23','L4','L5','L6']:
    for cell in cells[layer]:

	new_ref = "ROTATED_"+cell.split('.')[0]

        doc = loaders.NeuroMLLoader.load(cell)
        print("Loaded morphology file from: "+cell)

        ox = doc.cells[0].morphology.segments[0].proximal.x
        oy = doc.cells[0].morphology.segments[0].proximal.y

        doc.cells[0].id = new_ref

        allx = 0
        ally = 0
        for segment in doc.cells[0].morphology.segments:
            allx += float(segment.distal.x) - ox
            ally += float(segment.distal.y) - oy


        theta = math.atan(-1*allx/ally)
        print("Orient: (%s, %s), %s degrees"%(allx, ally, math.degrees(theta)))


        for segment in doc.cells[0].morphology.segments:

            if segment.proximal:
                segment.proximal.x = segment.proximal.x - ox
                segment.proximal.y = segment.proximal.y - oy

                segment.proximal.x, segment.proximal.y = rotate_z(segment.proximal.x, segment.proximal.y, -1*theta +math.pi)

            segment.distal.x = segment.distal.x - ox
            segment.distal.y = segment.distal.y - oy

            segment.distal.x, segment.distal.y = rotate_z(segment.distal.x, segment.distal.y, -1* theta+math.pi)


        new_cell_file = new_ref+'.cell.nml'

        writers.NeuroMLWriter.write(doc,new_cell_file)

        net_doc.includes.append(IncludeType(new_cell_file))

        pop = Population(id="Pop_%s"%new_ref, component=new_ref, type="populationList")

        net.populations.append(pop)

        inst = Instance(id="0")
        pop.instances.append(inst)
        
	X=count*300
	Z=0

	Y = ys[layer][1] + 0.5*(ys[layer][0] - ys[layer][1])
        inst.location = Location(x=X, y=Y, z=Z)
        
        count+=1

net_file = '%s.net.nml'%(net_ref)
writers.NeuroMLWriter.write(net_doc, net_file)

print("Written network with %i cells in network to: %s"%(count,net_file))

pynml.nml2_to_svg(net_file)
