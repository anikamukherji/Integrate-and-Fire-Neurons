from brian2 import *
from brian2.units import *

# facilitating weights are additive so f_rate is in volts
# depressing weights are multiplicative so d_rate is unit-less
# membrane potential & synaptic weights decay exponentially

eqs = '''
    dv/dt = (Vm - v)/tau_m : volt (unless refractory)
    Vm : volt
    tau_m : second
    epsp0 : volt

    dw_d/dt = (-w_d)/tau_d : volt 
    tau_d : second
    d_rate : 1

    dw_f/dt = (-w_f)/tau_f : volt 
    tau_f : second
    f_rate : volt       
   '''

# Poisson input with firing rate that is sinusoidal
poisson_input = PoissonGroup(20,rates='20*sin(t/second*2*pi*3)*Hz')

# PY Neuron Group
PY_group = NeuronGroup(N=20, threshold='v>-0.045*volt', reset='v=-0.05*volt',
        model=eqs, refractory=0.005*second, method='linear')

# initializing PY group variables
PY_group.v = -0.08*volt
PY_group.Vm = -0.08*volt
PY_group.tau_m = 0.02*second
PY_group.epsp0 = 0.005*volt
PY_group.w_d = 0.00*volt
PY_group.tau_d = 0.006*second
PY_group.d_rate = 0.8

# FS Neuron Group
FS_group = NeuronGroup(N=10, threshold='v>-0.045*volt', reset='v=-0.05*volt',
        model=eqs, refractory=0.005*second, method='linear')

# initializing FS group variables
FS_group.v = -0.065*volt
FS_group.Vm = -0.065*volt
FS_group.tau_m = 0.0075*second
FS_group.epsp0 = 0.007*volt
FS_group.w_d = 0.00*volt
FS_group.tau_d = 0.003*second
FS_group.d_rate = 0.6

# SOM Neuron Group
SOM_group = NeuronGroup(N=10, threshold='v>-0.045*volt', reset='v=-0.05*volt'           , model=eqs, refractory=0.005*second, method='linear')

# initializing SOM group variables
SOM_group.v = -0.065*volt
SOM_group.Vm = -0.065*volt
SOM_group.tau_m = 0.02*second
SOM_group.epsp0 = 0.0005*volt
SOM_group.w_f = 0.00*volt
SOM_group.tau_f = 0.005*second
SOM_group.f_rate = 0.003*volt


# create synapses between poisson input group and the others

S_P_PY = Synapses(poisson_input, PY_group, on_pre='''
                                                v_post += (epsp0 - w_d) 
                                                w_d *= d_rate
                                                ''')

S_P_FS = Synapses(poisson_input, FS_group, on_pre= '''
                                                v_post += (epsp0 - w_d)
                                                w_d *= d_rate
                                                ''')

S_P_SOM = Synapses(poisson_input, SOM_group, on_pre='''
                                                v_post += (epsp0 + w_f)
                                                w_f += f_rate                                                       ''')

# connect the neurons (I think this will connect everything together)

S_P_PY.connect()
S_P_FS.connect()
S_P_SOM.connect()

# record membrane voltages and spikes

mon_poisson_input = SpikeMonitor(poisson_input)
mon_PY = StateMonitor(PY_group, 'v', record=True)
spikes_PY = SpikeMonitor(PY_group)
mon_FS = StateMonitor(FS_group, 'v', record=True)
spikes_FS = SpikeMonitor(FS_group)
mon_SOM = StateMonitor(SOM_group, 'v', record=True)
spikes_SOM = SpikeMonitor(SOM_group)
rate_mon = PopulationRateMonitor(poisson_input)

run(1*second)

# print('PY Neuron 1 Voltages= ', mon_PY.v[0][0:20])
# print('FS Neuron 1 Voltages= ', mon_FS.v[0][0:20])
# print('SOM Neuron 1 Voltages=', mon_SOM.v[0][0:20])


# !!!!!PLOT THINGS!!!!!!
f, (axinput , axPY, axFS, axSOM) = plt.subplots(4, sharex=True, sharey= False)

axinput.plot(mon_poisson_input.t/ms, mon_poisson_input.i, '|k')
axinput.set_yticks([])
axinput.set_title("Poisson Inputs into PY, FS and SOM neurons")

axPY.plot(mon_PY.t/ms, mon_PY.v[0], 'g')
axPY.set_ylabel('PY Neurons MP (v)')
axPY.vlines(spikes_PY.t/ms, -0.040, 0, 'gray', lw=3)
axPY.set_ylim([-0.09, 0.01])

axFS.set_ylabel("FS Neurons MP (v)")
axFS.plot(mon_FS.t/ms, mon_FS.v[0], 'b')
axFS.vlines(spikes_FS.t/ms, -0.040, 0, 'gray', lw=3)
axFS.set_ylim([-0.09, 0.01])

axSOM.plot(mon_SOM.t/ms, mon_SOM.v[0], 'purple')
axSOM.vlines(spikes_SOM.t/ms, -0.040, 0, 'gray', lw=3)
axSOM.set_xlabel("Time (s)")
axSOM.set_ylabel("SOM Neurons MP (v)")
axSOM.set_ylim([-0.09, 0.01])

f.subplots_adjust(hspace=0.1)
plt.show()

# function from brian to visualize synaptic connections of a synapse object

def visualise_connectivity(S):
    Ns = len(S.source)
    Nt = len(S.target)
    figure(figsize=(10, 4))
    subplot(121)
    plot(zeros(Ns), arange(Ns), 'ok', ms=10)
    plot(ones(Nt), arange(Nt), 'ok', ms=10)
    for i, j in zip(S.i, S.j):
        plot([0, 1], [i, j], '-k')
    xticks([0, 1], ['Source', 'Target'])
    ylabel('Neuron index')
    xlim(-0.1, 1.1)
    ylim(-1, max(Ns, Nt))
    subplot(122)
    plot(S.i, S.j, 'ok')
    xlim(-1, Ns)
    ylim(-1, Nt)
    xlabel('Source neuron index')
    ylabel('Target neuron index')
    show()

