from brian2 import *
from brian2.units import *

eqs = '''
    dv/dt = (Vm - v)/tau_m : volt
    Vm : volt
    tau_m : second
    epsp0 : volt

    dw_d/dt = (-w_d)/tau_d : volt
    d_max : volt
    tau_d : second
    d_rate : 1

    dw_f/dt = (-w_f)/tau_f : volt
    f_max : volt
    tau_f : second
    r_rate : second
   '''

# Poisson group input with sinusoidal firing, max of 200 Hz, period of 10

poisson_input = PoissonGroup(100)
poisson_input.rates = TimedArray(200*sin(pi*t/5))

PY_group = NeuronGroup(N=20, threshold='v>-0.05*volt', model=eqs, 
        reset='v=-0.045*volt',
        refractory=0.001*second, method='linear')

# initializing PY group variables
PY_group.v = -0.067*volt
PY_group.Vm = -0.067*volt
PY_group.tau_m = 0.01*second
PY_group.epsp0 = 0.003*volt
PY_group.d_max = 0.0025*volt
PY_group.w_d = 0.00*volt
PY_group.d_rate = 0.01

FS_group = NeuronGroup(N=10, threshold='v>-0.04*volt', reset='v=-0.045*volt',
        model=eqs, refractory=0.001*second, method='linear')

# initializing FS group variables
FS_group.v = -0.067*volt
FS_group.Vm = -0.067*volt
FS_group.tau_m = 0.01*second
FS_group.epsp0 = 0.009*volt
FS_group.d_max = 0.0085*volt
FS_group.w_d = 0.00*volt
FS_group.d_rate = 0.005

SOM_group = NeuronGroup(N=10, threshold='v>-0.04*volt', reset='v=-0.045*volt',
        model=eqs, refractory=0.001*second, method='linear')

# initializing SOM group variables
SOM_group.v = -0.067*volt
SOM_group.Vm = -0.067*volt
SOM_group.tau_m = 0.01*second
SOM_group.epsp0 = 0.003*volt
SOM_group.f_max = 0.0025*volt
SOM_group.w_f = 0.00*volt
SOM_group.f_rate = 0.007


# create synapses between poisson input group and the others

S_P_PY = Synapses(poisson_input, PY_group, on_pre='''
                                                v_post += (epsp0 - w_d)
                                                w_d += (d_max - w_d)/f_rate
                                                ''')

S_P_FS = Synapses(poisson_input, FS_group, on_pre= '''
                                                v_post += (epsp0 - w_d)
                                                w_d += (d_max - w_d)/d_rate
                                                ''')

S_P_SOM = Synapses(poisson_input, SOM_group, on_pre='''
                                                v_post += (epsp0 - w_f)
                                                w_f += (f_max - w_f)/f_rate
                                                ''')

# connect the neurons (I think this will connect everything together)

S_P_PY.connect()
S_P_FS.connect()
S_P_SOM.connect()



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

