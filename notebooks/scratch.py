# -*- coding: utf-8 -*-
"""
Created on Tue Oct 29 23:10:49 2013

@author: alex
"""

import numpy as np
import numpy.linalg as LA

import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

data = np.load("shape001.npy")

x, y = data.T

fig = plt.figure()
ax = fig.add_subplot(111)
ax.scatter(x,y)