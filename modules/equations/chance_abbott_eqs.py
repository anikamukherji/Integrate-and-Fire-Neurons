
# contains equations for Chance, Nelson & Abbott's (1998) synaptic dynamics
# uses excitatory and inhibitory conductances to calculate MP
# V0 is RMP
# Ve/Vi are reversal potentials for excitation/inhibition
# Ge/Gi_total are excitatory/inhibitory conductances that decay to 0

neuron_eqs = '''
    dV/dt = (V0 - V + Ge_total*(Ve - V) + Gi_total*(Vi - V))/tau_m : volt
    dGe_total/dt = (-Ge_total)/tau_e_model : 1
    dGi_total/dt = (-Gi_total)/tau_i_model : 1
    tau_m : second
    tau_e_model : second
    tau_i_model : second
    Ve : volt
    Vi : volt
    V0 : volt
    '''


# Each synapse has its own depression factor
# More than one depression constant may be used 
# For example, Chance, Nelson and Abbott tested a model with 
# a slow factor (for contrast adaptation) and a fast 
# factor (for temporal nonlinearities)
# Facilitation factors may also be added in similar way, but 
# are usually implemented as additive (rather than multiplicative)
# Conductances decay to 0, D decays to 1

synapse_eqs = '''
    dG_e/dt = (-G_e)/tau_e : 1 (clock-driven)
    dG_i/dt = (-G_i)/tau_i : 1 (clock-driven)
    dD/dt = (1 - D)/tau_D : 1 (clock-driven)
    tau_e : second
    tau_i : second
    tau_D : second
    d_fast : 1
    strength_e : 1 
    strength_i : 1
         '''

# On spikes the excitatory and inhibitory conductance from each 
# synapse get added to the total excitatory and inhibitory 
# conductance of the model cell
# D gets multiplied by the depression factor after

onspike_eqs = '''
    G_e += strength_e*D 
    Ge_total_post += G_e
    G_i += strength_i*D 
    Gi_total_post += G_i
    D = d_fast*D
            '''
