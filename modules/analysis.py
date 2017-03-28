
from brian2tools import *
import matplotlib.pyplot as plt
from create_network import create_network
from chance_abbott_sim_settings import settings
from run_simulation import * 
from create_network_functions import visualise_connectivity
import dill as pickle
import math

########################################################################
# this file will be used to plot and compute various analyses of the data
# from pickled networks
########################################################################

def plot_everything(filenames, neuron_index=0):
    """
    Plots voltage, excitatory conductance and/or inhibitory conductance
    from HVA_PY, SOM, and FS cells
    Plots values from neuron 0 by default
    """
    f, axs = plt.subplots(len(filenames), 3)
    axs[0,0].set_title("FS currents")
    axs[0,1].set_title("SOM currents")
    axs[0,2].set_title("HVA PY currents")
    for i,f in enumerate(filenames):
        with open(f, 'rb') as open_f:
            net = pickle.load(open_f)
            # print(net.keys())
            # print(net['afferent_spike_mon'])
            hva_v_mon = [x[neuron_index] for x in net['HVA_PY_V_mon']['V']]
            fs_v_mon = [x[neuron_index] for x in net['FS_V_mon']['V']]
            som_v_mon = [x[neuron_index] for x in net['SOM_V_mon']['V']]
            hva_t_mon = net['HVA_PY_V_mon']['t']
            fs_t_mon = net['FS_V_mon']['t']
            som_t_mon = net['SOM_V_mon']['t']
            hva_ge_mon = [x[neuron_index] for x in net['HVA_PY_Ge_total_mon']['Ge_total']]
            fs_ge_mon = [x[neuron_index] for x in net['FS_Ge_total_mon']['Ge_total']]
            som_ge_mon = [x[neuron_index] for x in net['SOM_Ge_total_mon']['Ge_total']]
            hva_gi_mon = [x[neuron_index] for x in net['HVA_PY_Gi_total_mon']['Gi_total']]
            fs_gi_mon = [x[neuron_index] for x in net['FS_Gi_total_mon']['Gi_total']]
            som_gi_mon = [x[neuron_index] for x in net['SOM_Gi_total_mon']['Gi_total']]
            # axs[i,neuron_index].plot(hva_t_mon/ms, hva_v_mon, 'black')
            axs[i,neuron_index].plot(hva_t_mon/ms, hva_ge_mon, 'red')
            # axs[i,neuron_index].plot(hva_t_mon/ms, hva_gi_mon, 'blue')

            # axs[i,1].plot(fs_t_mon/ms, fs_v_mon, 'black')
            axs[i,1].plot(fs_t_mon/ms, fs_ge_mon, 'red')
            # axs[i,1].plot(fs_t_mon/ms, fs_gi_mon, 'blue')

            # axs[i,2].plot(som_t_mon/ms, som_v_mon, 'black')
            axs[i,2].plot(som_t_mon/ms, som_ge_mon, 'red') 
            # axs[i,2].plot(som_t_mon/ms, som_gi_mon, 'blue')
    plt.show()

def extract_presynaptic_spikes(filename, neuron_type, neuron_index):
    """
    Extract out presynaptic spike times for a specific neuron index 
    Pass in an already-run network
    """
    with open(filename, 'rb') as open_f:
        net = pickle.load(open_f)
    if neuron_type == "FS":
        S = net['afferents_FS_synapse']
    if neuron_type == "SOM":
        S = net['afferents_SOM_synapse']
    if neuron_type == "HVA_PY":
        S = net['afferents_HVA_PY_synapse']
    a_spikes = net["afferent_spike_mon"]
    presyn_indices = []
    for i,j in zip(S['i'], S['j']):
        if j == neuron_index: presyn_indices.append(i)
    presyn_spike_times= []
    for n, time in zip(a_spikes['i'], a_spikes['t']):
        if n in presyn_indices:
            presyn_spike_times.append(time)
    print(presyn_spike_times)
    return presyn_spike_times


def pulse_ratio_plot(pickle_file, neuron_type):

    pass


def global_peak_trough_ratio(pickle_file, neuron_type, neuron_index):
    """
    Find global peak to trough ratio by taking difference of min and max
    value for the second half of the simulation 

    valid neuron_type names = "FS", "SOM", "HVA_PY"
    """

    with open(pickle_file, 'rb') as open_f:
        net = pickle.load(open_f)
        # print(net.keys())
        # print(net['afferent_spike_mon'])
    if neuron_type == "FS":
        mon = [x[neuron_index] for x in net['FS_V_mon']['V']]
    if neuron_type == "SOM":
        mon = [x[neuron_index] for x in net['SOM_V_mon']['V']]
    if neuron_type == "HVA_PY":
        mon = [x[neuron_index] for x in net['HVA_PY_V_mon']['V']]
    
    plt.title("{} PPR".format(neuron_type))
    # cut out first half of simulation
    halfway = len(mon)//2
    mon = mon[halfway:]
    max_v = max(mon)
    min_v = min(mon)
    peak_to_trough = math.fabs(max_v - min_v)
    print(peak_to_trough)
    return peak_to_trough

