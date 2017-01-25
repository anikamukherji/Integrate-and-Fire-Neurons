
from brian2.units import *
from equations.chance_abbott_eqs import *
# from equations.thalamic_inputs.py import *

settings = {
    "neurons":
        {
            "PY":{
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
            "peak_rate":100
            },

        "syanpses":{

            ("SOM", "PY"):{
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

            ("FS", "PY"):{
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

            ("afferents", "PY"):{
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
            
            
            }
}

# print(settings["neurons"]["PY"]["eqs"])
