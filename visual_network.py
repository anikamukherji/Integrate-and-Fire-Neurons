from brian2 import *
from PY_FS_SOM_neurons_init import *

poisson_input = make_poisson_input(20, '20*sin(t*(2*pi)*3/second)*Hz')

# create synapses between poisson input group and the others

S_P_PY = make_synapse(poisson_input, PY_group, '''
                                                v_post += epsp
                                                epsp *= d_rate
                                                ''')

S_P_FS = make_synapse(poisson_input, FS_group,  '''
                                                v_post += epsp
                                                epsp *= d_rate
                                                ''')

S_P_SOM = make_synapse(poisson_input, SOM_group, '''
                                                v_post += epsp
                                                epsp += f_rate                                                                                           ''')

connect_synapse(S_P_PY)
connect_synapse(S_P_FS)
connect_synapse(S_P_SOM)

# record membrane voltages and spikes

mon_poisson_input = SpikeMonitor(poisson_input)
mon_PY = StateMonitor(PY_group, 'v', record=True)
spikes_PY = SpikeMonitor(PY_group)
mon_FS = StateMonitor(FS_group, 'v', record=True)
spikes_FS = SpikeMonitor(FS_group)
mon_SOM = StateMonitor(SOM_group, 'v', record=True)
spikes_SOM = SpikeMonitor(SOM_group)

run(1*second)

# print('PY Neuron 1 Voltages= ', mon_PY.v[0][0:20])
# print('FS Neuron 1 Voltages= ', mon_FS.v[0][0:20])
# print('SOM Neuron 1 Voltages=', mon_SOM.v[0][0:20])


plot_input_with_3_groups(mon_poisson_input, mon_PY, spikes_PY, 
        mon_FS, spikes_FS, mon_SOM, spikes_SOM, 'Poisson Inputs into PY, FS, and SOM neurons', 'PY Neurons MP (v)', 'FS Neurons MP (v)',
        'SOM Neurons MP (v)')
