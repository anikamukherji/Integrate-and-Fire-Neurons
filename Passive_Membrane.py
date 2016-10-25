import matplotlib.pyplot as plt
import numpy as np

T = 150                             # total simulation time (millisecond)
dt = 0.125                          # time step (millisecond)
Rm = 30                             # resistance (megaOhm)
Cm = 1                              # capacitance (microFaraday/cm^2)
tau_m = Rm * Cm                     # time membrane constant
times = np.arange(0, T+dt, dt)      # time step array
inputCurrentStart = 0
inputCurrentEnd = 100
inputCurrentLen = (inputCurrentEnd - inputCurrentStart) / dt
current = 1                         # default input current (nanoAmpere)
Vm = np.zeros(len(times))           # initializing array of membrane potentials
                                    # in milliVolts
t_rest = 0                          # refractory period tracker var

plt.figure(1)
# plt.plot(times, inputarray, "#ffff00")
plt.title("Passive Membrane Model")
plt.xlabel("Time (ms)")
plt.ylabel("Membrane Voltage (mV)")
plt.ylim(-35, 35)
plt.xlim(0, T)

for x in range(-10, 10, 2):         # range of currents -1 to 1 nA with step of
                                    # 200 pA (divide by 10)
    current = float(x)/float(10)
    # inputarray = np.zeros(len(times))
    # inputarray[inputCurrentStart:inputCurrentLen] = current
    # print inputarray

    for i, t in enumerate(times):

        if t > t_rest:
            I = current if (t < inputCurrentEnd and t > inputCurrentStart) else 0
            Vm[i] = Vm[i-1] + (dt/tau_m)*((-1*Vm[i-1]) + I*Rm)

    plt.plot(times, Vm, "#ff0066")

plt.show()

