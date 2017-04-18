
from brian2tools import *
from brian2 import units
import matplotlib.pyplot as plt
import dill as pickle
import math

########################################################################
# this file will be used to plot and compute various analyses of the data
# from pickled networks
########################################################################


def unpickle_net(pickle_file):
    """
    Unpickle a file and return its contents a mega-dictionary 
    of all the monitored states during that run
    """
    with open(pickle_file, 'rb') as open_f:
        net = pickle.load(open_f)
    return net


def plot_everything(filenames, neuron_index=0):
    """
    Plots voltage, excitatory conductance and/or inhibitory conductance
    from HVA_PY, SOM, and FS cells
    Plots values from neuron 0 by default
    """
    f, axs = plt.subplots(len(filenames), 3)
    axs[0,0].set_title("HVA PY currents")
    axs[0,1].set_title("FS currents")
    axs[0,2].set_title("SOM currents")
    for i,f in enumerate(filenames):
        net = unpickle_net(f)
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
        axs[i,0].plot(hva_t_mon, hva_v_mon, 'black')
        # axs[i,0].plot(hva_t_mon, hva_ge_mon, 'red')
        # axs[i,0].plot(hva_t_mon, hva_gi_mon, 'blue')

        axs[i,1].plot(fs_t_mon, fs_v_mon, 'black')
        # axs[i,1].plot(fs_t_mon, fs_ge_mon, 'red')
        # axs[i,1].plot(fs_t_mon, fs_gi_mon, 'blue')

        axs[i,2].plot(som_t_mon, som_v_mon, 'black')
        # axs[i,2].plot(som_t_mon, som_ge_mon, 'red') 
        # axs[i,2].plot(som_t_mon/ms, som_gi_mon, 'blue')
    plt.show()

def extract_presynaptic_spikes(filename, neuron_type, neuron_index, net=None):
    """
    Extract out presynaptic spike times for a specific neuron index 
    Pass in an already-run network
    """
    if net == None:
        net = unpickle_net(filename)
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
    
    # print(presyn_spike_times)
    return presyn_spike_times


def pulse_ratio(pickle_file, neuron_type, neuron_index, var):
    """
    Compare some variable at spike times to its value at the first spike

    valid neuron_type names = "FS", "SOM", "HVA_PY"
    """

    net = unpickle_net(pickle_file)
    
    spike_times = extract_presynaptic_spikes(pickle_file, neuron_type, neuron_index, net)
    # print(spike_times)
    if var == "V":
        mon = [x[neuron_index]/volt for x in net['{}_V_mon'.format(neuron_type)]['V']]
    if var == "Ge":
        mon = [x[neuron_index] for x in net['{}_Ge_total_mon'.format(neuron_type)]['Ge_total']]
    if var == "Gi":
        mon = [x[neuron_index] for x in net['{}_Gi_total_mon'.format(neuron_type)]['Gi_total']]

    responses = extract_responses(spike_times, mon)
    PPR = [float(x)/float(responses[0]) for x in responses]
    print(PPR)
    return responses 

def extract_responses(spike_times, mon):
    """
    time 0 = 0th index
    1st index = 0.1 ms into simulation
    if you want value at 400 ms -> 4000 index
    keep in mind that 400 ms = 0.4 seconds
    So seconds to index -> seconds x 10000
    """

    # we don't care if there are a bunch of afferents all firing together
    spike_times = sorted(list(set(spike_times/second)))
    responses = []

    for i,t in enumerate(spike_times):
        # get rid of pesky units
        t = t/second
        # use floor in case of precision wackiness
        spike_index = math.floor(t*10000)

        # get baseline right before spike
        if t == 0:
            before = mon[0]
        else:
            before = np.mean(np.array(mon[spike_index-10:spike_index+1]))

        # get max value after the spike 
        if i+ 1 != len(spike_times):
            next_spike_index = math.floor(spike_times[i+1]*10000)
            after = max(np.array(mon[spike_index:next_spike_index]))
        else:
            after = max(np.array(mon[spike_index:]))

        diff = math.fabs(after - before)
        responses.append(diff)
    return responses

def global_peak_trough_ratio(pickle_file, neuron_type, neuron_index):
    """
    Find global peak to trough ratio by taking difference of min and max
    value for the second half of the simulation 

    valid neuron_type names = "FS", "SOM", "HVA_PY"
    """

    net = unpickle_net(pickle_file)
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
    # print(peak_to_trough)
    return peak_to_trough



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

# global_peak_trough_ratio("../networks/run_0.p", "HVA_PY")
# global_peak_trough_ratio("../networks/run_0.p", "FS")
# global_peak_trough_ratio("../networks/run_0.p", "SOM")
# n = unpickle_net("../networks/run_0.p")
# average_values("../networks/run_0.p", "V", "FS")
# pulse_ratio_plot("../networks/run_0_30-03-2017.p", "SOM", 1)
plot_everything(["../networks/run_0_17-04-2017.p",
    "../networks/run_1_17-04-2017.p",
    "../networks/run_2_17-04-2017.p"])
# pulse_ratio("../networks/run_2_30-03-2017.p", "FS",0, "V")
# pulse_ratio("../networks/run_2_30-03-2017.p", "SOM",0, "V")


# this function is not all that useful honestly


