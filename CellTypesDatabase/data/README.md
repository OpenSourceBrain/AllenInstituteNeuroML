
### Data import

Some scripts for pulling data from the [Allen CellTypes Database](http://celltypes.brain-map.org/) for analysis, conversion to NeuroML etc.

See also [test script here](https://github.com/OpenSourceBrain/AllenInstituteNeuroML/blob/master/.github/workflows/non-omv.yml) which loads appropriate libraries, and runs this sequence.

**Download example data**

Run:

    pip install allensdk

    cd CellTypesDatabase/data
    
    python download.py -test # run short test to make sure all libraries installed
    python download.py  # download all

This will download a number of NWB files and display some of the content.


**Analyse data**

Run:

    pip install pyelectro

    python extract_data.py -test # run a quick test
    python extract_data.py


**Plot data**

    python data_summary.py
