import numpy as np

def onset_offset(firing_rate_array, threshold):

    '''
    Returns an array of onset and offset times
    1's indicate a time of pulse onset
    -1's indicate a time of pulse offset
    0's indicate no change in activity
    '''
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
    #TODO: would something like this work also work (to get all onsets/offsets)?
    #
    #  on_indicies = [x for x in range(len(onsets_offsets)) if onsets_offsets[x] == 1]
    #  off_indicies = [x for x in range(len(onsets_offsets)) if onsets_offsets[x] == -1]
    #
    # Thus, you get all onset/offset indicies ordered by pulse number?
    # P_1 would be on_indicies[0], P_end would be on_indicies[-1]?
    #
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
