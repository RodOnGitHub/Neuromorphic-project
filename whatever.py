import numpy as np
import pandas as pd

def receptive_field(number_neurons, sigma, min_value, max_value, value_to_encode, spike_time_ms):
    number_n_fields = number_neurons

    bins = value_to_encode
    Gauss_centers = np.arange(min_value, max_value,
                              np.divide(np.abs(np.array(max_value) - (min_value)), number_n_fields)).tolist()

    r = []
    for i in Gauss_centers:
        r.append(1 / (sigma * np.sqrt(2 * np.pi)) * np.exp(- (bins - i) ** 2 / (2 * sigma ** 2)))


    spike_time = pd.DataFrame([-spike_time_ms * r[i] + 10 for i in range(8)])
    spike_time[spike_time >= 9] = 'Silent'

    return r, spike_time