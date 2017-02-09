
from brian2 import *

def find_neuron_with_name(neuron_array, str_name):
    """
    Find neuron in a list of neurons with a certain name
    Useful for when making synapses
    """
    for n in neuron_array:
        if n.name == str_name: return n
    print("Neuron not in this list")
    return None

def create_neurons(neuron_params):
    """
    Returns a list of neurons initialized with valued specified in params
    settings["neurons"] should be passed in as the argument, with the same 
    set up as exemplified in chance_abbott_sim_settings.py
    """
    # fill list of proper size with 0's
    neuron_list = [0]*len(neuron_params)
    i = 0
    for neuron, vals in neuron_params.items():
        
        N = vals["N"]
        eqs = vals["eqs"] 
        # maybe add reset and/or threshold?
        neuron_list[i] = NeuronGroup(N, model=eqs, threshold='V>=-0.055*volt', reset='V=-0.058*volt', method='euler', name=neuron)
        neuron_list[i].tau_m = vals["tau_m"]
        neuron_list[i].tau_e_model = vals["tau_e"]
        neuron_list[i].tau_i_model = vals["tau_i"]
        neuron_list[i].V = -0.070*volt
        neuron_list[i].V0 = -0.070*volt
        neuron_list[i].Ve = -0.0*volt
        neuron_list[i].Vi = -0.090*volt

        i += 1
    return neuron_list
        
def create_afferents(afferent_params):
    """
    Returns a neuron group initialized with values specified in params
    settings["afferents"] should be passed in as the argument, with the same 
    set up as exemplified in chance_abbott_sim_settings.py
    """
    num = afferent_params["N"]
    mod_rate = afferent_params["modulation_rate"]
    peak = afferent_params["modulation_rate"]
    equations = afferent_params["eqs"]
    afferents = NeuronGroup(num, model=equations, threshold='rand()<rates*dt', method='euler', name="afferents")
    afferents.modulation_rate = mod_rate
    afferents.peak_rate = peak
    return afferents
    


    
def create_synapses(synapse_params, neurons):
    """
    Returns a list of synapses initialized with values specified in params
    settings["synapses"] should be passed in as the argument, with the same 
    set up as exemplified in chance_abbott_sim_settings.py
    """
    # fill list of proper size with 0's
    created_syns = [0]*len(synapse_params)

    k = 0
    for s in synapse_params:
        variables = synapse_params[s]
        pre_neuron_name = s[0]
        pre_neuron = find_neuron_with_name(neurons, pre_neuron_name)
        post_neuron_name = s[1]
        post_neuron = find_neuron_with_name(neurons, post_neuron_name)
        created_syns[k] = Synapses(pre_neuron, post_neuron, model = variables["eqs"], 
                method='euler', on_pre = variables["on_spike"], 
                name="{}_{}_synapse".format(pre_neuron_name, post_neuron_name))
        created_syns[k].connect()
        created_syns[k].d1 = variables["d1"],
        created_syns[k].d2 = variables["d2"],
        created_syns[k].f1 = variables["f1"],
        created_syns[k].f2 = variables["f2"],
        created_syns[k].tau_D1 = variables["tau_D1"],
        created_syns[k].tau_F1 = variables["tau_F1"],
        created_syns[k].tau_D2 = variables["tau_D2"],
        created_syns[k].tau_F2 = variables["tau_F2"],
        created_syns[k].w_e = variables["w_e"]
        created_syns[k].w_i = variables["w_i"]
        created_syns[k].tau_e = variables["tau_e"]
        created_syns[k].tau_i = variables["tau_i"]
        k += 1
    return created_syns

    
def create_state_monitors(monitor_params, neuron_list):
    """
    Returns a list of monitors initialized with values specified in params
    settings["monitors"] should be passed in as the argument, with the same 
    set up as exemplified in chance_abbott_sim_settings.py
    """
    mons = [0]*len(monitor_params)
    i = 0
    for key, val in monitor_params.items():

        neuron = find_neuron_with_name(neuron_list, key)
        if val == "spikes":
            mons[i] = SpikeMonitor(neuron, name="afferent_spike_mon")
            continue
        mons[i] = StateMonitor(neuron, val, record=True, name="{}_{}_mon".format(key, val))
        i += 1
    return mons


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











