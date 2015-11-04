Channel information
===================
    
<p style="font-family:arial">Channel information at: T = 26.0 degC, E_rev = 0 mV, [Ca2+] = 0.00043 mM</p>

<table>
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
</table>

