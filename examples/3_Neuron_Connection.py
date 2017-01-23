from brian2 import *

start_scope()

weight = 20

eqs = '''
dv/dt = (I-v)/tau : 1 (unless refractory)
I : 1
tau : second
'''
Ginter = NeuronGroup(1, eqs, threshold='v>-40', reset='v = -45',
                refractory=1.5 * ms, method='linear')
Gout = NeuronGroup(1, eqs, threshold='v>-40', reset='v = -45',
                refractory=1.5 * ms, method='linear')
P = PoissonGroup(1, 1000* Hz)

Gout.I = -67
Ginter.I = -67
Ginter.v = -67
Gout.v = -67
Ginter.tau = 5*ms
Gout.tau = 10*ms


S = Synapses(Ginter, Gout, on_pre='v_post += weight')
Sinput = Synapses(P, Ginter, on_pre='v_post += 40')

S.connect(i=0, j=0)
Sinput.connect(i=0, j=0)

Minter = StateMonitor(Ginter, 'v', record=True)
Mout = StateMonitor(Gout, 'v', record=True)
Minput = SpikeMonitor(P)
spikes_inter = SpikeMonitor(Ginter)
spikes_out = SpikeMonitor(Gout)

run(15*ms)

# Three subplots sharing y axis
f, (ax1, ax2, ax3) = plt.subplots(3, sharex=True, sharey=False)

ax1.plot(Minput.t/ms, Minput.i, '.r', label="Poisson Group Spikes")
ax1.set_title('2 Neuron Connection with Poisson Input Group')
ax2.plot(Minter.t/ms, Minter.v[0], '-b', label='Neuron 0')
ax2.vlines(spikes_inter.t/ms, -40, 0, 'gray', lw=3)
ax2.set_ylim([-80,5])
ax3.plot(Mout.t/ms, Mout.v[0], '-g', lw=2, label='Neuron 1')
ax3.vlines(spikes_out.t/ms, -40, 0, 'gray', lw=3)
ax3.set_ylim([-80, 5])

f.subplots_adjust(hspace=0.1)
plt.setp([a.get_xticklabels() for a in f.axes[:-1]], visible=False)

show()
