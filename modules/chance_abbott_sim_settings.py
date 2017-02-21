
from brian2.units import *
from equations.chance_abbott_eqs import *
from equations.thalamic_inputs import *

settings = {
    "neurons":
        {
            "HVA_PY":{
                "N":1,
                "eqs":neuron_eqs,
                "tau_m":0.015,
                "tau_e":0.002,
                "tau_i":0.010,
                "thresh":-0.040,
                "reset":-0.058,
                "V_rest":-0.07,
                "refract":0.00
                },
            "FS":{
                "N":1,
                "eqs":neuron_eqs,
                "tau_m":0.007,
                "tau_e":0.002,
                "tau_i":0.010,
                "thresh":-0.030,
                "reset":-0.058,
                "V_rest":-0.07,
                "refract":0.00
                },
            "SOM":{
                "N":1,
                "eqs":neuron_eqs,
                "tau_m":0.030,
                "tau_e":0.002,
                "tau_i":0.010,
                "thresh":-0.035,
                "reset":-0.058,
                "V_rest":-0.07,
                "refract":0.00
                }
            },

        "afferents":{
            "N":650,
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
                "w_i":0.02,
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
                "w_e":0.01,
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
                "tau_D1":0.30,
                "tau_D2":0.300,
                "tau_F1":0.300,
                "tau_F2":0.300,
                "w_e":0.02,
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
                "f1":0.1,
                "f2":0.0,
                "tau_D1":0.300,
                "tau_D2":0.300,
                "tau_F1":0.300,
                "tau_F2":0.300,
                "w_e":0.050,
                "w_i":0.00,
                "tau_e":0.002,
                "tau_i":0.010,
                "delay":0
                } 
            },

        "monitors":{
                "HVA_PY": 'V Ge_total Gi_total',
                "FS": 'V Ge_total Gi_total',
                "SOM": 'V Ge_total Gi_total',
                "afferents": 'spikes'
            }
}

# print(settings["neurons"]["PY"]["eqs"])
