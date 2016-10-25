import matplotlib.pyplot as plt
import numpy as np

T = 150                             # total simulation time (millisecond)
dt = 0.125                          # time step (millisecond)
Rm = 7                              # resistance (megaOhm)
Cm = 1                              # capacitance (microFaraday/cm^2)
tau_m = Rm * Cm                     # time membrane constant
times = np.arange(0, T+dt, dt)      # time step array
inputCurrentStart = 0
inputCurrentEnd = 100
inputCurrentLen = (inputCurrentEnd - inputCurrentStart) / dt
current = 1                         # default input current (nanoAmpere)
Vm = np.zeros(len(times))           # initializing array of membrane potentials


def makeinputarray(currStart, currEnd, current, times):

    inputarray = np.zeros(len(times))
    inputarray[(currStart/dt):(currEnd/dt)] = current
    return inputarray


def calcVoltages(Vm, inputarray, tau_m, Rm, dt, times):

    for i, t in enumerate(times):
        I = inputarray[i]
        Vm[i] = Vm[i - 1] + (dt / tau_m) * ((-1 * Vm[i - 1]) + I * Rm)

    return Vm


def plotcurrrange(Vm, Rm, tau_m, lowerCurr, upperCurr, currStep,
                  currStart, currEnd, times, dt, T):

    plt.figure(1)
    plt.title("Passive Membrane Model")
    plt.xlabel("Time (ms)")
    plt.ylabel("Membrane Voltage (mV)")
    plt.ylim(-10, 10)
    plt.xlim(0, T)
    currentrange = np.arange(lowerCurr, upperCurr + currStep, currStep)

    for x in currentrange:

        inputs = makeinputarray(currStart, currEnd, x, times)

        Vm = calcVoltages(Vm, inputs, tau_m, Rm, dt, times)

        plt.plot(times, Vm, "#ff0066")

    plt.show()
    return



plotcurrrange(Vm, Rm, tau_m, -1, 1, 0.2, 0, 100, times, dt, T)



