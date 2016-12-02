from brian2 import *

def make_poisson_input(N, firing_rates):
    '''
    Makes poisson input group with N neurons 
    firing_rates can be a function formatted as a string or 
    a number with units Hz
    '''

    poisson_input = PoissonGroup(N, rates=firing_rates)
    return poisson_input

def make_spike_generator(N, time_array):
    '''
    Returns SpikeGeneratorGroup with N neurons that fires 
    according to times specified in array (so must have units second)
    '''
    gen = SpikeGeneratorGroup(N, [0]*len(time_array), times=time_array)
    return gen

def make_neuron_group(N, thresh, reset_value, eq_model, refract,
        integration_method):
    '''
    Makes neuron group with N neurons
    All other parameters should be formatted as strings
    Ex. thresh='v>-0.04*volt', reset_value='v=-0.05*volt'
    '''

    neuron_group = NeuronGroup(N, threshold=thresh, reset=reset_value,
            model=eq_model, refractory=refract, method=integration_method)
    return neuron_group

def make_synapse(group_1, group_2, post_eq):
    '''
    Creates synaptic connection between all neurons in group_1 (pre-synaptic)
    and all neurons in group_2 (post-synaptic)
    Postsynaptic dynamics are controlled by post_eq string param
    '''
    
    syn = Synapses(group_1, group_2, on_pre=post_eq) 
    return syn

def connect_synapse(synapse):
    '''
    Necessary to make an already created Syanpses object functional
    '''

    synapse.connect()

# !!!!!PLOT THINGS!!!!!!
def plot_input_with_3_groups(input_mon, mon_1, spikes_1, mon_2, spikes_2, 
        mon_3, spikes_3, title, y_label_1, y_label_2, y_label_3, ymin, ymax):
    '''
    Make 4 subplots organized vertically
    TOP = raster plot of input group spikes
    BOTTOM 3 = plots of membrane potential 
    spikes are inserted via gray bars and are recorded with spikemonitors =
    spikes_1/2/3
    '''
    f, (axinput , axPY, axFS, axSOM) = plt.subplots(4, sharex=True, sharey= False)

    axinput.plot(input_mon.t/ms, input_mon.i, '|k')
    axinput.set_yticks([])
    # Can change the title and labels based on system
    axinput.set_title(title)

    axPY.plot(mon_1.t/ms, mon_1.v[0], 'g')
    axPY.set_ylabel(y_label_1)
    axPY.vlines(spikes_1.t/ms, -0.040, 0, 'gray', lw=3)
    axPY.set_ylim([ymin, ymax])

    axFS.set_ylabel(y_label_2)
    axFS.plot(mon_2.t/ms, mon_2.v[0], 'b')
    axFS.vlines(spikes_2.t/ms, -0.040, 0, 'gray', lw=3)
    axFS.set_ylim([ymin, ymax])

    axSOM.plot(mon_3.t/ms, mon_3.v[0], 'purple')
    axSOM.vlines(spikes_3.t/ms, -0.040, 0, 'gray', lw=3)
    axSOM.set_xlabel("Time (s)")
    axSOM.set_ylabel(y_label_3)
    axSOM.set_ylim([ymin, ymax])

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
        eqs, 0.005*second, 'linear')

# initializing PY group variables
PY_group.v = -0.08*volt
PY_group.Vm = -0.08*volt
PY_group.tau_m = 0.03*second
PY_group.epsp0 = 0.005*volt
PY_group.epsp = 0.005*volt
PY_group.tau_d = 7.4*second
PY_group.D = 1
PY_group.d_rate = 0.85

# FS Neuron Group
FS_group = make_neuron_group(10, 'v>-0.045*volt', 'v=-0.05*volt',
        eqs, 0.005*second, 'linear')

# initializing FS group variables
FS_group.v = -0.065*volt
FS_group.Vm = -0.065*volt
FS_group.tau_m = 0.02*second
FS_group.epsp0 = 0.007*volt
FS_group.epsp = 0.007*volt
FS_group.d_rate = 0.35
FS_group.D = 1
FS_group.tau_d = 0.58*second

# SOM Neuron Group
SOM_group = make_neuron_group(10, 'v>-0.045*volt', 'v=-0.05*volt', eqs, 0.005*second, 'linear')

# initializing SOM group variables
SOM_group.v = -0.065*volt
SOM_group.Vm = -0.065*volt
SOM_group.tau_m = 0.02*second
SOM_group.epsp0 = 0.0005*volt
SOM_group.epsp = 0.0005*volt
SOM_group.tau_f = 0.02*second
SOM_group.F = 1
SOM_group.f_rate = 0.5


