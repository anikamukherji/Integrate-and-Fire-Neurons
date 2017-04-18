"""Empty settings dict.

1) Fill in this dictionary with values to over-ride the default params.

2) Re-name the file settings_sim_YYYYY where YYYYY describes the type
   of the model (eg. settings_sim_medial_areas to model PM or AL)

3) For testing situations, name the file settings_test_YYYYY

4) Write a description of the new network in the docstring of the new
   settings file.

"""


settings = {
    "neurons": {
        "HVA_PY": {
            "N": None,
            "eqs": None,
            "tau_m": None,
            "tau_e": None,
            "tau_i": None,
            "thresh": None,
            "reset": None,
            "V_rest": None,
            "refract": None
        },
        "FS": {
            "N": None,
            "eqs": None,
            "tau_m": None,
            "tau_e": None,
            "tau_i": None,
            "thresh": None,
            "reset": None,
            "V_rest": None,
            "refract": None
        },
        "SOM": {
            "N": None,
            "eqs": None,
            "tau_m": None,
            "tau_e": None,
            "tau_i": None,
            "thresh": None,
            "reset": None,
            "V_rest": None,
            "refract": None
        }
    },

    "afferents": {
        "N": None,
        "use_poisson": None,
        "modulation_rate": None,
        "peak_rate": None,
        "spikes_per_second": None,
        "eqs": None,
        "sim_time": 2
    },

    "synapses": {
        ("SOM", "HVA_PY"): {
            "eqs": None,
            "on_spike": None,
            "p_connect": None,
            "d1": None,
            "d2": None,
            "f1": None,
            "f2": None,
            "tau_D1": None,
            "tau_D2": None,
            "tau_F1": None,
            "tau_F2": None,
            "w_e": None,
            "w_i": None,
            "tau_e": None,
            "tau_i": None,
            "delay": None
        },

        ("FS", "HVA_PY"): {
            "eqs": None,
            "on_spike": None,
            "p_connect": None,
            "d1": None,
            "d2": None,
            "f1": None,
            "f2": None,
            "tau_D1": None,
            "tau_D2": None,
            "tau_F1": None,
            "tau_F2": None,
            "w_e": None,
            "w_i": None,
            "tau_e": None,
            "tau_i": None,
            "delay": None
        },

        ("afferents", "HVA_PY"): {
            "eqs": None,
            "on_spike": None,
            "p_connect": None,
            "d1": None,
            "d2": None,
            "f1": None,
            "f2": None,
            "tau_D1": None,
            "tau_D2": None,
            "tau_F1": None,
            "tau_F2": None,
            "w_e": None,
            "w_i": None,
            "tau_e": None,
            "tau_i": None,
            "delay": None
        },

        ("afferents", "FS"): {
            "eqs": None,
            "on_spike": None,
            "p_connect": None,
            "d1": None,
            "d2": None,
            "f1": None,
            "f2": None,
            "tau_D1": None,
            "tau_D2": None,
            "tau_F1": None,
            "tau_F2": None,
            "w_e": None,
            "w_i": None,
            "tau_e": None,
            "tau_i": None,
            "delay": None
        },

        ("afferents", "SOM"): {
            "eqs": None,
            "on_spike": None,
            "p_connect": None,
            "d1": None,
            "d2": None,
            "f1": None,
            "f2": None,
            "tau_D1": None,
            "tau_D2": None,
            "tau_F1": None,
            "tau_F2": None,
            "w_e": None,
            "w_i": None,
            "tau_e": None,
            "tau_i": None,
            "delay": None
        }
    },

    "monitors": {
        "HVA_PY": None,
        "FS": None,
        "SOM": None,
        "afferents": None
    }
}
