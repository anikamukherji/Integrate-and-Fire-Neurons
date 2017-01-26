
from brian2 import *
from modules.equations.chance_abbott_eqs import *

def find_neuron_with_name(neuron_array, str_name):
    """
    Find neuron in a list of neurons with a certain name
    Useful for when finding synapses
    """
    for n in neuron_array:
        if n.name == str_name: return n
    print("Neuron not in this list")
    return None
    
thal_model='''
        rates = peak_rate*sin(2*pi*t*modulation_rate/second)*Hz : Hz
        modulation_rate : 1
        peak_rate : 1
        '''

params = {"thalamic_input":thal_model, "PV":neuron_eqs,
        "SOM":neuron_eqs, "PY":neuron_eqs }
neurons = [0]*len(params)


x = 0
for key, val in params.items():
    
    neurons[x] = NeuronGroup(1, model=val, name=key)
    x += 1

print(neurons)

syns = [("PV", "PY"), ("SOM", "PY")]

created_syns = [0]*len(syns)

k = 0
for s in syns:
    pre_neuron_name = s[0]
    pre_neuron = find_neuron_with_name(neurons, pre_neuron_name)
    post_neuron_name = s[1]
    post_neuron = find_neuron_with_name(neurons, post_neuron_name)
    created_syns[k] = Synapses(pre_neuron, post_neuron, model=synapse_eqs, 
            name="{}_{}_synapse".format(pre_neuron_name, post_neuron_name))
    k += 1

print(created_syns)



    
