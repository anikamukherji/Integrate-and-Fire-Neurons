from brian2 import *
from brian2.units import *

start_scope()


eqs = '''
dv/dt = (Vm - v)/tau_m : volt (unless refractory)
Vm : volt
tau_m : second

dw_f/dt = (-w_f)/tau_f : volt
dw_d/dt = (-w_d)/tau_d : volt
w_d : volt
w_f : volt
epsp0 : volt
tau_f : second
tau_d : second
'''

P = SpikeGeneratorGroup(1, [0, 0, 0, 0], [1*ms, 2*ms, 3*ms, 8*ms])
G = NeuronGroup(1, eqs, threshold='v>-0.04*volt', reset='v=-0.045*volt',
                refractory=0.001*second, method='linear')

# initialize voltages

G.v = -0.067*volt
G.Vm = -0.067*volt

# initialize membrane constants

G.tau_m = 0.01*second
G.tau_f = 0.003*volt
G.tau_d = 0.008*second

# initializing weights & baseline weights

G.w_d = 0*volt
G.w_f = 0*volt
G.epsp0 = 0.003*volt
G.F = 0.004*volt
G.D = 0.002*volt

# add synapses
# add both facilitating & depressing weights at presynaptic spike

S = Synapses(P, G, on_pre=''' v_post += (epsp0 + w_f + w_d)
                            D = 0.003*volt
                            w_f += F
                            w_d -= D
                            F = (w_f - epsp0)/2
                            D = (-w_d - epsp0)/1.2
                            ''')
S.connect(i=0,j=0)

# record spikes & MP

M_G = StateMonitor(G, 'v', record=True)
S_G = SpikeMonitor(G)
S_w_f = StateMonitor(G, 'w_f', record=True)
S_w_d = StateMonitor(G, 'w_d', record=True)
S_P = SpikeMonitor(P)

run(10*ms)

print(S_w_f.w_f)
print(S_w_d.w_d)
print(S_w_d.w_d + S_w_f.w_f)
f, (ax1, axw, ax2) = plt.subplots(3, sharex=True, sharey=False)

ax1.plot(S_P.t/ms, S_P.i, '|r')
ax1.set_ylim([-0.005,0.005])
ax1.set_yticks([])
ax1.set_title("2 layers with Complex STP")
axw.plot(S_w_f.t/ms, S_w_f.w_f[0] + S_w_d.w_d[0], 'g')
axw.set_ylim([0.0052, 0.018])
ax2.plot(M_G.t/ms, M_G.v[0], 'b')
ax2.vlines(S_G.t/ms, -0.040, 0, 'gray', lw=3)
ax2.set_ylim([-0.08, 0.015])
ax2.set_xlabel("Time (s)")
ax2.set_ylabel("MP (v)")
f.subplots_adjust(hspace=0.1)
plt.show()
