Channel information
===================
    
<p style="font-family:arial">Channel information at: T = 34.0 degC, E_rev = 0 mV, [Ca2+] = 0.00043 mM</p>

<table>
    <tr>
<td width="120px">
            <sup><b>NaTa</b><br/>
            <a href="../NaTa.channel.nml">NaTa.channel.nml</a><br/>
            <b>Ion: na</b><br/>
            <i>g = gmax * m<sup>3</sup> * h </i><br/>
            Fast inactivating Na+ current
Modified slightly for Allen Institute cell models from Hay et al. 2011 version:
 - Added Q10 scaling to rate variables 
 - Values for midpoint changed to match mod            
            
Comment from original mod file: 
:Reference :Colbert and Pan 2002</sup>
</td>
<td>
<a href="NaTa.inf.png"><img alt="NaTa steady state" src="NaTa.inf.png" height="220"/></a>
</td>
<td>
<a href="NaTa.tau.png"><img alt="NaTa time course" src="NaTa.tau.png" height="220"/></a>
</td>
</tr>
    <tr>
<td width="120px">
            <sup><b>NaTs</b><br/>
            <a href="../NaTs.channel.nml">NaTs.channel.nml</a><br/>
            <b>Ion: na</b><br/>
            <i>g = gmax * m<sup>3</sup> * h </i><br/>
            Fast inactivating Na+ current. 
Modified slightly for Allen Institute cell models from Hay et al. 2011 version:
 - Added Q10 scaling to rate variables 
 - Values for midpoint changed to match mod 
            
Comment from mod file (NaTs2_t.mod): took the NaTa and shifted both activation/inactivation by 6 mv</sup>
</td>
<td>
<a href="NaTs.inf.png"><img alt="NaTs steady state" src="NaTs.inf.png" height="220"/></a>
</td>
<td>
<a href="NaTs.tau.png"><img alt="NaTs time course" src="NaTs.tau.png" height="220"/></a>
</td>
</tr>
    <tr>
<td width="120px">
            <sup><b>Nap</b><br/>
            <a href="../Nap.channel.nml">Nap.channel.nml</a><br/>
            <b>Ion: na</b><br/>
            <i>g = gmax * m * h </i><br/>
            Persistent Na+ current
Modified for Allen Institute cell models from Hay et al. 2011 version:
- Form of conductance expression changed from: g = gbar * m^3 * h to: g = gbar * minf * h (comment in mod: assuming instantaneous activation as modeled by Magistretti and Alonso)
- Added Q10 scaling to rate variables            

Comment from original mod file: 
:Comment : mtau deduced from text (said to be 6 times faster than for NaTa)
:Comment : so I used the equations from NaT and multiplied by 6
:Reference : Modeled according to kinetics derived from Magistretti and Alonso 1999
:Comment: corrected rates using q10 = 2.3, target temperature 34, orginal 21</sup>
</td>
<td>
<a href="Nap.inf.png"><img alt="Nap steady state" src="Nap.inf.png" height="220"/></a>
</td>
<td>
<a href="Nap.tau.png"><img alt="Nap time course" src="Nap.tau.png" height="220"/></a>
</td>
</tr>
    <tr>
<td width="120px">
            <sup><b>Kd</b><br/>
            <a href="../Kd.channel.nml">Kd.channel.nml</a><br/>
            <b>Ion: k</b><br/>
            <i>g = gmax * m * h </i><br/>
            Kd current
            
Comment from original mod file: 
Based on Kd model of Foust et al. (2011)</sup>
</td>
<td>
<a href="Kd.inf.png"><img alt="Kd steady state" src="Kd.inf.png" height="220"/></a>
</td>
<td>
<a href="Kd.tau.png"><img alt="Kd time course" src="Kd.tau.png" height="220"/></a>
</td>
</tr>
    <tr>
<td width="120px">
            <sup><b>K_P</b><br/>
            <a href="../K_P.channel.nml">K_P.channel.nml</a><br/>
            <b>Ion: k</b><br/>
            <i>g = gmax * m<sup>2</sup> * h </i><br/>
            Slow inactivating K+ current
Modified slightly for Allen Institute cell models from Hay et al. 2011 version:
 - Added Q10 scaling to rate variables 
 - Equations for tau/inf updated to match mod
            
