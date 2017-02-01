
from brian2 import *
from create_network_functions import *
from chance_abbott_sim_settings import *

net = Network()

# creating neurons and afferents, then adding them to the network
neuron_list = create_neurons(settings["neurons"])
afferents = create_afferents(settings["afferents"])
neuron_list.append(afferents)
net.add(neuron_list)

# creating synapses and adding them to the network
synapse_list = create_synapses(settings["synapses"], neuron_list) 
net.add(synapse_list)

monitor_list = create_state_monitors(settings["monitors"], neuron_list)
net.add(monitor_list)

visualise_connectivity(net["afferents_HVA_PY_synapse"])
