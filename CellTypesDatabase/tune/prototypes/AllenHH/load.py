
import pyneuroml.pynml

neuroml_file = "AllenHH.cell.nml"

neuroml_files = ["Ca_LVA.channel.nml","CaDynamics.nml","AllenHH.cell.nml"]
    
for neuroml_file in neuroml_files:
    print("=====================================================")
    nml_doc = pyneuroml.pynml.read_neuroml2_file(neuroml_file, 
                                     include_includes=True,
                                     verbose = True,
                                     already_included = [])
    print pyneuroml.pynml.quick_summary(nml_doc)
    
    pyneuroml.pynml.write_neuroml2_file(nml_doc, neuroml_file+".PG")