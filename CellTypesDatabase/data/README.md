
#### Data import 

Some scripts for pulling data from the [Allen CellTypes Database](http://celltypes.brain-map.org/) for analysis, conversion to NeuroML etc.

**Download example data**

Run:

    sudo apt-get install python-h5py
    sudo pip install pandas
    sudo pip install allensdk

    cd CellTypesDatabase/data
    python download.py

This will download a number of NWB files and display some of the content.


**Analyse data**

Run:

    sudo pip install git+https://github.com/NeuralEnsemble/pyelectro

    python extract_data.py


**Plot data**

    python data_summary.py