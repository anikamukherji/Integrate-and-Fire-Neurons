import matplotlib.pyplot as plt
import numpy as np

# simulates and plots spiking neuronal membrane
# membrane voltage = 0 represents resting membrane potential


T = 40                              # total simulation time
dt = 0.125                          # time step
Rm = 1                              # resistance
Cm = 10                             # capacitance
tau_m = Rm * Cm                     # time membrane constant
times = np.arange(0, T+dt, dt)      # time step array
inputCurrentStart = 0
inputCurrentEnd = 13
inputCurrentLen = (inputCurrentEnd - inputCurrentStart) / dt
current = 70
inputarray = np.zeros(len(times))
inputarray[inputCurrentStart:inputCurrentLen] = current

Vm = [0]*(len(times))
tau_r = 1.5                         # refractory period
t_rest = 0                          # initial refractory time
Vt = 30                             # spike threshold
V_spike = 110                       # spike delta
Vh = -20                            # hyperpolarized state

for i, t in enumerate(times):

    if t > t_rest:
        I = current if (t < inputCurrentEnd and t > inputCurrentStart) else 0
        Vm[i] = Vm[i-1] + (dt/tau_m)*((-1*Vm[i-1]) + I*Rm)
    if Vm[i] > Vt:
        Vm[i] += V_spike
        t_rest = t + tau_r
        if i < len(Vm) - 1:
            Vm[i+1] = Vh


plt.figure(1)
plt.plot(times, Vm)
plt.plot(times, inputarray)
plt.title("Leaky Integrate and Fire Neuron With Spikes")
plt.xlabel("Time (ms)")
plt.ylabel("Membrane Voltage (mV)")
plt.ylim(-30, 150)
plt.show()