def unpickle_net(pickle_file):
    with open(pickle_file, 'rb') as open_f:
        net = pickle.load(open_f)
    return net


def average_values(pickle_file, value, neuron_type):
    """
    valid value names = "Ge", "Gi", "V"
    valid neuron_type names = "FS", "SOM", "HVA_PY"
    """
    net = unpickle_net(pickle_file)
    if value == 'Ge':
        key = "{}_Ge_total_mon".format(neuron_type)
        key2 = "Ge_total"
    if value == 'Gi':
        key = "{}_Gi_total_mon".format(neuron_type)
        key2 = "Gi_total"
    if value == 'V':
        key = "{}_V_mon".format(neuron_type)
        key2 = "V"
    total_arr = np.array(net[key][key2])
    averages = np.mean(total_arr, axis=1)
    print(averages)
    # print(averages)
    return averages

# extract_presynaptic_spikes("../networks/run_0.p", "SOM",0)
# plot_everything(["../networks/run_0.p"])
# global_peak_trough_ratio("../networks/run_0.p", "HVA_PY")
# global_peak_trough_ratio("../networks/run_0.p", "FS")
# global_peak_trough_ratio("../networks/run_0.p", "SOM")
# n = unpickle_net("../networks/run_0.p")
average_values("../networks/run_0.p", "V", "FS")


# this function is not all that useful honestly

# def raster_plot(pickled_file, neuron_type):
    # """
    # Compare responses of 3 neurons when drawing randomly from a set of
    # firing afferents 

    # Valid neuron types = "FS", "SOM", "HVA_PY"

    # **note** ->
    # network passed in must have N:3 for the given neuron_type
    # """
    # with open(filename, 'rb') as open_f:
        # net = pickle.load(open_f)
    # print(net)
    # f, axs = plt.subplots(2,3, sharex=True, sharey=True)
    # if neuron_type == "FS":
        # S = net['afferents_FS_synapse']
        # fs_v_mon = net['FS_V_mon']
        # axs[0,0].plot(fs_v_mon.t/ms, fs_v_mon.V[0], 'black')
        # axs[0,1].plot(fs_v_mon.t/ms, fs_v_mon.V[1], 'black')
        # axs[0,2].plot(fs_v_mon.t/ms, fs_v_mon.V[2], 'black')
    # if neuron_type == "SOM":
        # S = net['afferents_SOM_synapse']
        # som_v_mon = net['SOM_V_mon']
        # axs[0,0].plot(som_v_mon.t/ms, som_v_mon.V[0], 'black')
        # axs[0,1].plot(som_v_mon.t/ms, som_v_mon.V[1], 'black')
        # axs[0,2].plot(som_v_mon.t/ms, som_v_mon.V[2], 'black')
    # if neuron_type == "HVA_PY":
        # S = net['afferents_HVA_PY_synapse']
        # hva_py_v_mon = net['HVA_PY_V_mon']
        # axs[0,0].plot(hva_py_v_mon.t/ms, hva_py_v_mon.V[0], 'black')
        # axs[0,1].plot(hva_py_v_mon.t/ms, hva_py_v_mon.V[1], 'black')
        # axs[0,2].plot(hva_py_v_mon.t/ms, hva_py_v_mon.V[2], 'black')
    # a_spikes = net["afferent_spike_mon"]
    # # brian_plot(a_spikes)
    # # plt.show()
    # neuron_1 = []
    # neuron_2 = []
    # neuron_3 = []
    # for i,j in zip(S.i, S.j):
        # # print("{} is connected to {}".format(i, j))
        # if j == 0: neuron_1.append(i)
        # if j == 1: neuron_2.append(i)
        # if j == 2: neuron_3.append(i)
    # neuron_1_i = []
    # neuron_1_t = []
    # neuron_2_i = []
    # neuron_2_t = []
    # neuron_3_i = []
    # neuron_3_t = []
    # for k, j in zip(a_spikes.i, a_spikes.t):
        # # print("Neuron {} spiked at time {}".format(k,j))
        # if k in neuron_1:
            # neuron_1_i.append(k)
            # neuron_1_t.append(j)
        # if k in neuron_2:
            # neuron_2_i.append(k)
            # neuron_2_t.append(j)
        # if k in neuron_3:
            # neuron_3_i.append(k)
            # neuron_3_t.append(j)
    # for i in range(len(neuron_1)):
        # axs[1,0].plot(neuron_1_t, neuron_1_i, 'o')
    # for i in range(len(neuron_2)):
        # axs[1,1].plot(neuron_2_t, neuron_2_i, 'o')
    # for i in range(len(neuron_3)):
        # axs[1,2].plot(neuron_3_t, neuron_3_i, 'o')

    # plt.show()

