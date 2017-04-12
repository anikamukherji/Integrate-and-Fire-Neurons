from brian2 import *
# QUESTION: Is this module used anymore?

def make_poisson_input(N, firing_rates, str_name=None):
    '''
    Makes poisson input group with N neurons
    firing_rates can be a function formatted as a string or
    a number with units Hz
    '''
    if str_name is None:
        poisson_input = PoissonGroup(N, rates=firing_rates)
    else:
        poisson_input = PoissonGroup(N, rates=firing_rates, name=str_name)
    return poisson_input

def make_spike_generator(N, time_array, str_name=None):
    '''
    Returns SpikeGeneratorGroup with N neurons that fires
    according to times specified in array (so must have units second)
    '''
    if str_name is None:
        gen = SpikeGeneratorGroup(N, [0]*len(time_array), times=time_array)
    else:
        gen = SpikeGeneratorGroup(N, [0]*len(time_array), times=time_array, name=str_name)
    return gen

def make_neuron_group(N, thresh, reset_value, eq_model, refract,
        integration_method, str_name=None, time_step=0.1*msecond):
    '''
    Makes neuron group with N neurons
    All other parameters should be formatted as strings
    Ex. thresh='v>-0.04*volt', reset_value='v=-0.05*volt'
    '''
    if str_name is None:
        neuron_group = NeuronGroup(N, threshold=thresh, reset=reset_value,
            model=eq_model, refractory=refract, method=integration_method,
            dt=time_step)
    else:
        neuron_group = NeuronGroup(N, threshold=thresh, reset=reset_value,
            model=eq_model, refractory=refract, method=integration_method, name=str_name,
            dt=time_step)
    return neuron_group

def make_synapse(group_1, group_2, post_eq, str_name=None):
    '''
    Creates synaptic connection between all neurons in group_1 (pre-synaptic)
    and all neurons in group_2 (post-synaptic)
    Postsynaptic dynamics are controlled by post_eq string param
    '''

    if str_name is None:
        syn = Synapses(group_1, group_2, on_pre=post_eq)
    else:
        syn = Synapses(group_1, group_2, on_pre=post_eq, name=str_name)
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
    axSOM.set_xlabel("Time (ms)")
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
