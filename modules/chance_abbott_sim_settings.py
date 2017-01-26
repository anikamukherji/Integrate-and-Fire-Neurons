
from brian2.units import *
from equations.chance_abbott_eqs import *
from equations.thalamic_inputs import *

settings = {
    "neurons":
        {
            "HVA_PY":{
                "N":1,
                "eqs":neuron_eqs,
                "tau_m":0.030*second,
                "tau_e":0.002*second,
                "tau_i":0.010*second
                },
            "FS":{
                "N":1,
                "eqs":neuron_eqs,
                "tau_m":0.030*second,
                "tau_e":0.002*second,
                "tau_i":0.010*second
                    },
            "SOM":{
                "N":1,
                "eqs":neuron_eqs,
                "tau_m":0.030*second,
                "tau_e":0.002*second,
                "tau_i":0.010*second
                }
            },

        "afferents":{
            "N":200,
            "modulation_rate":10,
            "peak_rate":100,
            "eqs":sinusoid_rate
            },

        "syanpses":{

            ("SOM", "HVA_PY"):{
                "eqs":syn_eqs,
                "on_spike":onspike_eqs,
                "d1":0.4,
                "d2":1.0,
                "f1":1.0,
                "f2":1.0,
                "tau_D1":0.300*second,
                "tau_D2":0.300*second,
                "tau_F1":0.300*second,
                "tau_F2":0.300*second,
                "w_e":0.009,
                "w_i":0.00,
                "tau_e":0.002*second,
                "tau_i":0.010*second,
                "delay":0
                }, 

            ("FS", "HVA_PY"):{
                "eqs":syn_eqs,
                "on_spike":onspike_eqs,
                "d1":0.4,
                "d2":1.0,
                "f1":1.0,
                "f2":1.0,
                "tau_D1":0.300*second,
                "tau_D2":0.300*second,
                "tau_F1":0.300*second,
                "tau_F2":0.300*second,
                "w_e":0.009,
                "w_i":0.00,
                "tau_e":0.002*second,
                "tau_i":0.010*second,
                "delay":0
                }, 

            ("afferents", "HVA_PY"):{
                "eqs":syn_eqs,
                "on_spike":onspike_eqs,
                "d1":0.4,
                "d2":1.0,
                "f1":1.0,
                "f2":1.0,
                "tau_D":0.300*second,
                "tau_F":0.300*second,
                "w_e":0.009,
                "w_i":0.00,
                "tau_e":0.002*second,
                "tau_i":0.010*second,
                "delay":0
                }, 

            ("afferents", "FS"):{
                "eqs":syn_eqs,
                "on_spike":onspike_eqs,
                "d1":0.4,
                "d2":1.0,
                "f1":1.0,
                "f2":1.0,
                "tau_D":0.300*second,
                "tau_F":0.300*second,
                "w_e":0.009,
                "w_i":0.00,
                "tau_e":0.002*second,
                "tau_i":0.010*second,
                "delay":0
                }, 

            ("afferents", "SOM"):{
                "eqs":syn_eqs,
                "on_spike":onspike_eqs,
                "d1":0.4,
                "d2":1.0,
                "f1":1.0,
                "f2":1.0,
                "tau_D":0.300*second,
                "tau_F":0.300*second,
                "w_e":0.009,
                "w_i":0.00,
                "tau_e":0.002*second,
                "tau_i":0.010*second,
                "delay":0
                } 
            },

        "monitors":{
                "afferents":"spikes",
            }
}

# print(settings["neurons"]["PY"]["eqs"])
