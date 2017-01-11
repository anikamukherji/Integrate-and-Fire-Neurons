from PY_FS_SOM_neurons_init import *

def sim_caller(N, time, input_frequency=[50]*10, n_input=[20]*10, n_PY=[20]*10, n_FS=[20]*10,
        n_SOM=[20]*10, PY_Vm=[-0.08]*10, FS_Vm=[-0.065]*10, SOM_Vm=[-0.065]*10,
        PY_tau_m=[0.02]*10, FS_tau_m=[0.015]*10, SOM_tau_m=[0.012]*10,
        PY_epsp0=[0.005]*10, FS_epsp0=[0.007]*10, SOM_epsp0=[0.0005]*10, PY_d=[0.85]*10, FS_d=[0.55]*10, 
        SOM_f=[0.12]*10, PY_tau_d=[0.58]*10, FS_tau_d=[0.32]*10, SOM_tau_d=[0.02]*10) -> dict:
    # TODO convert to params_all_sims dictionary that exists above the caller in "test_simulations.py" check with fxn

    ret = {0:0} # TODO can this be initialized as "ret = {}". Is ret[0] going to be a pain down the road?
    # take in a bunch of parameters 
    # take in N for num of simulations
    # format each parameter to match num of simulations
    for i_sim in range(1, N+1):
        print("Sim # ", i_sim)
        # build a dictionary for the parameter set for that run
        # TODO use list comprehension to quickly build this based on the keys from params_all_sims
        param_dict = {"input_frequency":input_frequency[i_sim], "n_input":n_input[i_sim],
                "n_PY":n_PY[i_sim], "n_FS":n_FS[i_sim], "n_SOM":n_SOM[i_sim], 
                "PY_Vm":PY_Vm[i_sim], "FS_Vm":FS_Vm[i_sim], "SOM_Vm":SOM_Vm[i_sim],
                "PY_tau_m":PY_tau_m[i_sim], "FS_tau_m":FS_tau_m[i_sim], "SOM_tau_m":SOM_tau_m[i_sim],
                "PY_epsp0":PY_epsp0[i_sim], "FS_epsp0":FS_epsp0[i_sim],
                "SOM_epsp0":SOM_epsp0[i_sim], "PY_d":PY_d[i_sim], "FS_d":FS_d[i_sim],
                "SOM_f":SOM_f[i_sim], "PY_tau_d":PY_tau_d[i_sim], "FS_tau_d":FS_tau_d[i_sim],
                "SOM_tau_f":SOM_tau_d[i_sim]}
        # call run_simulation
        net = init_net(param_dict, time)
        sim_dict = run_simulation(net, time)
        # print(param_dict)
        # save return argument somewhere
        ret[i_sim] = sim_dict

def run_simulation(network, time) -> dict:
    # TODO what's up with start_scope() in Brian2, and is it useful here?
    network.restore("initial")
    net_objects = network.objects

    # Run simulation for time according to params from the dict
    # TODO where does network t=0 get initialized, or is this persisting from run to run?
    network.run(time)

    net_objects = network.objects
    # index 5 of objects stores SOM F monitor
    # index 4 stores FS D monitor
    # index 3 stores PY D monitor
    
    # Return dict =
    PY_vals = network.PY_D_mon.D[0]*network.PY_g.epsp0[0]
    FS_vals = network.FS_D_mon.D[0]*network.FS_g.epsp0[0]
    SOM_vals = network.SOM_F_mon.F[0]*network.SOM_g.epsp0[0]
    # print(PY_vals)
    # print(FS_vals)
    # print(SOM_vals)
    PY_arr = [0]*len(network.spike_monitor.t[:])
    FS_arr = [0]*len(network.spike_monitor.t[:])
    SOM_arr = [0]*len(network.spike_monitor.t[:])

    for i in range(len(network.spike_monitor.t[:])):
        spike_t = network.spike_monitor.t[i]
        PY_arr[i] = PY_vals[spike_t/(0.1*msecond)]  # TODO variable dt instead of hardcoded 0.001 (here and elsewhere)
        FS_arr[i] = FS_vals[spike_t/(0.1*msecond)]  # TODO consider +1 to floor division (x//y)+1, or ceiling round: -(-x//y)
        SOM_arr[i] = SOM_vals[spike_t/(0.1*msecond)] # TODO also consider an "event monitor" to grab EPSPs automatically

    epsp_dict = {"PY_EPSP":PY_vals, "FS_EPSP":FS_vals, "SOM_EPSP":SOM_vals}
    pulses = np.arange(1, len(network.spike_monitor.t[:])+1)
    epsp_dict["pulse_num"]=pulses
    print("dict for this sim= ", epsp_dict)

    return epsp_dict  # TODO where does this epsp_dict get called? also, strictly speaking it does not appear to be EPSPs but rather Ds and Fs?

