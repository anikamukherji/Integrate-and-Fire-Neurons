
from brian2 import *
from create_network_functions import *
from chance_abbott_sim_settings import *


def create_network(*args):
    net = Network()

    # ugly nested for loop to replace values in settings file
    # arguments given to this function should be a string listing out 
    # the key path to the variable you want to replace
    # don't include "settings" 

    for path in args:
        path_name = path.split()
        length = len(path_name) - 2
        i = 0
        for k0 in settings.keys():
            if k0 == path_name[0]:
                i += 1
                if i > length:
                    settings[k0] = path_name[i]
                    break
                for k1 in settings[k0].keys():
                    if k1 == path_name[1]:
                        i += 1
                        if i > length:
                            settings[k0][k1] = path_name[i]
                            break
                        for k2 in settings[k0][k1].keys():
                            if k2 == path_name[2]:
                                i += 1
                                if i > length:
                                    settings[k0][k1][k2] = path_name[i]
                                    break

    neuron_list = create_neurons(settings["neurons"])
    afferents = create_afferents(settings["afferents"])
    neuron_list.append(afferents)
    net.add(neuron_list)

    # creating synapses and adding them to the network
    synapse_list = create_synapses(settings["synapses"], neuron_list) 
    net.add(synapse_list)

    monitor_list = create_state_monitors(settings["monitors"], neuron_list)
    net.add(monitor_list)
    return net

