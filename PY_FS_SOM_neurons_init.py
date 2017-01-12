from brian2 import *
from functions import *

# facilitating weights are additive 
# depressing weights are multiplicative
# membrane potential & synaptic weights decay exponentially
eqs = '''
    dv/dt = (Vm - v)/tau_m : volt (unless refractory)
    Vm : volt
    tau_m : second
    epsp0 : volt
    epsp : volt

    dD/dt = (1-D)/tau_d : 1 
    dF/dt = (1-F)/tau_f : 1
    tau_f : second
    tau_d : second
    d_rate : 1
    f_rate : 1 
   '''

# PY Neuron Group
PY_group = make_neuron_group(20, 'v>-0.045*volt', 'v=-0.05*volt',
        eqs, 0.005*second, 'linear', name='PY_group')

# initializing PY group variables
PY_group.v = -0.08*volt
PY_group.Vm = -0.08*volt
PY_group.tau_m = 0.015*second
PY_group.epsp0 = 0.005*volt
PY_group.epsp = 0.005*volt
PY_group.tau_d = 0.6*second
PY_group.D = 1
PY_group.d_rate = 0.85

# FS Neuron Group
FS_group = make_neuron_group(10, 'v>-0.045*volt', 'v=-0.05*volt',
        eqs, 0.005*second, 'linear', name='FS_group')

# initializing FS group variables
FS_group.v = -0.065*volt
FS_group.Vm = -0.065*volt
FS_group.tau_m = 0.01*second
FS_group.epsp0 = 0.007*volt
FS_group.epsp = 0.007*volt
FS_group.d_rate = 0.35
FS_group.D = 1
FS_group.tau_d = 0.28*second

# SOM Neuron Group
SOM_group = make_neuron_group(10, 'v>-0.045*volt', 'v=-0.05*volt', 
        eqs, 0.005*second, 'linear', name='SOM_group')

# initializing SOM group variables
SOM_group.v = -0.065*volt
SOM_group.Vm = -0.065*volt
SOM_group.tau_m = 0.02*second
SOM_group.epsp0 = 0.0005*volt
SOM_group.epsp = 0.0005*volt
SOM_group.tau_f = 0.022*second
SOM_group.F = 1
SOM_group.f_rate = 0.2


