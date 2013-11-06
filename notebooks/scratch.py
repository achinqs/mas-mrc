# -*- coding: utf-8 -*-
"""
Created on Tue Oct 29 23:10:49 2013

@author: alex
"""

import numpy as np
import numpy.linalg as LA

import matplotlib.pyplot as plt

data = np.load("shape001.npy")

x, y = data.T

A = np.vstack([x, np.ones(len(x))]).T

m, c = LA.lstsq(A, y)[0]

print m, c

fig = plt.figure()
ax = fig.add_subplot(111)
ax.scatter(x,y)
ax.plot(x, m*x + c, 'r', label='Fitted line')

plt.show()