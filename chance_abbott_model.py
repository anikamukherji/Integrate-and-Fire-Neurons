
from brian2 import *
from functions import *

eqs = '''
    dV/dt = (V0 - V + Ge_total*(Ve - V) + Gi_total*(Vi - V))/tau_m : volt
    dGe_total/dt = (-Ge_total)/tau_e_model : 1
    dGi_total/dt = (-Gi_total)/tau_i_model : 1
    tau_m : second
    tau_e_model : second
    tau_i_model : second
    Ve : volt
    Vi : volt
    V0 : volt
    '''

syn_eqs = '''
    dG_e/dt = (-G_e)/tau_e : 1 (clock-driven)
    dG_i/dt = (-G_i)/tau_i : 1 (clock-driven)
    dD/dt = (1 - D)/tau_D : 1 (clock-driven)
    tau_e : second
    tau_i : second
    tau_D : second
    d_fast : 1
    strength_e : 1 
    strength_i : 1
         '''
onspike_eqs = '''
    G_e += strength_e*D 
    Ge_total_post += G_e
    G_i += strength_i*D 
    Gi_total_post += G_i
    D = d_fast*D
            '''

model_cell = NeuronGroup(1, eqs, threshold='V>=-0.055*volt', reset='V=-0.058*volt', method='euler')
# reversal potentials for excitatory & inhibitory synapses
model_cell.V = -0.070*volt
model_cell.Ve = 0*volt
model_cell.Vi = -0.090*volt
model_cell.V0 = -0.070*volt 
# time constants
model_cell.tau_m = 0.030*second
model_cell.tau_e_model = 0.002*second
model_cell.tau_i_model = 0.010*second
# total conductances (to be summed from synpases)
model_cell.Ge_total = 0
model_cell.Gi_total = 0

# state monitor
model_cell_mon = StateMonitor(model_cell,'V', record=True)

# figure out how in the world to model LGN input
thalamic_input = PoissonGroup(200, '(50*sin(t*(6*pi)/second))*Hz')
# spike monitor
poisson_mon = SpikeMonitor(thalamic_input)

syn = Synapses(thalamic_input, model_cell, model=syn_eqs, method='euler', on_pre=onspike_eqs)
syn.connect(i=range(0,200), j=[0])

# syanptic conductances
syn.G_e = 0
syn.G_i = 0
syn.tau_e = 0.002*second
syn.tau_i = 0.010*second
# depressive factors
syn.D = 1
syn.tau_D = 0.300*second
# amount of depression
# d  fast depression (plays role in nonlinear dynamics)
syn.d_fast = 0.4
# syanpse strength with afferent 
# may differ when creating DS model
syn.strength_e = 0.009
syn.strength_i = 0.0025

run(2*second)

f, (ax_sin, ax_input, ax_model) = plt.subplots(3, sharex=True, sharey=False)
ax_sin.set_title("Stimulating a Model Cell with Sinusoidal Poisson Firing Rates Using Chance et al. Dynamics")

times = poisson_mon.t/ms
model_times = model_cell_mon.t/ms
seconds = np.arange(0, 2, .001)

ax_sin.plot(50*sin(6*seconds*pi))
ax_sin.set_ylim([0,55])
ax_sin.set_ylabel("Poisson Firing Rate")

ax_input.plot(times, poisson_mon.i, '|k')
ax_input.set_yticks([])

ax_model.plot(model_times, model_cell_mon.V[0])
ax_model.set_ylim([-0.09,-0.04])
ax_model.set_ylabel("Model Cell MP (V)")
ax_model.set_xlabel("Time (ms)")
plt.show()

# visualise_connectivity(syn)
# print(syn._registered_variables)
