
from brian2.units import *
from equations.chance_abbott_eqs import *
from equations.thalamic_inputs import *

settings = {
    "neurons":
        {
            "HVA_PY":{
                "N":1,
                "eqs":neuron_eqs,
                "tau_m":0.030,
                "tau_e":0.002,
                "tau_i":0.010
                },
            "FS":{
                "N":20,
                "eqs":neuron_eqs,
                "tau_m":0.030,
                "tau_e":0.002,
                "tau_i":0.010
                    },
            "SOM":{
                "N":20,
                "eqs":neuron_eqs,
                "tau_m":0.030,
                "tau_e":0.002,
                "tau_i":0.010
                }
            },

        "afferents":{
            "N":200,
            "modulation_rate":10,
            "peak_rate":10,
            "spikes_per_second":20,
            "eqs":sinusoid_rate
            },

        "synapses":{

            ("SOM", "HVA_PY"):{
                "eqs":synapse_eqs,
                "on_spike":onspike_eqs,
                "d1":0.5,
                "d2":1.0,
                "f1":0.0,
                "f2":0.0,
                "tau_D1":0.300,
                "tau_D2":0.300,
                "tau_F1":0.300,
                "tau_F2":0.300,
                "w_e":0.00,
                "w_i":0.04,
                "tau_e":0.002,
                "tau_i":0.010,
                "delay":0
                }, 

            ("FS", "HVA_PY"):{
                "eqs":synapse_eqs,
                "on_spike":onspike_eqs,
                "d1":0.4,
                "d2":1.0,
                "f1":0.0,
                "f2":0.0,
                "tau_D1":0.300,
                "tau_D2":0.300,
                "tau_F1":0.300,
                "tau_F2":0.300,
                "w_e":0.00,
                "w_i":0.2,
                "tau_e":0.002,
                "tau_i":0.010,
                "delay":0
                }, 

            ("afferents", "HVA_PY"):{
                "eqs":synapse_eqs,
                "on_spike":onspike_eqs,
                "d1":0.6,
                "d2":1.0,
                "f1":0.3,
                "f2":0.0,
                "tau_D1":0.500,
                "tau_D2":0.300,
                "tau_F1":0.080,
                "tau_F2":0.300,
                "w_e":0.1,
                "w_i":0.00,
                "tau_e":0.002,
                "tau_i":0.010,
                "delay":0
                }, 

            ("afferents", "FS"):{
                "eqs":synapse_eqs,
                "on_spike":onspike_eqs,
                "d1":0.2,
                "d2":1.0,
                "f1":0.0,
                "f2":0.0,
                "tau_D1":0.080,
                "tau_D2":0.300,
                "tau_F1":0.300,
                "tau_F2":0.300,
                "w_e":.2,
                "w_i":0.00,
                "tau_e":0.002,
                "tau_i":0.010,
                "delay":0
                }, 

            ("afferents", "SOM"):{
                "eqs":synapse_eqs,
                "on_spike":onspike_eqs,
                "d1":1.0,
                "d2":1.0,
                "f1":0.6,
                "f2":0.0,
                "tau_D1":0.300,
                "tau_D2":0.300,
                "tau_F1":0.300,
                "tau_F2":0.300,
                "w_e":0.080,
                "w_i":0.00,
                "tau_e":0.002,
                "tau_i":0.010,
                "delay":0
                } 
            },

        "monitors":{
                "HVA_PY": 'V',
                "afferents": 'spikes'
            }
}

# print(settings["neurons"]["PY"]["eqs"])
