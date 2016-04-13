
import matplotlib.pyplot as pylab
import os.path


chans = ['K_T', 'K_P', 'NaTa', 'Nap', 'NaTs', 'Ih', 'Ca_LVA', 'Ca_HVA', 'SKv3_1']
chans = ['Ca_LVA', 'NaTa']
chans = ['K_P', 'K_T']
chans = ['Kv3_1', 'SK']
chans = ['Nap']
chans = ['Ih', 'Im']
chans = ['Im','Im_v2']
chans = ['Kd']
chans = ['Kv2like']

problematic = []

gates = ['m', 'h', 'z']
#gates = ['h']

temperatures = [26]
temperatures = [26,34]

for temperature in temperatures:

    for channel_id in chans:

        vramp_lems_file  = '%s.rampV.lems.%s.dat'%(channel_id, temperature)

        ts = []
        volts = []
        for line in open(vramp_lems_file):
            ts.append(float(line.split()[0])*1000)
            volts.append(float(line.split()[1])*1000)

        fig = pylab.figure()
        fig.canvas.set_window_title("Time Course(s) of activation variables of %s at %sdegC"%(channel_id, temperature))

        pylab.xlabel('Membrane potential (mV)')
        pylab.ylabel('Time Course - tau (ms)')
        pylab.grid('on')

        for gate in gates:

            tau_lems_file  = '%s.%s.tau.lems.%s.dat'%(channel_id, gate, temperature)

            if os.path.isfile(tau_lems_file):
                taus = []
                for line in open(tau_lems_file):
                    ts.append(float(line.split()[0])*1000)
                    taus.append(float(line.split()[1])*1000)

                pylab.plot(volts, taus, linestyle='-', linewidth=2, label="LEMS %s %s tau"%(channel_id, gate))

                tau_mod_file  = '../NEURON/%s.%s.tau.%s.dat'%(channel_id, gate, temperature)
                vs = []
                taus = []
                for line in open(tau_mod_file):
                    vs.append(float(line.split()[0]))
                    taus.append(float(line.split()[1]))

                pylab.plot(vs, taus, '--x', label="Mod %s %s tau"%(channel_id, gate))


        pylab.legend()


        fig = pylab.figure()
        fig.canvas.set_window_title("Steady state(s) of activation variables of %s at %sdegC"%(channel_id, temperature))

        pylab.xlabel('Membrane potential (mV)')
        pylab.ylabel('Steady state (inf)')
        pylab.grid('on')

        for gate in gates:

            inf_lems_file  = '%s.%s.inf.lems.%s.dat'%(channel_id, gate, temperature)

            if os.path.isfile(inf_lems_file):
                infs = []
                for line in open(inf_lems_file):
                    infs.append(float(line.split()[1]))

                pylab.plot(volts, infs, linestyle='-', linewidth=2, label="LEMS %s %s inf"%(channel_id, gate))

                inf_mod_file  = '../NEURON/%s.%s.inf.%s.dat'%(channel_id, gate,temperature)
                vs = []
                infs = []
                for line in open(inf_mod_file):
                    vs.append(float(line.split()[0]))
                    infs.append(float(line.split()[1]))

                pylab.plot(vs, infs, '--x', label="Mod %s %s inf"%(channel_id, gate))

        pylab.legend()

pylab.show()
