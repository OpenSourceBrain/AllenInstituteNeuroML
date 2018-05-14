
### Allen CellTypes Database
 
Data and models from the [Allen CellTypes Database](http://celltypes.brain-map.org/) has been used to 
construct NeuroML based models. 

#### Data import 

Electrophysiological data on multiple cell types from the visual cortex of mouse have been made available on the 
[Allen CellTypes Database](http://celltypes.brain-map.org/).

There are scripts for importing/analysing this data [here](https://github.com/OpenSourceBrain/AllenInstituteNeuroML/tree/master/CellTypesDatabase/data).


#### NeuroML 2 models

[This directory](https://github.com/OpenSourceBrain/AllenInstituteNeuroML/tree/master/CellTypesDatabase/models) contains both examples
of the [original biophysical models in NEURON](https://github.com/OpenSourceBrain/AllenInstituteNeuroML/tree/master/CellTypesDatabase/models/NEURON)
(e.g. [483108201](https://github.com/OpenSourceBrain/AllenInstituteNeuroML/tree/master/CellTypesDatabase/models/483108201)) which have been generated 
by the Allen Institute from their own data, as well as [NeuroML 2 versions of these models](https://github.com/OpenSourceBrain/AllenInstituteNeuroML/tree/master/CellTypesDatabase/models/NeuroML2).


#### Retuned cell models

[This directory](https://github.com/OpenSourceBrain/AllenInstituteNeuroML/tree/master/CellTypesDatabase/tune) contains preliminary work to tune new
NeuroML2 models against the Allen CellTypes Database data for other types of NeuroML model (e.g. Izhikevich spiking models).

*Work in progress!*

