# TODO: rename module to "create_simulation" and delete functions.py?

from brian2 import *
from make_run_settings import create_run_settings
import settings_default
import dpath.util
import dill as pickle
import time

""" IMPORTANT
 Increment RUN_NUM everytime you run a simulation
"""
RUN_NUM = 0 # FIXME: change to method that doens't require hard coding


def run_net_and_save(net, settings_dict, sim_length, description):
    global RUN_NUM  # QUESTION: Is RUN_NUM global already, or has correct scope?
    net.run(sim_length*second)
    pickle.dump(net.get_states(), open("../networks/run_{}_".format(RUN_NUM) + time.strftime("%d-%m-%Y") + ".p", "wb"))
    pickle.dump(settings_dict, open("../networks/run_{}_".format(RUN_NUM) + time.strftime("%d-%m-%Y") + "_settings" + ".p", "wb"))
    with open("../networks/net_descriptions.txt", "a") as f:
        f.write("\n")
        f.write("Run #{}: ".format(RUN_NUM) + time.strftime("%d/%m/%Y"))
        f.write(description)
    RUN_NUM += 1
    print("Assign RUN_NUM to {} if you plan on running simulations later today".format(RUN_NUM))


def run_loops(sim_settings, sim_length, description, poisson_on=True):
    """
    Run several simulations based on sim_settings passed containing a list
    of values as the key for the parameter you want to modify per simulation

    Each simulation will be pickled and saved to networks directory

    Pass in string description for distinguishing purpose of simulation
    """

    # load the default settings but override with the sim_settings where present
    (list_path, run_settings) = create_run_settings(settings_default.settings,
                                                    sim_settings)

    # pull out the list of params (if list was present)
    if len(list_path) > 0:
        param_list_vals = dpath.util.get(run_settings, list_path)

    # loop over params in the list and run the simulation
    if len(list_path) == 0:
        loop_settings = run_settings.copy()
        net = create_network(loop_settings, sim_length, poisson=poisson_on)
        run_net_and_save(net, loop_settings, sim_length, description)
    else:
        for i in range(len(param_list_vals)):
            loop_settings = run_settings.copy()
            dpath.util.set(loop_settings, list_path, param_list_vals[i])
            net = create_network(loop_settings, sim_length, poisson=poisson_on)
            run_net_and_save(net, loop_settings, sim_length, description)



def create_network(settings_modified, sim_length, poisson=True):
    net = Network()

    neuron_list = create_neurons(settings_modified["neurons"])
    poisson_on = poisson
    afferents = create_afferents(settings_modified["afferents"], sim_length, poisson=poisson_on)
    neuron_list.append(afferents)
    net.add(neuron_list)

    # creating synapses and adding them to the network
    synapse_list = create_synapses(settings_modified["synapses"], neuron_list)
    net.add(synapse_list)

    monitor_list = create_state_monitors(settings_modified["monitors"], neuron_list)
    net.add(monitor_list)
    return net


def find_neuron_with_name(neuron_array, str_name):
    """
    Find neuron in a list of neurons with a certain name
    Useful for when making synapses
    """
    for n in neuron_array:
        if n.name == str_name: return n
    print("Neuron not in this list")
    return None


def create_neurons(neuron_params):
    """
    Returns a list of neurons initialized with valued specified in params
    settings["neurons"] should be passed in as the argument, with the same
    set up as exemplified in chance_abbott_sim_settings.py
    """
    # fill list of proper size with 0's
    neuron_list = [0]*len(neuron_params)
    i = 0
    for neuron, vals in neuron_params.items():

        N = vals["N"]
        eqs = vals["eqs"]
        t = 'V>=' + str(vals["thresh"]) + '*volt'
        res = 'V=' + str(vals["reset"]) + '*volt'
        v_init = vals["V_rest"]
        refract = vals["refract"]*second
        neuron_list[i] = NeuronGroup(N, model=eqs, threshold=t,
                reset=res,  method='euler', refractory=refract, name=neuron)
        neuron_list[i].tau_m = vals["tau_m"]*second
        neuron_list[i].tau_e_model = vals["tau_e"]*second
        neuron_list[i].tau_i_model = vals["tau_i"]*second
        neuron_list[i].V = v_init*volt
        neuron_list[i].V0 = v_init*volt
        neuron_list[i].Ve = -0.0*volt
        neuron_list[i].Vi = -0.090*volt

        i += 1
    return neuron_list


