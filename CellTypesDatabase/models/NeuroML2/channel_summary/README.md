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
</table>