Comment from original mod file: 
:Comment : The persistent component of the K current
:Reference : :		Voltage-gated K+ channels in layer 5 neocortical pyramidal neurones from young rats:subtypes and gradients,Korngreen and Sakmann, J. Physiology, 2000
:Comment : shifted -10 mv to correct for junction potential
:Comment: corrected rates using q10 = 2.3, target temperature 34, orginal 21</sup>
</td>
<td>
<a href="K_P.inf.png"><img alt="K_P steady state" src="K_P.inf.png" height="220"/></a>
</td>
<td>
<a href="K_P.tau.png"><img alt="K_P time course" src="K_P.tau.png" height="220"/></a>
</td>
</tr>
    <tr>
<td width="120px">
            <sup><b>K_T</b><br/>
            <a href="../K_T.channel.nml">K_T.channel.nml</a><br/>
            <b>Ion: k</b><br/>
            <i>g = gmax * m<sup>4</sup> * h </i><br/>
            Fast inactivating K+ current
Modified slightly for Allen Institute cell models from Hay et al. 2011 version:
 - Added Q10 scaling to rate variables 
 - Equations for tau/inf updated to match mod
            
Comment from original mod file: 
:Comment : The transient component of the K current
:Reference : :		Voltage-gated K+ channels in layer 5 neocortical pyramidal neurones from young rats:subtypes and gradients,Korngreen and Sakmann, J. Physiology, 2000
:Comment : shifted -10 mv to correct for junction potential
:Comment: corrected rates using q10 = 2.3, target temperature 34, orginal 21</sup>
</td>
<td>
<a href="K_T.inf.png"><img alt="K_T steady state" src="K_T.inf.png" height="220"/></a>
</td>
<td>
<a href="K_T.tau.png"><img alt="K_T time course" src="K_T.tau.png" height="220"/></a>
</td>
</tr>
    <tr>
<td width="120px">
            <sup><b>Kv3_1</b><br/>
            <a href="../Kv3_1.channel.nml">Kv3_1.channel.nml</a><br/>
            <b>Ion: k</b><br/>
            <i>g = gmax * m </i><br/>
            Fast, non inactivating K+ current (Kv3-like)
            
Comment from original mod file: 
:Reference : :		Characterization of a Shaw-related potassium channel family in rat brain, The EMBO Journal, vol.11, no.7,2473-2486 (1992)</sup>
</td>
<td>
<a href="Kv3_1.inf.png"><img alt="Kv3_1 steady state" src="Kv3_1.inf.png" height="220"/></a>
</td>
<td>
<a href="Kv3_1.tau.png"><img alt="Kv3_1 time course" src="Kv3_1.tau.png" height="220"/></a>
</td>
</tr>
    <tr>
<td width="120px">
            <sup><b>Kv2like</b><br/>
            <a href="../Kv2like.channel.nml">Kv2like.channel.nml</a><br/>
            <b>Ion: k</b><br/>
            <i>g = gmax * m<sup>2</sup> </i><br/>
            Kv2-like channel
            
Comment from original mod file: 
: Kv2-like channel
: Adapted from model implemented in Keren et al. 2005
: Adjusted parameters to be similar to guangxitoxin-sensitive current in mouse CA1 pyramids from Liu and Bean 2014</sup>
</td>
<td>
<a href="Kv2like.inf.png"><img alt="Kv2like steady state" src="Kv2like.inf.png" height="220"/></a>
</td>
<td>
<a href="Kv2like.tau.png"><img alt="Kv2like time course" src="Kv2like.tau.png" height="220"/></a>
</td>
</tr>
    <tr>
<td width="120px">
            <sup><b>Im</b><br/>
            <a href="../Im.channel.nml">Im.channel.nml</a><br/>
            <b>Ion: k</b><br/>
            <i>g = gmax * m </i><br/>
            Muscarinic K+ current
Modified slightly for Allen Institute cell models from Hay et al. 2011 version:
 - Added Q10 scaling to rate variables 
            
Comment from original mod file: 
:Reference : :		Adams et al. 1982 - M-currents and other potassium currents in bullfrog sympathetic neurones
:Comment: corrected rates using q10 = 2.3, target temperature 34, orginal 21</sup>
</td>
<td>
<a href="Im.inf.png"><img alt="Im steady state" src="Im.inf.png" height="220"/></a>
</td>
<td>
<a href="Im.tau.png"><img alt="Im time course" src="Im.tau.png" height="220"/></a>
</td>
</tr>
    <tr>
