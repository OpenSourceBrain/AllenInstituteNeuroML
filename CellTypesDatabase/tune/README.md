## Tune data
Some scripts for tuning and optimisation of NeuroML models against the Allen data sets using [pyNeuroML](https://docs.neuroml.org/Userdocs/Software/pyNeuroML.html#pyneuroml).

Run:

    cd CellTypesDatabase/data
    git clone https://github.com/NeuralEnsemble/neurotune.git
    cd neurotune/
    python setup.py install
    rm -rf neurotune
    cd ..

    python tuneAllen.py -izhone  # run one Izhikevich cell with typical values
    python tuneAllen.py  # to see all options

See https://github.com/OpenSourceBrain/AllenInstituteNeuroML/blob/master/CellTypesDatabase/data/summary/README.md for
comparison of these tuned NeuroML 2 cell models to the original Allen data sets.
