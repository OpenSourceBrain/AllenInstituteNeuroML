
from neuroml import NeuroMLDocument
from neuroml import Network
from neuroml import Population
from neuroml import Location
from neuroml import Instance
from neuroml import IncludeType

import neuroml.loaders as loaders
import neuroml.writers as writers
import math
import random
import glob



cells = ['467703703', '323452245']
cells = ['467703703', '471141261', '320207387', '471141261', '324493977', '464326095']
cell_files = glob.glob('*.cell.nml')
cells = [c.split('.')[0] for c in cell_files]


problematic = ['314642645', '469704261', '466664172', '314822529', '320654829', '324025371', '397353539', '469704261', '469753383']


net_ref = "Net"
net_doc = NeuroMLDocument(id=net_ref)

net = Network(id=net_ref)
net_doc.networks.append(net)

def rotate_z(x, y, theta):
    
    x_ = x * math.cos(theta) - y * math.sin(theta)
    y_ = x * math.sin(theta) + y * math.cos(theta)
    
    return x_, y_

count = 0
for cell in cells:
    
    suffix = '_trans'
    
    if cell not in problematic and suffix not in cell:
    
        new_ref = cell+suffix

        fn = cell+'.cell.nml'
        doc = loaders.NeuroMLLoader.load(fn)
        print("Loaded morphology file from: "+fn)

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


        nml_file = new_ref+'.cell.nml'

        writers.NeuroMLWriter.write(doc,nml_file)

        print("Saved modified morphology file to: "+nml_file)

        net_doc.includes.append(IncludeType(nml_file))

        pop = Population(id="Pop_%s"%new_ref, component=new_ref, type="populationList")

        net.populations.append(pop)

        inst = Instance(id="0")
        pop.instances.append(inst)
        
        width = 6
        X = count%width
        Z = (count -X) / width
        inst.location = Location(x=300*X, y=0, z=300*Z)
        
        count+=1


net_file = net_ref+'.net.nml'
writers.NeuroMLWriter.write(net_doc, net_file)

print("Written network with %i cells in network to: %s"%(count,net_file))
