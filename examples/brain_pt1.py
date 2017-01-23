# Was using brian1 here, so the program won't run property with brian2

from brian import *
import numpy as np


Vt = -40 * mV
Vm = -75 * mV
Vr = -45 * mV
Rm = 36 * Mohm
Cm = .001 * ufarad

tau_m = (Rm * Cm)

inputs = list(drange(-1.0, 1.2, 0.2))
n = NeuronGroup(N=11, model='''dv/dt=((Vm - v) + I*Rm)/tau_m : mV
                                I : namp
                            ''',
                threshold=Vt, reset=Vr,
                refractory=1 * msecond)
n.v = Vm

for t, i in enumerate(inputs):

    index = int(t)
    n[t].I = TimedArray([0 * namp, i * namp, i * namp, 0 * namp],
                        dt=500 * msecond)

# for i in range(11):
#     print "current =", n[i].I, "neuron #=", i

M = StateMonitor(n, 'v', record=True)
S = SpikeMonitor(n)

run(2 * second)

# print("Neuron 0 Vms = ", M[0])
# print("Neuron 0 I*Rm = ", n[0].I * Rm)
M.insert_spikes(S)

plot(M.times, M[0])
plot(M.times, M[1])
plot(M.times, M[2])
plot(M.times, M[3])
plot(M.times, M[4])
plot(M.times, M[5])
plot(M.times, M[6])
plot(M.times, M[7])
plot(M.times, M[8])
plot(M.times, M[9])
plot(M.times, M[10])

# print S.nspikes

ylim(-0.15, 0.04)
xlabel("Time")
ylabel("Membrane Potential")
show()