def create_afferents(afferent_params, sim_length_seconds, poisson=True):
    """
    Returns a neuron group initialized with values specified in params
    settings["afferents"] should be passed in as the argument, with the same
    set up as exemplified in chance_abbott_sim_settings.py
    """
    num = afferent_params["N"]
    if poisson:
        mod_rate = afferent_params["modulation_rate"]
        peak = afferent_params["peak_rate"]
        equations = afferent_params["eqs"]
        afferents = NeuronGroup(num, model=equations, threshold='rand()<rates*dt',
                method='euler', name="afferents")
        afferents.modulation_rate = mod_rate
        afferents.peak_rate = peak
    else:
        spikes_sec = int(afferent_params["spikes_per_second"])
        sec_spikes = 1/spikes_sec
        spike_arr = np.arange(0,sim_length_seconds,sec_spikes)
        spike_list = spike_arr.tolist()
        neuron_nums = []
        for i in range(num):
            neuron_nums += [i]*len(spike_arr)
        afferents = SpikeGeneratorGroup(num, neuron_nums,spike_list*num*second, name="afferents")
    return afferents


def create_synapses(synapse_params, neurons):
    """
    Returns a list of synapses initialized with values specified in params
    settings["synapses"] should be passed in as the argument, with the same
    set up as exemplified in chance_abbott_sim_settings.py
    """
    # fill list of proper size with 0's
    created_syns = [0]*len(synapse_params)

    k = 0
    for s in synapse_params:
        variables = synapse_params[s]
        pre_neuron_name = s[0]
        pre_neuron = find_neuron_with_name(neurons, pre_neuron_name)
        post_neuron_name = s[1]
        post_neuron = find_neuron_with_name(neurons, post_neuron_name)
        created_syns[k] = Synapses(pre_neuron, post_neuron, model = variables["eqs"],
                method='euler', on_pre = variables["on_spike"],
                name="{}_{}_synapse".format(pre_neuron_name, post_neuron_name))
        if pre_neuron_name == "afferents":
            created_syns[k].connect(p=0.25)
        else:
            created_syns[k].connect(p=0.25)
        created_syns[k].d1 = variables["d1"],
        created_syns[k].d2 = variables["d2"],
        created_syns[k].f1 = variables["f1"],
        created_syns[k].f2 = variables["f2"],
        created_syns[k].tau_D1 = variables["tau_D1"]*second,
        created_syns[k].tau_F1 = variables["tau_F1"]*second,
        created_syns[k].tau_D2 = variables["tau_D2"]*second,
        created_syns[k].tau_F2 = variables["tau_F2"]*second,
        created_syns[k].w_e = variables["w_e"]
        created_syns[k].w_i = variables["w_i"]
        created_syns[k].tau_e = variables["tau_e"]*second
        created_syns[k].tau_i = variables["tau_i"]*second
        created_syns[k].D1 = 1
        created_syns[k].D2 = 1
        created_syns[k].F1 = 1
        created_syns[k].F2 = 1
        k += 1
    return created_syns


def create_state_monitors(monitor_params, neuron_list):
    """
    Returns a list of monitors initialized with values specified in params
    settings["monitors"] should be passed in as the argument, with the same
    set up as exemplified in chance_abbott_sim_settings.py
    """
    # current max of 20 monitors
    mons = [0]*20
    i = 0
    for key, val in monitor_params.items():
        neuron = find_neuron_with_name(neuron_list, key)
        if val == "spikes":
            mons[i] = SpikeMonitor(neuron, name="afferent_spike_mon")
            continue
        v = val.split()
        for variable in v:
            mons[i] = StateMonitor(neuron, variable, record=True, name="{}_{}_mon".format(key, variable))
            i += 1
        i += 1
    mons_stripped = [x for x in mons if type(x) != int]
    return mons_stripped

# TODO: move to analysis code?
def visualise_connectivity(S):
    Ns = len(S.source)
    Nt = len(S.target)
    figure(figsize=(10, 4))
    subplot(121)
    plot(zeros(Ns), arange(Ns), 'ok', ms=10)
    plot(ones(Nt), arange(Nt), 'ok', ms=10)
    for i, j in zip(S.i, S.j):
        plot([0, 1], [i, j], '-k')
    xticks([0, 1], ['Source', 'Target'])
    ylabel('Neuron index')
    xlim(-0.1, 1.1)
    ylim(-1, max(Ns, Nt))
    subplot(122)
    plot(S.i, S.j, 'ok')
    xlim(-1, Ns)
    ylim(-1, Nt)
    xlabel('Source neuron index')
    ylabel('Target neuron index')
    show()
