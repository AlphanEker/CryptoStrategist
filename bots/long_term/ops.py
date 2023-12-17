import os
import math
import logging

import numpy as np


def sigmoid(x):
    """
    Performs sigmoid operation
    """
    try:
        if x < 0:
            return 1 - 1 / (1 + math.exp(x))
        return 1 / (1 + math.exp(-x))
    except Exception as err:
        print("Error in sigmoid: " + err)


def get_state(data, t, n_days):
    """Returns an n-day state representation ending at time t for multiple features."""
    d = t - n_days + 1
    block = data[d: t + 1, :] if d >= 0 else np.vstack((-d * [data[0, :]], data[0: t + 1, :]))  # pad with t0

    res = []
    for i in range(n_days - 1):
        # Calculate the difference for each feature and apply sigmoid
        res.append([sigmoid(block[i + 1, j] - block[i, j]) for j in range(block.shape[1])])

    # Return as a numpy array
    # 2D array with first element indicator, second element value.
    return np.array(res)
