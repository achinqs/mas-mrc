# -*- coding: utf-8 -*-
"""
Created on Tue Oct 15 22:49:46 2013

@author: alex
"""

from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import sympy.physics.mechanics 

data = np.load('lidar_scan.npy')

r = data[data.nonzero()]
a = data.nonzero()[1]
t = data.nonzero()[0]

m = np.amax(r)

mx = m*np.cos(np.deg2rad(np.arange(180)))
my = m*np.sin(np.deg2rad(np.arange(180)))

x = r * ( np.cos(np.deg2rad(a)) )
y = r * ( np.sin(np.deg2rad(a)) )
fig = plt.figure()
axes = fig.add_subplot(111)
axes.set_aspect("equal", )
plt.scatter(x,y, c=t, marker='o')
cb = fig.colorbar(plt)

#plt.scatter(mx,my, marker='.', alpha=0.1)


plt.show()
