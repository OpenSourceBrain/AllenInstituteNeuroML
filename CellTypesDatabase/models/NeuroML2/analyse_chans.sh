
pynml-channelanalysis Ca_LVA.channel.nml Ca_HVA.channel.nml \
                      NaTa.channel.nml NaTs.channel.nml Nap.channel.nml\
                      Kd.channel.nml K_P.channel.nml K_T.channel.nml Kv3_1.channel.nml Kv2like.channel.nml \
                      Ih.channel.nml Im.channel.nml Im_v2.channel.nml \
                      SK.channel.nml \
                      -caConc 0.00043 -temperature 26 -datSuffix '.26' -minV -100 -maxV 60 -html -md

pynml-channelanalysis Ca_LVA.channel.nml Ca_HVA.channel.nml \
                      NaTa.channel.nml NaTs.channel.nml Nap.channel.nml\
                      Kd.channel.nml K_P.channel.nml K_T.channel.nml Kv3_1.channel.nml Kv2like.channel.nml \
                      Ih.channel.nml Im.channel.nml Im_v2.channel.nml \
                      SK.channel.nml \
                      -caConc 0.00043 -temperature 34 -datSuffix '.34' -minV -100 -maxV 60 -html -md


#Ih.channel.nml \
#NaTa_t.channel.nml  Nap_Et2.channel.nml  \Ca_HVA.channel.nml
#K_Tst.channel.nml  KdShu2007.channel.nml \
#                      SKv3_1.channel.nml SK_E2.channel.nml \
                      

# Im.channel.nml  problematic...
