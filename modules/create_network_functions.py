
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
        neuron_list[i] = NeuronGroup(N, model=eqs, method='euler', name=neuron)
        neuron_list[i].tau_m = vals["tau_m"]
        neuron_list[i].tau_e = vals["tau_e"]
        neuron_list[i].tau_i = vals["tau_i"]
        neuron_list[i].V0 = vals["V0"]
        i += 1
    return neuron_list
        
def create_synapses(synapse_params):
    """
    Returns a list of synapses initialized with valued specified in params
    settings["synapses"] should be passed in as the argument, with the same 
    set up as exemplified in chance_abbott_sim_settings.py
    """
    # fill list of proper size with 0's
    created_syns = [0]*len(syns)

    k = 0
    for s in syns:
        pre_neuron_name = s[0]
        pre_neuron = find_neuron_with_name(neurons, pre_neuron_name)
        post_neuron_name = s[1]
        post_neuron = find_neuron_with_name(neurons, post_neuron_name)
        created_syns[k] = Synapses(pre_neuron, post_neuron, model=, 
                name="{}_{}_synapse".format(pre_neuron_name, post_neuron_name))
        created_syns[k].connect()
        k += 1

    












