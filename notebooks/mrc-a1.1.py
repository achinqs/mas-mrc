# -*- coding: utf-8 -*-
"""
Created on Tue Oct 15 18:56:19 2013

@author: alex
"""

from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import sympy.physics.mechanics 

data = np.load('youbot_drawing_points.npy')

YBx = data[:, 0]
YBy = data[:, 1]
YBz = data[:, 2]

fig = plt.figure()
axes = fig.add_subplot(111)
axes.set_aspect("equal")
plt.scatter(YBx,YBz, c=YBy, marker='.', alpha=0.03, cmap=mpl.cm.gray)

plt.show()