def init_net(arg_dict, time):
    
    sim_net = Network()
    input_g = make_spike_generator(arg_dict["n_input"], np.arange(0*second, time, 1/arg_dict["input_frequency"]*second))  # TODO is one call to "second" sufficient (here and elsewhere)?
    # poisson_g = make_input_g(arg_dict["n_input"], arg_dict["input_frequency"])
    # TODO consider using method='euler' instead of method='linear'?
    PY_g = make_neuron_group(arg_dict["n_PY"], 'v>-0.045*volt', 'v=-0.05*volt', eqs, 0.003*second, 'linear')
    FS_g = make_neuron_group(arg_dict["n_FS"], 'v>-0.045*volt', 'v=-0.05*volt', eqs, 0.003*second, 'linear')
    SOM_g = make_neuron_group(arg_dict["n_SOM"], 'v>-0.045*volt', 'v=-0.05*volt', eqs, 0.003*second, 'linear')
    sim_net.add(input_g)
    sim_net.add(PY_g)
    sim_net.add(FS_g)
    sim_net.add(SOM_g)
    print("Dict for current simulation = ", arg_dict)
    # initialize lots of vars for simulation
    PY_g.v = arg_dict["PY_Vm"]*volt 
    PY_g.Vm = arg_dict["PY_Vm"]*volt # TODO .Vm .tau_m .epsp0 .epsp are "per neruon" params. is this assignment sufficient for the whole network? see Brian tutorial
    PY_g.tau_m =arg_dict["PY_tau_m"]*second
    PY_g.epsp0 =arg_dict["PY_epsp0"]*volt
    PY_g.epsp =arg_dict["PY_epsp0"]*volt
    PY_g.tau_d =arg_dict["PY_tau_d"]*second
    PY_g.D = 1
    PY_g.d_rate =arg_dict["PY_d"]

    FS_g.v = arg_dict["FS_Vm"]*volt
    FS_g.Vm = arg_dict["FS_Vm"]*volt
    FS_g.tau_m =arg_dict["FS_tau_m"]*second
    FS_g.epsp0 =arg_dict["FS_epsp0"]*volt
    FS_g.epsp =arg_dict["FS_epsp0"]*volt
    FS_g.tau_d =arg_dict["FS_tau_d"]*second
    FS_g.D = 1
    FS_g.d_rate =arg_dict["FS_d"]

    SOM_g.v = arg_dict["SOM_Vm"]*volt
    SOM_g.Vm = arg_dict["SOM_Vm"]*volt
    SOM_g.tau_m =arg_dict["SOM_tau_m"]*second
    SOM_g.epsp0 =arg_dict["SOM_epsp0"]*volt
    SOM_g.epsp =arg_dict["SOM_epsp0"]*volt
    SOM_g.tau_f =arg_dict["SOM_tau_f"]*second
    SOM_g.F = 1
    SOM_g.f_rate =arg_dict["SOM_f"]

    # synapses
    syn_PY = make_synapse(input_g, PY_g, '''
                                        epsp = epsp0*D
                                        v_post += epsp
                                        D *= d_rate
                                        ''')

    syn_FS = make_synapse(input_g, FS_g,  '''
                                        epsp = epsp0*D
                                        v_post += epsp
                                        D *= d_rate
                                        ''')

    syn_SOM = make_synapse(input_g, SOM_g, '''
                                        epsp = epsp*F
                                        v_post += epsp
                                        F += f_rate
                                        ''')
    connect_synapse(syn_PY)
    connect_synapse(syn_FS)
    connect_synapse(syn_SOM)
    
    sim_net.add(syn_PY)
    sim_net.add(syn_FS)
    sim_net.add(syn_SOM)

    spike_monitor = SpikeMonitor(input_g)
    PY_D_mon = StateMonitor(PY_g, 'D', record=True) #TODO if all neurons are identical, consider record=0, but for scalability keep True?
    FS_D_mon = StateMonitor(FS_g, 'D', record=True) # TODO if state variables for STP are in SynapseGroup instead of NeuronGroup, can we add them here explictly?
    SOM_F_mon = StateMonitor(SOM_g, 'F', record=True)

    sim_net.add(spike_monitor)
    sim_net.add(PY_D_mon)
    sim_net.add(FS_D_mon)
    sim_net.add(SOM_F_mon)

    sim_net.store("initial")
    return sim_net


# General To-do but not important now
# TODO add delays to synaptic connections if not already present
# TODO add recurrent connections between FS, SOM, PY cells.
# TODO check the params for each cell type to see that they do the correct thing (DC injections, STP)
# TODO add spike-rate adaptation by playing with the "refractory" period (least important)