from brian2 import *
from brian2.units import *

start_scope()

w_e = 0.013 * volt
w_i = -0.017 * volt

eqs = '''
dv/dt = (Vm - v)/tau : volt (unless refractory)
Vm : volt
tau : second
'''

# excitatory and inhibitory poisson input groups
Pi = PoissonGroup(1, 600*Hz)
Pe = PoissonGroup(1,1000*Hz)
Ge = NeuronGroup(1, eqs, threshold='v>-.040 *volt',
                 reset='v=-.045*volt', refractory=.001*second,
                 method='linear')
Gi = NeuronGroup(1, eqs, threshold='v>-.040 *volt',
                 reset='v=-.045*volt', refractory=.001*second,
                 method='linear')

Gout = NeuronGroup(1, eqs, threshold='v>-.040 *volt',
                 reset='v=-.045*volt', refractory=0.001*second,
                 method='linear')

# initialize vars/starting states
Ge.Vm = -.067 * volt
Gi.Vm = -.067 * volt
Gout.Vm = -.067 * volt
Ge.v = -.067 * volt
Gi.v = -.067 * volt
Gout.v= -.067 * volt
Ge.tau = .015 * second
Gi.tau = .015 * second
Gout.tau = .015 * second

Se1 = Synapses(Pe, Ge, on_pre='v_post += 0.01 * volt')
Si1 = Synapses(Pi, Gi, on_pre = 'v_post += 0.01 * volt')
Se2 = Synapses(Ge, Gout, on_pre = 'v_post += w_e')
Si2 = Synapses(Gi, Gout, on_pre = 'v_post += w_i')

# connect the cells using the synapses created above
Si1.connect(i=0, j=0)
Si2.connect(i=0, j=0)
Se1.connect(i=0, j=0)
Se2.connect(i=0, j=0)

# record all of the different cells
S_Pi = SpikeMonitor(Pi)
S_Pe = SpikeMonitor(Pe)
M_Ge = StateMonitor(Ge, 'v', record=True)
M_Gi = StateMonitor(Gi, 'v', record=True)
S_Ge = SpikeMonitor(Ge)
S_Gi = SpikeMonitor(Gi)
M_Gout = StateMonitor(Gout, 'v', record=True)
S_Gout = SpikeMonitor(Gout)

run(100*ms)

f, (ax1, ax2, ax3) = plt.subplots(3, sharex=True, sharey=False)

ax1.plot(S_Pi.t / ms, S_Pi.i, '|r', label="Poisson Group Spikes")
ax1.plot(S_Pe.t / ms, S_Pe.i, '|b', label="Poisson Group Spikes")
ax1.set_ylim([-.005, 0.005])
ax1.set_yticks([])
ax1.set_title('5 Neuron Connection with Poisson Input Group')
ax2.plot(M_Ge.t / ms, M_Ge.v[0], '-b', label='Excitatory Interneuron')
ax2.plot(M_Gi.t / ms, M_Gi.v[0], '-r', label= 'Inhibitory Interneuron')
ax2.vlines(S_Ge.t / ms, -.040, 0, 'gray', lw=3)
ax2.vlines(S_Gi.t / ms, -.040, 0, 'gray', lw=3)
ax2.set_ylim([-.080, .015])
ax3.plot(M_Gout.t / ms, M_Gout.v[0], '-g', lw=2, label='Output Neuron')
ax3.vlines(S_Gout.t / ms, -.040, 0, 'gray', lw=3)
ax3.set_ylim([-.10, .005])
ax3.set_xlabel("Time (s)")
ax3.set_ylabel("MP (v)")
ax2.set_ylabel("MP (v)")

f.subplots_adjust(hspace=0.1)
plt.setp([a.get_xticklabels() for a in f.axes[:-1]], visible=False)

show()
