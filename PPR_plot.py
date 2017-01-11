from simulations import *

input_freq = [10, 35, 60, 85, 110]
ret_dict = sim_caller(5, 1*second, input_frequency=input_freq)
PY_PPR_2 = [0]*5
PY_PPR_10 = [0]*5
FS_PPR_2 = [0]*5
FS_PPR_10 = [0]*5
SOM_PPR_2 = [0]*5
SOM_PPR_10 = [0]*5

# pulling out PY neuron EPSP values from ret_dict
# PPR_2 array stores first spike epsp:initial epsp ratio
# PP_10 stores 10th spike epsp:initial epsp ratio
PY_1 = ret_dict[1]['PY_EPSP']
PY_PPR_2[0] = PY_1[1]/PY_1[0]
PY_PPR_10[0] = PY_1[9]/PY_1[0]
PY_2 = ret_dict[2]['PY_EPSP']
PY_PPR_2[1] = PY_2[1]/PY_2[0]
PY_PPR_10[1] = PY_2[9]/PY_2[0]
PY_3 = ret_dict[3]['PY_EPSP']
PY_PPR_2[2]= PY_3[1]/PY_3[0]
PY_PPR_10[2] = PY_3[9]/PY_3[0]
PY_4 = ret_dict[4]['PY_EPSP']
PY_PPR_2[3] = PY_4[1]/PY_4[0]
PY_PPR_10[3] = PY_4[9]/PY_4[0]
PY_5 = ret_dict[5]['PY_EPSP']
PY_PPR_2[4] = PY_5[1]/PY_5[0]
PY_PPR_10[4] = PY_5[9]/PY_5[0]

# same for FS neurons
FS_1 = ret_dict[1]['FS_EPSP']
FS_PPR_2[0] = FS_1[1]/FS_1[0]
FS_PPR_10[0] = FS_1[9]/FS_1[0]
FS_2 = ret_dict[2]['FS_EPSP']
FS_PPR_2[1] = FS_2[1]/FS_2[0]
FS_PPR_10[1] = FS_2[9]/FS_2[0]
FS_3 = ret_dict[3]['FS_EPSP']
FS_PPR_2[2]= FS_3[1]/FS_3[0]
FS_PPR_10[2] = FS_3[9]/FS_3[0]
FS_4 = ret_dict[4]['FS_EPSP']
FS_PPR_2[3] = FS_4[1]/FS_4[0]
FS_PPR_10[3] = FS_4[9]/FS_4[0]
FS_5 = ret_dict[5]['FS_EPSP']
FS_PPR_2[4] = FS_5[1]/FS_5[0]
FS_PPR_10[4] = FS_5[9]/FS_5[0]

# same for SOM neurons
SOM_1 = ret_dict[1]['SOM_EPSP']
SOM_PPR_2[0] = SOM_1[1]/SOM_1[0]
SOM_PPR_10[0] = SOM_1[9]/SOM_1[0]
SOM_2 = ret_dict[2]['SOM_EPSP']
SOM_PPR_2[1] = SOM_2[1]/SOM_2[0]
SOM_PPR_10[1] = SOM_2[9]/SOM_2[0]
SOM_3 = ret_dict[3]['SOM_EPSP']
SOM_PPR_2[2]= SOM_3[1]/SOM_3[0]
SOM_PPR_10[2] = SOM_3[9]/SOM_3[0]
SOM_4 = ret_dict[4]['SOM_EPSP']
SOM_PPR_2[3] = SOM_4[1]/SOM_4[0]
SOM_PPR_10[3] = SOM_4[9]/SOM_4[0]
SOM_5 = ret_dict[5]['SOM_EPSP']
SOM_PPR_2[4] = SOM_5[1]/SOM_5[0]
SOM_PPR_10[4] = SOM_5[9]/SOM_5[0]


# lots of print statements to check things are operating right
# print(ret_dict[5]['SOM_EPSP'][:10])
# print("First sim epsps:")
# print(SOM_1[0])
# print(SOM_1[1])
# print(SOM_1[9])
# print("Last sim epsps:")
# print(SOM_5[0])
# print(SOM_5[1])
# print(SOM_5[9])
# # print(PY_PPR_2)
# # print(PY_PPR_10)
# # print(FS_PPR_2)
# # print(FS_PPR_10)
# # print(SOM_PPR_2)
# # print(SOM_PPR_10)

plt.plot(input_freq, PY_PPR_2, "blue")
plt.plot(input_freq, PY_PPR_10, "b--")
plt.plot(input_freq, FS_PPR_2, "green")
plt.plot(input_freq, FS_PPR_10, "g--")
plt.plot(input_freq,SOM_PPR_2,  "red")
plt.plot(input_freq, SOM_PPR_10, "r--")
plt.show()
