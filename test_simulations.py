from simulations import *
import matplotlib.pyplot as plt

test_dict = sim_caller(3, 0.5*second, input_frequency=[10, 50, 100])
ret_dict = test_dict

pulses_1 = ret_dict[1]["pulse_num"]
max_pulses = pulses_1[-1]
PY_1 = ret_dict[1]['PY_EPSP']
PY_2 = ret_dict[2]['PY_EPSP']
PY_3 = ret_dict[3]['PY_EPSP']
FS_1 = ret_dict[1]['FS_EPSP']
FS_2 = ret_dict[2]['FS_EPSP']
FS_3 = ret_dict[3]['FS_EPSP']
SOM_1 = ret_dict[1]['SOM_EPSP']
SOM_2 = ret_dict[2]['SOM_EPSP']
SOM_3 = ret_dict[3]['SOM_EPSP']

print(PY_1[:10])
print(PY_2[:10])
print(PY_3[:10])

f, (ax10, ax50, ax100) = plt.subplots(3, sharex=True, sharey=True)
ax10.plot(PY_1, 'blue')
ax10.plot(FS_1, 'green')
ax10.plot(SOM_1, 'red')
ax50.plot(PY_2, 'blue')
ax50.plot(FS_2, 'green')
ax50.plot(SOM_2, 'red')
ax100.plot(PY_3, 'blue')
ax100.plot(FS_3, 'green')
ax100.plot(SOM_3, 'red')
ax100.set_xlim([-50, 5000])
ax100.set_ylim([-0.002, 0.009])
ax10.set_title("EPSP Strength for 10 Hz Input Train")
ax50.set_title("EPSP Strength for 50 Hz Input Train")
ax100.set_title("EPSP Strength for 100 Hz Input Train")
ax100.set_xlabel("Time steps (10^-4 seconds)")
plt.show()
