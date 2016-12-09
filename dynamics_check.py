from brian2 import *
from PY_FS_SOM_neurons_init import *

# spikes = make_spike_generator(1, np.arange(0.01, 1, 0.01)*second)
spikes = make_spike_generator(1, np.arange(0.01, 1, 0.3)*second)

# create synapses between spike generator groups and the neurons

S_P_PY = make_synapse(spikes, PY_group, '''
                                                epsp = epsp0*D
                                                v_post += epsp
                                                D *= d_rate
                                                ''')

S_P_FS = make_synapse(spikes, FS_group,  '''
                                                epsp = epsp0*D
                                                v_post += epsp
                                                D *= d_rate
                                                ''')

S_P_SOM = make_synapse(spikes, SOM_group, '''
                                                epsp = epsp0*F
                                                v_post += epsp
                                                F += f_rate
                                                ''')
connect_synapse(S_P_PY)
connect_synapse(S_P_FS)
connect_synapse(S_P_SOM)

# visualise_connectivity(S_P_PY)
mon_gen_input = SpikeMonitor(spikes)
mon_PY = StateMonitor(PY_group, 'epsp', record=True)
mon_FS = StateMonitor(FS_group, 'epsp', record=True)
mon_SOM = StateMonitor(SOM_group, 'epsp', record=True)
mon_vPY = StateMonitor(PY_group, 'v', record=True)
mon_vFS = StateMonitor(FS_group, 'v', record=True)
mon_vSOM = StateMonitor(SOM_group, 'v', record=True)
mon_DPY = StateMonitor(PY_group, 'D', record=True)
spikes_PY = SpikeMonitor(PY_group)
spikes_FS = SpikeMonitor(FS_group)
spikes_SOM = SpikeMonitor(SOM_group)

run(.5*second)

# print(mon_DPY.D[0])
plot_input_with_3_groups(mon_gen_input, mon_vPY, spikes_PY, mon_vFS,
        spikes_FS, mon_vSOM, spikes_SOM, "Membrane Potential", 
        "PY MP (v)", "FS MP (v)", "SOM MP (v)", -0.083, -0.05)
