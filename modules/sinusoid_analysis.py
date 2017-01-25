import numpy as np
import math
import matplotlib.pyplot as plt

    
def onset_offset(frequency, runtime, threshold):

    '''
    Returns an array of onset and offset times
    1's indicate a time of pulse onset
    -1's indicate a time of pulse offset
    0's indicate no change in activity 
    '''
    # match firing_rate_array to time array assuming dt=0.1*ms
    firing_rate_array = list(range(0, runtime*10000))
    # translate into seconds
    # turn into array of sine values ranging from 0 to 1
    firing_rate_array = [math.sin(2*math.pi*t*frequency) for t in firing_rate_array]
    thresh_arr = [0 if v<threshold else 1 for v in firing_rate_array]
    on_off_arr = np.diff(thresh_arr)
    # account for lost first term by appending a 0
    on_off_arr = np.insert(on_off_arr, 0, 0, axis=0)

    return on_off_arr

def first_pulse(onsets_offsets):

    '''
    Returns dict with indices of beginning and end of first pulse given an
    array of onsets and offsets
    '''

    onsets_offsets = onsets_offsets.tolist()
    on = onsets_offsets.index(1)
    off = onsets_offsets.index(-1)
    ret = {"on":on, "off":off}
    return ret

def last_pulse(onsets_offsets):

    '''
    Returns dict with indices of beginning and end of last pulse given an
    array of onsets and offsets
    '''
    
    on = rindex(onsets_offsets, 1)
    off = rindex(onsets_offsets, -1)
    ret = {"on":on, "off":off}
    return ret


def rindex(lst, val):
    lst = lst.tolist()
    return len(lst) - lst[::-1].index(val) - 1
