
# import standard stuff
import brian2 as brian
import dpath.util
import dill as pickle
import os
import time

# import from within this codebase
from make_run_settings import create_run_settings
import settings_default


def run_simulations(sim_settings, description, dat_path):
    """
    Run several simulations based on sim_settings passed containing a list
    of values as the key for the parameter you want to modify per simulation

    Each simulation will be pickled and saved to networks directory

    Pass in string description for distinguishing purpose of simulation
    """

    # generate a new directory for saved data in the dat_path location
    sim_data_path = make_data_directory(dat_path)
    print("Saving to: {}".format(sim_data_path))

    # load the default settings, override with the sim_settings where present
    (list_path, run_settings) = create_run_settings(settings_default.settings,
                                                    sim_settings)

    # loop over params in the list and run the simulation
    try:
        if len(list_path) == 0:
            loop_settings = run_settings.copy()
            run_net_and_save(loop_settings, description, sim_data_path, 1)
        else:
            param_list_vals = dpath.util.get(run_settings, list_path)
            for i_run in range(len(param_list_vals)):
                loop_settings = run_settings.copy()
                dpath.util.set(loop_settings,
                               list_path,
                               param_list_vals[i_run]
                               )
                run_net_and_save(loop_settings,
                                 description,
                                 sim_data_path,
                                 i_run
                                 )
        print("Simulation successful")

    except Exception:
        os.chdir(dat_path)
        os.rmdir(sim_data_path)
        print("Simulation failed. Delete empty directories")
        raise

    return


def run_net_and_save(settings_dict, description, sim_data_path, file_num):

    # run the simulation
    net = create_network(settings_dict)
    sim_length = settings_dict["afferents"]["sim_time"]
    print("  Running network {}".format(file_num))
    net.run(sim_length * brian.second)

    # save the simulation
    data_to_save = {
        "net": net.get_states(),
        "settings": settings_dict,
        "description": description
    }
    fname = "network_data_run_{}".format(file_num)
    fpath = sim_data_path + os.sep + fname
    save_simulation_data(data_to_save, fpath)

    return


def save_simulation_data(data_to_save, fpath):

    with open(fpath + '.p', 'wb') as f:
                pickle.dump(data_to_save, f, -1)
    return


def make_data_directory(dat_path) -> str:
    """
    Make a new directory for the saved simulation data.

    Directory name is based off date string
    Returns the path.
    """

    # cd to the dat_path
    os.chdir(dat_path)

    # make a new directory
    tm = time.gmtime()
    fname = "{}_{}_{}_{}".format(tm.tm_year, tm.tm_yday, tm.tm_hour, tm.tm_min)
    os.mkdir(fname)

    # return the path to the new directory
    return dat_path + os.sep + fname


def create_network(settings_modified):

    net = brian.Network()

    neuron_list = create_neurons(settings_modified["neurons"])
    afferents = create_afferents(settings_modified["afferents"])
    neuron_list.append(afferents)
    net.add(neuron_list)

    # creating synapses and adding them to the network
    synapse_list = create_synapses(settings_modified["synapses"], neuron_list)
    net.add(synapse_list)

    monitor_list = create_state_monitors(settings_modified["monitors"],
                                         neuron_list)
    net.add(monitor_list)
    return net


def find_neuron_with_name(neuron_array, str_name):
    """
    Find neuron in a list of neurons with a certain name
    Useful for when making synapses
    """
    for n in neuron_array:
        if n.name == str_name:
            return n
    print("Neuron not in this list")
    return None


def create_neurons(neuron_params):
    """
    Returns a list of neurons initialized with valued specified in params
    settings["neurons"] should be passed in as the argument, with the same
    set up as exemplified in chance_abbott_sim_settings.py
    """
    # fill list of proper size with 0's
    neuron_list = [0] * len(neuron_params)
    i = 0
    for neuron, vals in neuron_params.items():

        N = vals["N"]
        eqs = vals["eqs"]
        t = 'V>=' + str(vals["thresh"]) + '*volt'
        res = 'V=' + str(vals["reset"]) + '*volt'
        v_init = vals["V_rest"]
        refract = vals["refract"] * brian.second
        neuron_list[i] = brian.NeuronGroup(N,
                                           model=eqs,
                                           threshold=t,
                                           reset=res,
                                           method='euler',
                                           refractory=refract,
                                           name=neuron
                                           )
        neuron_list[i].tau_m = vals["tau_m"] * brian.second
        neuron_list[i].tau_e_model = vals["tau_e"] * brian.second
        neuron_list[i].tau_i_model = vals["tau_i"] * brian.second
        neuron_list[i].V = v_init * brian.volt
        neuron_list[i].V0 = v_init * brian.volt
        neuron_list[i].Ve = -0.0 * brian.volt
        neuron_list[i].Vi = -0.090 * brian.volt

        i += 1
    return neuron_list


