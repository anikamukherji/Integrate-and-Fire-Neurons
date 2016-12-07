def sim_caller(N, time, input_frequency=[50]*10, n_input=[20]*10, n_PY=[20]*10, n_FS=[20]*10,
        n_SOM=[20]*10, PY_Vm=[-0.08]*10, FS_Vm=[-0.065]*10, SOM_Vm=[-0.065]*10,
        PY_tau_m=[0.02]*10, FS_tau_m=[0.015]*10, SOM_tau_m=[0.012]*10,
        PY_epsp0=[0.005]*10, FS_epsp0=[0.007]*10, SOM_epsp0=[0.0005]*10, PY_d=[0.85]*10, FS_d=[0.55]*10, 
        SOM_f=[0.12]*10, PY_tau_d=[0.58]*10, FS_tau_d=[0.32]*10, SOM_tau_d=[0.02]*10) --> None:


    # take in a bunch of parameters 
    # take in N for num of simulations
    # format each parameter to match num of simulations
    for i_sim in range(N):

        # build a dictionary for the parameter set for that run
        param_dict = {"input_frequency":input_frequency[i_sim], "n_input":n_input[i_sim],
                "n_PY":n_PY[i_sim], "n_FS":n_FS[i_sim], "n_SOM":n_SOM[i_sim], 
                "PY_Vm":PY_Vm[i_sim], "FS_Vm":FS_Vm[i_sim], "SOM_Vm":SOM_Vm[i_sim],
                "PY_tau_m":PY_tau_m[i_sim], "FS_tau_m":FS_tau_m[i_sim], "SOM_tau_m":SOM_tau_m[i_sim],
                "PY_epsp0":PY_epsp0[i_sim], "FS_epsp0":FS_epsp0[i_sim],
                "SOM_epsp0":SOM_epsp0, "PY_d":PY_d[i_sim], "FS_d":FS_d[i_sim],
                "SOM_f":SOM_f[i_sim], "PY_tau_d":PY_tau_d[i_sim], "FS_tau_d":FS_tau_d,
                "SOM_tau_f":SOM_tau_d[i_sim]}
        # call run_simulation
        run_simulation(param_dict, time)
        # save return argument somewhere

def run_simulation(arg_dict, time) --> dict:


    # Run simulation for time according to params from the dict
    # Return dict = 
        # spike_nums : 1 ... N
        # PY_epsp, FS_epsp, SOM_epsp
