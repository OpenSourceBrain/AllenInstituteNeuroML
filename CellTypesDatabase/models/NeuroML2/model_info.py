
import sys
import os
import glob

import numpy as np

from pyneuroml import pynml

from pyneuroml.analysis.ChannelDensityPlot import generate_channel_density_plots


if __name__ == '__main__':
    
    all_cell_files = glob.glob("Cell*.cell.nml")[:3]
    all_cell_files = glob.glob("Cell*.cell.nml")
    
    #os.chdir('cell_summary')
    
    vals = {}
    
    for cell_file in all_cell_files:
        
        print("Loading %s"%cell_file)
        
        
        sgv_files, all_info = generate_channel_density_plots(cell_file, text_densities=True, passives_erevs=True,target_directory='cell_summary')
        
        print("   Generate file: %s"%sgv_files)
        
        print all_info.keys()
        info = all_info[cell_file.split('.')[0]]
        for k in info:
            
            val = info[k] if not isinstance(info[k], dict) else info[k]['max']
            if val:
                
                if not k in vals:
                    vals[k]=[]
                vals[k].append(float(val))
        
    print("\n====================================")
    vv = vals.keys()
    vv = sorted(vv)
    for v in vv:
        factor = 0.0001
        if v.startswith('e'): factor = 1000.0
        if v.startswith('specific_capacitance'): factor = 100.0
        n = np.array([x*factor for x in vals[v]])
        print("%s: \t mean %s (%s -> %s) "%(v, np.mean(n), np.min(n), np.max(n)))
        
        
