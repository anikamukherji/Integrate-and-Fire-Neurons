
# These are a set of equations that can be used to implement
# both depression and facilitation without having to control
# conductances.
# The changes in MP calculated directly by the values of epsp0 (RMP) 
# and the values of F and D
# F is implemented as additive, and D as multiplicative

equations = 
'''
    dv/dt = (Vm - v)/tau_m : volt (unless refractory)
    Vm : volt
    tau_m : second
    epsp0 : volt
    epsp : volt

    dD/dt = (1-D)/tau_d : 1 
    dF/dt = (1-F)/tau_f : 1
    tau_f : second
    tau_d : second
    d_rate : 1
    f_rate : 1 
 '''

synapse_eqs = 
'''
    epsp = epsp0*D*F
    v_post += epsp
    D *= d_rate
    F += f_rate
''' 
