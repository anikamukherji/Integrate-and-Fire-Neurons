"""Settings to test STP dynamics.

1) Enforces all the HVA neurons to be identical (all clones
   of the default PY cells)

2) Recovery of D,F is infinite so that we can see:
    * Geometric decay for Depression
    * Linear increase for facilitation

3) Feedforward weights of the V1 afferents onto the HVA neurons
   3 different values so that we can ensure the weights are correct
     * the P1 amplitude should be equal to this weight.

4) Dynamics of STP are different across the HVA neurons to check to make
   sure things are correct.

5) Decay of synaptic conductance is instantaneous so that there is no summation
   and the only dynamics of the EPSCs is due to STP (D,F, d,f)

"""

from equations import neuron_eqs, synapse_eqs, onspike_eqs, sinusoid_rate


settings = {
    "neurons": {
        "HVA_PY": {
            "N": 1,
            "eqs": None,
            "tau_m": 0.030,
            "tau_e": 0.002,
            "tau_i": 0.010,
            "thresh": -0.044,
            "reset": -0.050,
            "V_rest": -0.075,
            "refract": 0.0015
        },
        "FS": {
            "N": 1,
            "eqs": None,
            "tau_m": 0.030,
            "tau_e": 0.002,
            "tau_i": 0.010,
            "thresh": -0.044,
            "reset": -0.050,
            "V_rest": -0.075,
            "refract": 0.0015
        },
        "SOM": {
            "N": 1,
            "eqs": None,
            "tau_m": 0.030,
            "tau_e": 0.002,
            "tau_i": 0.010,
            "thresh": -0.044,
            "reset": -0.050,
            "V_rest": -0.075,
            "refract": 0.0015
        }
    },

    "afferents": {
        "N": 1,
        "use_poisson": False,
        "modulation_rate": None,
        "peak_rate": None,
        "spikes_per_second": [1, 10, 50, 100],  # pulse train frequencies
        "eqs": None
    },

    "synapses": {
        ("SOM", "HVA_PY"): {
            "eqs": None,
            "on_spike": None,
            "d1": None,
            "d2": None,
            "f1": None,
            "f2": None,
            "tau_D1": None,
            "tau_D2": None,
            "tau_F1": None,
            "tau_F2": None,
            "w_e": 0,  # no recurrent effect of SOM onto HVA_PY
            "w_i": 0,  # no recurrent effect of SOM onto HVA_PY
            "tau_e": None,
            "tau_i": None,
            "delay": None
        },

        ("FS", "HVA_PY"): {
            "eqs": None,
            "on_spike": None,
            "d1": None,
            "d2": None,
            "f1": None,
            "f2": None,
            "tau_D1": None,
            "tau_D2": None,
            "tau_F1": None,
            "tau_F2": None,
            "w_e": 0,  # no recurrent effect of SOM onto HVA_PY
            "w_i": 0,  # no recurrent effect of SOM onto HVA_PY
            "tau_e": None,
            "tau_i": None,
            "delay": None
        },

        ("afferents", "HVA_PY"): {
            "eqs": synapse_eqs,
            "on_spike": onspike_eqs,
            "d1": 0.8,
            "d2": 1,
            "f1": 1,
            "f2": 1,
            "tau_D1": 100000,
            "tau_D2": 100000,
            "tau_F1": 100000,
            "tau_F2": 100000,
            "w_e": 10,
            "w_i": 0,
            "tau_e": 0.001,
            "tau_i": 0.001,
            "delay": 0
        },

        ("afferents", "FS"): {
            "eqs": synapse_eqs,
            "on_spike": onspike_eqs,
            "d1": 0.5,
            "d2": 1,
            "f1": 1,
            "f2": 1,
            "tau_D1": 100000,
            "tau_D2": 100000,
            "tau_F1": 100000,
            "tau_F2": 100000,
            "w_e": 1,
            "w_i": 0,
            "tau_e": 0.001,
            "tau_i": 0.001,
            "delay": 0
        },

        ("afferents", "SOM"): {
            "eqs": synapse_eqs,
            "on_spike": onspike_eqs,
            "d1": None,
            "d2": None,
            "f1": None,
            "f2": None,
            "tau_D1": 100000,
            "tau_D2": 100000,
            "tau_F1": 100000,
            "tau_F2": 100000,
            "w_e": 0.5,
            "w_i": 0,
            "tau_e": 0.001,
            "tau_i": 0.001,
            "delay": 0
        }
    },

    "monitors": {
        "HVA_PY": 'V Ge_total Gi_total',
        "FS": 'V Ge_total Gi_total',
        "SOM": 'V Ge_total Gi_total',
        "afferents": 'spikes'
    }
}
