"""

Example to build a network using libNeuroML, save it as XML and validate it

"""


#########################################################

import neuroml

nml_doc = neuroml.NeuroMLDocument(id="simplenet")

net = neuroml.Network(id="simplenet")
nml_doc.networks.append(net)

# Create 2 populations
size0 = 5
size1 = 5

pop0 = neuroml.Population(id="Pop0", size = size0)
net.populations.append(pop0)

pop0.annotation = neuroml.Annotation()
p = neuroml.Property(tag="axes_to_plot_tuple", value="(1,1)")
pop0.annotation.anytypeobjs_.append(p)


pop1 = neuroml.Population(id="Pop1", size = size1)
net.populations.append(pop1)

            
#########################################################


import neuroml.writers as writers

nml_file = 'simplenet.nml'
writers.NeuroMLWriter.write(nml_doc, nml_file)

print("Written network file to: "+nml_file)


###### Validate the NeuroML ######    

from neuroml.utils import validate_neuroml2

validate_neuroml2(nml_file)
