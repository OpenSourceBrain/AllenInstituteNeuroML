
from pyneuroml import pynml
from neuroml import *

import math
import random




def rotate_z(x, y, theta):

    x_ = x * math.cos(theta) - y * math.sin(theta)
    y_ = x * math.sin(theta) + y * math.cos(theta)

    return x_, y_

def get_oriented_cell(cell_file_name):
    
    new_ref = "ROTATED_"+cell_file_name.split('.')[0]

    doc = loaders.NeuroMLLoader.load(cell_file_name)

    ox = doc.cells[0].morphology.segments[0].proximal.x
    oy = doc.cells[0].morphology.segments[0].proximal.y
    oz = doc.cells[0].morphology.segments[0].proximal.z
    print("Loaded morphology file from: %s at (%s,%s,%s)"%(cell_file_name,ox,oy,oz))

    doc.cells[0].id = new_ref

    allx = 0
    ally = 0
    segs_used = 0
    maxl = -1
    farx =0
    fary =0
    for segment in doc.cells[0].morphology.segments:
        dx = float(segment.distal.x) - ox
        dy = float(segment.distal.y) - oy
        l = math.sqrt(dx*dx+dy*dy)
        if l>maxl:
            maxl = l
            farx = dx
            fary = dy
        if l>50:
            allx += dx**3
            ally += dy**3
            segs_used+=1


    theta = math.atan2(fary,farx)
    #theta = math.atan2(ally,allx)
    #theta=0
    print("- Orient: (%s, %s), %s, %s, (%s,%s), %s degrees"%(allx/segs_used, ally/segs_used,allx/ally,segs_used, farx, fary, math.degrees(theta)))

    
    for segment in doc.cells[0].morphology.segments:

        if segment.proximal:
            segment.proximal.x = segment.proximal.x - ox
            segment.proximal.y = segment.proximal.y - oy

            segment.proximal.x, segment.proximal.y = rotate_z(segment.proximal.x, segment.proximal.y, -1*theta +math.pi/2)

        segment.distal.x = segment.distal.x - ox
        segment.distal.y = segment.distal.y - oy

        segment.distal.x, segment.distal.y = rotate_z(segment.distal.x, segment.distal.y, -1* theta+math.pi/2)


    new_cell_file = new_ref+'.cell.nml'

    writers.NeuroMLWriter.write(doc,new_cell_file)
    
    return new_ref, new_cell_file


net_ref = "SomeCells"
net_doc = NeuroMLDocument(id=net_ref)

net = Network(id=net_ref)
net_doc.networks.append(net)

count = 0

cells = {}


per_row = 5

import glob

all_cell_files  = glob.glob('Cell*cell.nml')

for cell_file in all_cell_files:
    
    print cell_file
    cell_doc = loaders.NeuroMLLoader.load(cell_file)
    cell = cell_doc.cells[0]
    include_this = True
    
    for cd in cell.biophysical_properties.membrane_properties.channel_densities:
        if cd.ion_channel=="Kv2like":
            include_this = False
    
    if include_this:
        new_ref, new_cell_file = get_oriented_cell(cell_file)

        net_doc.includes.append(IncludeType(new_cell_file))

        pop = Population(id="Pop_%s"%new_ref, component=new_ref, type="populationList")

        net.populations.append(pop)

        inst = Instance(id=0)
        pop.instances.append(inst)

        X= 400 * (count%per_row)
        Z= 400 * (count/per_row)

        Y = 0

        inst.location = Location(x=X, y=Y, z=Z)

        count+=1

net_file = '%s.net.nml'%(net_ref)
writers.NeuroMLWriter.write(net_doc, net_file)

print("Written network with %i cells in network to: %s"%(count,net_file))

pynml.nml2_to_png(net_file, max_memory="2G")
pynml.nml2_to_svg(net_file, max_memory="2G")