def create_afferents(afferent_params):
    """
    Returns a neuron group initialized with values specified in params
    settings["afferents"] should be passed in as the argument, with the same
    set up as exemplified in chance_abbott_sim_settings.py
    """
    num = afferent_params["N"]
    use_poisson = afferent_params["use_poisson"]
    if use_poisson:
        mod_rate = afferent_params["modulation_rate"]
        peak = afferent_params["peak_rate"]
        equations = afferent_params["eqs"]
        afferents = brian.NeuronGroup(num,
                                      model=equations,
                                      threshold='rand()<rates*dt',
                                      method='euler',
                                      name="afferents"
                                      )
        afferents.modulation_rate = mod_rate
        afferents.peak_rate = peak
    else:
        sim_length_sec = afferent_params["sim_time"]
        isi_sec = 1 / afferent_params["spikes_per_second"]
        spike_arr = brian.arange(0, sim_length_sec, isi_sec)  # numpy
        spike_list = spike_arr.tolist() * num * brian.second
        neuron_nums = []
        for idx in range(num):
            neuron_nums += [idx] * len(spike_arr)
        afferents = brian.SpikeGeneratorGroup(num,
                                              neuron_nums,
                                              spike_list,
                                              name="afferents"
                                              )
    return afferents


def create_synapses(synapse_params, neurons):
    """
    Returns a list of synapses initialized with values specified in params
    settings["synapses"] should be passed in as the argument, with the same
    set up as exemplified in chance_abbott_sim_settings.py
    """
    # initialize an empty list
    created_syns = []

    for syn in synapse_params.keys():
        # create the synapse and give it a name
        variables = synapse_params[syn]
        pre_neuron_name = syn[0]  # key is tuple (pre, post)
        pre_neuron = find_neuron_with_name(neurons, pre_neuron_name)
        post_neuron_name = syn[1]
        post_neuron = find_neuron_with_name(neurons, post_neuron_name)
        syn_name = "{}_{}_synapse".format(pre_neuron_name, post_neuron_name)
        created_syns.append(brian.Synapses(pre_neuron,
                                           post_neuron,
                                           model=variables["eqs"],
                                           method='euler',
                                           on_pre=variables["on_spike"],
                                           name=syn_name
                                           ))

        # modify the synapse properties
        created_syns[-1].connect(p=variables["p_connect"])
        created_syns[-1].d1 = variables["d1"]
        created_syns[-1].d2 = variables["d2"]
        created_syns[-1].f1 = variables["f1"]
        created_syns[-1].f2 = variables["f2"]
        created_syns[-1].tau_D1 = variables["tau_D1"] * brian.second
        created_syns[-1].tau_F1 = variables["tau_F1"] * brian.second
        created_syns[-1].tau_D2 = variables["tau_D2"] * brian.second
        created_syns[-1].tau_F2 = variables["tau_F2"] * brian.second
        created_syns[-1].w_e = variables["w_e"]
        created_syns[-1].w_i = variables["w_i"]
        created_syns[-1].D1 = 1
        created_syns[-1].D2 = 1
        created_syns[-1].F1 = 1
        created_syns[-1].F2 = 1

    return created_syns


def create_state_monitors(monitor_params, neuron_list):
    """
    Returns a list of monitors initialized with values specified in params
    settings["monitors"] should be passed in as the argument, with the same
    set up as exemplified in chance_abbott_sim_settings.py
    """

    mons = []
    for key, val in monitor_params.items():
        neuron = find_neuron_with_name(neuron_list, key)

        if val == "spikes":
            mons.append(brian.SpikeMonitor(neuron, name="afferent_spike_mon"))
        else:
            v = val.split()
            for variable in v:
                tmp_name = "{}_{}_mon".format(key, variable)
                mons.append(brian.StateMonitor(neuron,
                                               variable,
                                               record=True,
                                               name=tmp_name
                                               ))

    return mons
