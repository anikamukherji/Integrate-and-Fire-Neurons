
from brian2 import *
from create_network_functions import *
from chance_abbott_sim_settings import *


def create_network(settings_modified, sim_length, poisson=True):
    net = Network()

    neuron_list = create_neurons(settings_modified["neurons"])
    if poisson:
        afferents = create_afferents(settings_modified["afferents"], sim_length)
    if not poisson:
        afferents = create_afferents(settings_modified["afferents"], sim_length, poisson=False)
    neuron_list.append(afferents)
    net.add(neuron_list)

    # creating synapses and adding them to the network
    synapse_list = create_synapses(settings_modified["synapses"], neuron_list) 
    net.add(synapse_list)

    monitor_list = create_state_monitors(settings_modified["monitors"], neuron_list)
    net.add(monitor_list)
    return net

