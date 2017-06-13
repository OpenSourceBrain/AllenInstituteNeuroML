
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

net_ref = "SomeCells2"
net_doc = NeuroMLDocument(id=net_ref)

net = Network(id=net_ref)
net_doc.networks.append(net)


cells = {}


per_row = 5

Y_layer = {}
Y_layer['2/3'] = 0
Y_layer['4'] = -200
Y_layer['5'] = -500
Y_layer['6a'] = -700

colours = {}
colours['2/3'] = '1 0 0'
colours['4'] = '0 0 1'
colours['5'] = '0 1 0'
colours['6a'] = '1 0 1'

import glob

all_cell_files  = glob.glob('Cell*cell.nml')

count_a = 0
count_s = 0

max_to_include = 1000

for cell_file in all_cell_files:
    
    if max_to_include>0:
        print("----- Adding: %s"%cell_file)
        cell_doc = loaders.NeuroMLLoader.load(cell_file)
        cell = cell_doc.cells[0]
        include_this = False

        info = ""
        for p in cell.properties:
            info += "  %s = %s\n"%(p.tag,p.value)
            print(info)
            if p.tag == 'AIBS:intracellular_ephys:Electrode 1:location':
                include_this = True
                layer = p.value.split(" ")[-1]
            if p.tag == 'AIBS:aibs_dendrite_type':
                dend_type = p.value

        for cd in cell.biophysical_properties.membrane_properties.channel_densities:
            if cd.ion_channel=="Kv2like":
                include_this = False

        if not include_this:
            print("       Skipping, no metadata...")
        if include_this:
            new_ref, new_cell_file = get_oriented_cell(cell_file)

            net_doc.includes.append(IncludeType(new_cell_file))

            pop = Population(id="Pop_%s"%new_ref, component=new_ref, type="populationList")

            net.populations.append(pop)

            p = Property(tag='color', value=colours[layer])
            pop.properties.append(p)
            pop.annotation = Annotation()
            p.original_tagname_ = 'property'
            pop.annotation.anytypeobjs_.append(p)
            pop.notes=info

            inst = Instance(id=0)
            pop.instances.append(inst)

            separation = 200
            offset = separation*(per_row+2)
            if dend_type=='spiny':
                X= separation * (count_s%per_row)
                Z= separation * (count_s/per_row)
                count_s+=1
            else:
                X= offset + (separation * (count_a%per_row))
                Z=  (separation * (count_a/per_row))
                count_a+=1

            Y = Y_layer[layer]

            inst.location = Location(x=X, y=Y, z=Z)
            
    max_to_include-=1


net_file = '%s.net.nml'%(net_ref)
writers.NeuroMLWriter.write(net_doc, net_file)

print("Written network with %i spiny & %i aspiny cells in network to: %s"%(count_s,count_a,net_file))

pynml.nml2_to_png(net_file, max_memory="2G")
pynml.nml2_to_svg(net_file, max_memory="2G")
