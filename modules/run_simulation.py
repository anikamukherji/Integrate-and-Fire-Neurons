
from create_network import *
import matplotlib.pyplot as plt

# print(net.objects)
mod_rates = [10, 30, 60, 100]
for i in mod_rates:
    path = "afferents modulation_rate {}".format(i)
    net = create_network(path)
    net.run(3*second)
    mon = net['HVA_PY_V_mon']
    plt.plot(mon.t/ms, mon.V[0])

plt.show()
# aff_mon = net["afferent_spike_mon"]

# f, (ax_input, ax2) = plt.subplots(2, sharex = True, sharey = False)

# ax_input.plot(aff_mon.t/ms, aff_mon.i, '|k')
# ax_input.set_yticks([])
# ax_input.set_title("HVA_PY Spiking Cells Response to 200 afferents")
# ax2.plot(mon.t/ms, mon.V[0])