<td width="120px">
            <sup><b>Im_v2</b><br/>
            <a href="../Im_v2.channel.nml">Im_v2.channel.nml</a><br/>
            <b>Ion: k</b><br/>
            <i>g = gmax * m </i><br/>
            Im current
            
Comment from original mod file: 
Based on Im model of Vervaeke et al. (2006)</sup>
</td>
<td>
<a href="Im_v2.inf.png"><img alt="Im_v2 steady state" src="Im_v2.inf.png" height="220"/></a>
</td>
<td>
<a href="Im_v2.tau.png"><img alt="Im_v2 time course" src="Im_v2.tau.png" height="220"/></a>
</td>
</tr>
    <tr>
<td width="120px">
            <sup><b>SK</b><br/>
            <a href="../SK.channel.nml">SK.channel.nml</a><br/>
            <b>Ion: k</b><br/>
            <i>g = gmax * z </i><br/>
            Small-conductance, Ca2+ activated K+ current
            
Comment from original mod file: 
: SK-type calcium-activated potassium current
: Reference : Kohler et al. 1996</sup>
</td>
<td>
<a href="SK.inf.png"><img alt="SK steady state" src="SK.inf.png" height="220"/></a>
</td>
<td>
<a href="SK.tau.png"><img alt="SK time course" src="SK.tau.png" height="220"/></a>
</td>
</tr>
    <tr>
<td width="120px">
            <sup><b>Ca_LVA</b><br/>
            <a href="../Ca_LVA.channel.nml">Ca_LVA.channel.nml</a><br/>
            <b>Ion: ca</b><br/>
            <i>g = gmax * m<sup>2</sup> * h </i><br/>
            Low voltage activated Ca2+ current
Modified slightly for Allen Institute cell models from Hay et al. 2011 version:
 - Added Q10 scaling to rate variables 
            
Comment from original mod file: 
Note: mtau is an approximation from the plots
:Reference : :		Avery and Johnston 1996, tau from Randall 1997
:Comment: shifted by -10 mv to correct for junction potential
:Comment: corrected rates using q10 = 2.3, target temperature 34, orginal 21</sup>
</td>
<td>
<a href="Ca_LVA.inf.png"><img alt="Ca_LVA steady state" src="Ca_LVA.inf.png" height="220"/></a>
</td>
<td>
<a href="Ca_LVA.tau.png"><img alt="Ca_LVA time course" src="Ca_LVA.tau.png" height="220"/></a>
</td>
</tr>
    <tr>
<td width="120px">
            <sup><b>Ca_HVA</b><br/>
            <a href="../Ca_HVA.channel.nml">Ca_HVA.channel.nml</a><br/>
            <b>Ion: ca</b><br/>
            <i>g = gmax * m<sup>2</sup> * h </i><br/>
            High voltage activated Ca2+ current. 
NOTE: Most Allen Institute channel models from Hay et al. 2011 use Q10 scaling. This one doesn't...
See https://github.com/OpenSourceBrain/AllenInstituteNeuroML/issues/2
            
Comment from original mod file: 
Reuveni, Friedman, Amitai, and Gutnick, J.Neurosci. 1993</sup>
</td>
<td>
<a href="Ca_HVA.inf.png"><img alt="Ca_HVA steady state" src="Ca_HVA.inf.png" height="220"/></a>
</td>
<td>
<a href="Ca_HVA.tau.png"><img alt="Ca_HVA time course" src="Ca_HVA.tau.png" height="220"/></a>
</td>
</tr>
    <tr>
<td width="120px">
            <sup><b>Ih</b><br/>
            <a href="../Ih.channel.nml">Ih.channel.nml</a><br/>
            <b>Ion: hcn</b><br/>
            <i>g = gmax * m </i><br/>
            Non-specific cation current
            
Comment from original mod file: 
Reference : :		Kole,Hallermann,and Stuart, J. Neurosci. 2006</sup>
</td>
<td>
<a href="Ih.inf.png"><img alt="Ih steady state" src="Ih.inf.png" height="220"/></a>
</td>
<td>
<a href="Ih.tau.png"><img alt="Ih time course" src="Ih.tau.png" height="220"/></a>
</td>
</tr>
</table>

