# -*- coding: utf-8 -*-
"""
Created on Sat Jan 25 17:09:20 2014

@author: alex
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import proj3d

data = np.load("trial_exam_data_031.npy")

x, y, z = data.T

fig = plt.figure()
ax1 = fig.add_subplot(111, projection='3d')
ax1.scatter(x, y, z)

plt.show()