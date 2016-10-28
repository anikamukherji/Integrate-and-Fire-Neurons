from brian import *
import numpy as np



def drange(start, stop, step):
    r = start
    while r < stop:
        yield r
        r += step


Vt = -40 * mV
Vm = -75 * mV
Vr = -45 * mV
Rm = 7 * Mohm
Cm = 1 * ufarad

tau_m = (Rm * Cm)

inputs = list(drange(-1.0, 1.2, 0.2))
n = NeuronGroup(N=11, model='''dv/dt=((-1*v) + I*Rm)/tau_m : mV
                                I : namp
                            ''',
                threshold=Vt, reset=Vr,
                refractory=0.5 * msecond)
n.v = Vm

for t, i in enumerate(inputs):

    index = int(t)
    n[t].I = i * namp

for i in range(11):
    print "current =", n[i].I, "neuron #=", i

M = StateMonitor(n, 'v', record=True)
S = SpikeMonitor(n)

run(10 * second)

print(M[0])

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

print S.nspikes

M.insert_spikes(S)

ylim(-0.1, 0)
xlabel("Time")
ylabel("Membrane Potential")
show()

raster_plot(S)
show()
