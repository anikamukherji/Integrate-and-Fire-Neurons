from brian2 import *

poisson_input = PoissonGroup(25, rates='25 + 25*sin(pi*(t*6))')
spike_mon = SpikeMonitor(poisson_input)
mon = PopulationRateMonitor(poisson_input)
state_mon = StateMonitor(poisson_input, 'rates', record=True)
run(1*second)

print(state_mon.rates[0])
print(state_mon.t)

f, (ax1, ax2) = plt.subplots(2, sharex=True, sharey=False)
ax2.plot(state_mon.t/ms, state_mon.rates[0])
ax2.set_xlabel("Time (ms)")
ax1.set_title("Poisson Input Firing")
ax2.set_ylabel("Firing Rate (Hz)")
ax1.plot(spike_mon.t/ms, spike_mon.i, '.k')
ax1.set_ylabel("Neuron Number")
plt.show()
