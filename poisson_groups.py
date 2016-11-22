from brian2 import *

poisson_input = PoissonGroup(25, '125 + 125*sin(pi*t*1000/3)')
spike_mon = SpikeMonitor(poisson_input)
mon = PopulationRateMonitor(poisson_input)
state_mon = StateMonitor(poisson_input, 'rates', record=True)
run(1*second)

print(state_mon.rates)

plt.plot(spike_mon.t/ms, spike_mon.i, '.k')
plt.show()
