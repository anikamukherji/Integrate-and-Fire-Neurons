from brian2 import *

start_scope()


eqs = '''
dv/dt = (Vm - v)/tau_m : volt (unless refractory)
Vm : volt
tau_m : second

dw_d/dt = (-w_d)/tau_d : volt
epsp0 : volt
tau_d : second
f_max : volt
d_max : volt
'''

P = PoissonGroup(100, rates='20+20*sin(t*pi*6)')
G = NeuronGroup(1, eqs, threshold='v>-0.04*volt', reset='v=-0.045*volt',
                refractory=0.001*second, method='linear')

# initialize voltages

G.v = -0.067*volt
G.Vm = -0.067*volt

# initialize membrane constants

G.tau_m = 0.01*second
G.tau_d = 0.013*second

# initializing weights & baseline weights
# w_d will decay to 0

G.w_d = 0*volt
G.epsp0 = 0.008*volt
G.d_max = -0.005*volt

# add synapses
# add depressing weights at presynaptic spike
# when w_d == d_max, no more depression will occur (d_max - w_d = 0)
# if |d_max| > epsp0, (and the synapse is only depressing) or if
#   tau_m is very large, the synapse may turn inhibitory

S = Synapses(P, G, on_pre=''' v_post += (epsp0 + w_d)
                            w_d += (d_max - w_d)/2
                            ''')
S.connect()

# record spikes & MP

M_G = StateMonitor(G, 'v', record=True)
S_G = SpikeMonitor(G)
S_w_d = StateMonitor(G, 'w_d', record=True)
S_P = SpikeMonitor(P)

run(100*ms)

# print(S_w_d.w_d)
print(0.005*volt + S_w_d.w_d)

# plot lots of things

f, (ax1, axw, ax2) = plt.subplots(3, sharex=True, sharey=False)

ax1.plot(S_P.t/ms, S_P.i, '|r')
ax1.set_ylim([-0.005,0.005])
ax1.set_yticks([])
ax1.set_title("Depressing Synapse")
axw.plot(S_w_d.t/ms, 0.005*volt + S_w_d.w_d[0], 'g')
axw.set_ylim([0.0, 0.01])
ax2.set_ylabel("EPSP (v)")
ax2.plot(M_G.t/ms, M_G.v[0], 'b')
ax2.vlines(S_G.t/ms, -0.040, 0, 'gray', lw=3)
ax2.set_ylim([-0.08, 0.015])
ax2.set_xlabel("Time (ms)")
ax2.set_ylabel("MP (v)")
f.subplots_adjust(hspace=0.1)
plt.show()
