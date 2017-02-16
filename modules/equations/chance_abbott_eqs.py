
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
    dD1/dt = (1 - D1)/tau_D1 : 1 (clock-driven)
    dD2/dt = (1 - D2)/tau_D2 : 1 (clock-driven)
    dF1/dt = (1 - F1)/tau_F1 : 1 (clock-driven)
    dF2/dt = (1 - F2)/tau_F2 : 1 (clock-driven)
    tau_e : second
    tau_i : second
    tau_D1 : second
    tau_D2 : second
    tau_F1 : second
    tau_F2 : second
    d1 : 1
    d2 : 1
    f1 : 1
    f2 : 1
    w_e : 1 
    w_i : 1
     '''

# On spikes the excitatory and inhibitory conductance from each 
# synapse get added to the total excitatory and inhibitory 
# conductance of the model cell
# Depression and faciliation factors get incremented/decremented 
# by their respective constants

onspike_eqs = '''
    G_e += w_e*D1*D2*F1*F2
    Ge_total_post += G_e
    G_i += w_i*D1*D2*F1*F2 
    Gi_total_post += G_i
    D1 *= d1
    D2 *= d2
    F1 += f1
    F2 += f2 
    '''
