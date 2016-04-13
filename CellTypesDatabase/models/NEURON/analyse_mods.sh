#Ca_HVA.mod Ca_LVA.mod Ih.mod Im.mod Im_v2.mod K_P.mod K_T.mod Kd.mod Kv2like.mod Kv3_1.mod NaTa.mod NaTs.mod NaV.mod Nap.mod SK.mod

pynml-modchananalysis Ca_LVA -stepV 5 -temperature [26,34]
pynml-modchananalysis Ca_HVA -stepV 5 -temperature [26,34]

pynml-modchananalysis NaTa -stepV 5 -temperature [26,34]
pynml-modchananalysis NaTs -stepV 5 -temperature [26,34]
pynml-modchananalysis Nap -stepV 5 -temperature [26,34] -dt 0.1 -duration 25000

pynml-modchananalysis K_P -stepV 5 -temperature [26,34]
pynml-modchananalysis K_T -stepV 5 -temperature [26,34]
pynml-modchananalysis Kd -stepV 5 -temperature [26,34]  -duration 50000 -dt 0.1
pynml-modchananalysis Kv2like -stepV 5 -temperature [26,34] -dt 0.05 -duration 50000
pynml-modchananalysis Kv3_1 -stepV 5 -temperature [26,34]


pynml-modchananalysis Ih -stepV 5 -temperature [26,34]
pynml-modchananalysis Im -stepV 5 -temperature [26,34]
pynml-modchananalysis Im_v2 -stepV 5 -temperature [26,34]

pynml-modchananalysis SK -stepV 5 -temperature [26,34] -caConc 0.00043

# Kinetic scheme based...
#pynml-modchananalysis NaV -stepV 5 -temperature [26,34]
