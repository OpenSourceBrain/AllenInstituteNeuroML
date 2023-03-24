<p align="center">
  <img src="https://user-images.githubusercontent.com/60441372/130372329-9897167a-83a6-4cc6-a7cf-e1a2137d86cc.png"/>
</p>

# Simulating multiscale models of the mouse visual cortex in NeuroML

These contributions were made as part of Google Summer of Code 2022.

- Organization: [INCF](https://www.incf.org/)
- Mentors: [Padraig Gleeson](https://github.com/pgleeson), [Ankur Sinha](https://github.com/sanjayankur31)
- Contributor: [Anuja Negi](https://github.com/anujanegi)
- Repository: [AllenInstituteNeuroML](https://github.com/OpenSourceBrain/AllenInstituteNeuroML)

## Introduction

Computational models, based on detailed neuroanatomical and electrophysiological data, are heavily used as an aid for understanding the brain. An increasing number of studies have been published over the past, but remain available in simulator-specific formats. 

[NeuroML](https://neuroml.org/) is a standardized data format to describe the biophysics, anatomy, and network architecture of neuronal systems at multiple scales in an XML-based language. 

Hence, to improve accessibility, exchange, and transparency in the research of neuronal models, this project aimed to make neuronal mouse models in the [Allen cell types database](http://celltypes.brain-map.org/) available in a simulator-independent format, using NeuroML.


## Contributions
- [Pull requests opened during GSoC](https://github.com/OpenSourceBrain/AllenInstituteNeuroML/pulls?q=is%3Apr+author%3Aanujanegi+created%3A2022-06-01..2022-09-15+)
- [Issues opened during GSoC](https://github.com/OpenSourceBrain/AllenInstituteNeuroML/issues?q=is%3Aissue+author%3Aanujanegi+created%3A2022-06-01..2022-09-15+)
- [Commit history](https://github.com/OpenSourceBrain/AllenInstituteNeuroML/commits?author=anujanegi)

### Overview

1. GLIF cells: download, run downloaded models in NEURON, parse and generate equivalent NeuroML, simulate and plot comparison graphs, generate and simulate network of GLIF cells.
2. All-active cells: download, run downloaded models in NEURON, parse and generate equivalent NeuroML, simulate and plot comparison graphs.
3. Refactored old code(perisomatic cells) to new version of python and allenSDK.
4. Added github actions for testing all workflows and scripts.
5. Better READMEs!
