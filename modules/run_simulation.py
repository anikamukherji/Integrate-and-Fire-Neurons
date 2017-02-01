
from create_network import *
import matplotlib.pyplot as plt

# print(net.objects)
net.run(3*second)

mon = net['HVA_PY_V_mon']

plt.plot(mon.t/ms, mon.V[0])
plt.show()


