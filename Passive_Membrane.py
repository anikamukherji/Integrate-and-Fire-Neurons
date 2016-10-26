import matplotlib.pyplot as plt
import numpy as np

T = 150                             # total simulation time (millisecond)
dt = 0.125                          # time step (millisecond)
Rm = 7                              # resistance (megaOhm)
Cm = 1                              # capacitance (microFaraday/cm^2)
tau_m = Rm * Cm                     # time membrane constant
times = np.arange(0, T+dt, dt)      # time step array
input_current_start = 0
input_current_end = 100
input_current_len = (input_current_end - input_current_start) / dt
current = 1                         # default input current (nanoAmpere)
Vm = np.zeros(len(times))           # initializing array of membrane potentials


def make_input_array(curr_start, curr_end, current, times):

    input_array = np.zeros(len(times))
    input_array[(curr_start/dt):(curr_end/dt)] = current
    return input_array


def calc_voltages(Vm, input_array, tau_m, Rm, dt, times):

    for i, t in enumerate(times):
        I = input_array[i]
        Vm[i] = Vm[i - 1] + (dt / tau_m) * ((-1 * Vm[i - 1]) + I * Rm)

    return Vm


def plot_curr_range(Vm, Rm, tau_m, lower_curr, upper_curr, curr_step,
                  curr_start, curr_end, times, dt, T):

    plt.figure(1)
    plt.title("Passive Membrane Model")
    plt.xlabel("Time (ms)")
    plt.ylabel("Membrane Voltage (mV)")
    plt.ylim(-10, 10)
    plt.xlim(0, T)
    current_range = np.arange(lower_curr, upper_curr + curr_step, curr_step)

    for x in current_range:

        inputs = make_input_array(curr_start, curr_end, x, times)

        Vm = calc_voltages(Vm, inputs, tau_m, Rm, dt, times)

        plt.plot(times, Vm, "#ff0066")

    plt.show()


def plot_mV_vs_curr(currents, tau_m, Rm, dt, times):

    asymp = len(times) - 1
    plt.figure(1)
    plt.xlabel("Asymptotic Value (mV)")
    plt.ylabel("Current Injection (nA)")
    plt.ylim(currents[0], currents[-1])
    plt.xlim(currents[0]*Rm, currents[-1]*Rm)

    for i in currents:
        inputs = make_input_array(0, len(times), i, times)
        Vm = np.zeros(len(times))
        Vm = calc_voltages(Vm, inputs, tau_m, Rm, dt, times)
        # print "asymtope =" + str(Vm[asymp])
        # print "current=" + str(i)
        plt.scatter(Vm[asymp], i)

    plt.show()
    

plot_curr_range(Vm, Rm, tau_m, -1, 1, 0.2, 0, 100, times, dt, T)

currents = np.arange(-1, 1.2, .2)

plot_mV_vs_curr(currents, tau_m, Rm, dt, times)



