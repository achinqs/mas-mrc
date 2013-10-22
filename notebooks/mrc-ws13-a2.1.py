# -*- coding: utf-8 -*-
"""
Created on Tue Oct 22 20:36:03 2013

@author: alex
"""

# Solution 2.1
# ...

## Note the magic offset of 1 here and there. 

from sklearn.cluster import KMeans
import numpy as np
import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from numpy import linalg as LA
#draw a vector
from matplotlib.patches import FancyArrowPatch
from mpl_toolkits.mplot3d import proj3d

class Arrow3D(FancyArrowPatch):
    '''
    This Arrow3D class was found on StackOverflow, to plot 3D vector Arrows
    http://stackoverflow.com/questions/11140163/
    '''
    def __init__(self, xs, ys, zs, *args, **kwargs):
        FancyArrowPatch.__init__(self, (0,0), (0,0), *args, **kwargs)
        self._verts3d = xs, ys, zs

    def draw(self, renderer):
        xs3d, ys3d, zs3d = self._verts3d
        xs, ys, zs = proj3d.proj_transform(xs3d, ys3d, zs3d, renderer.M)
        self.set_positions((xs[0],ys[0]),(xs[1],ys[1]))
        FancyArrowPatch.draw(self, renderer)

# Load the Data
data = np.load('point_cloud_001.npy')

# The plot is by default a little hard to see, these fix that 
ARROW_SCALE = 4
# pylab.rcParams['figure.figsize'] = (15.0, 15.0)

# start a figure with 3D axes
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Using KMeans from SciKit Learn, cluster the data
km = KMeans().fit(data)

# get the center of the clusters and plot them as large red dots
xc, yc, zc = km.cluster_centers_.T
ax.scatter(xc, yc, zc, c='r', s=400, marker='o')

# append labels to the data
l_data = np.column_stack([data, km.labels_])
# sort the labeled data
sl_data = l_data[l_data[:,3].argsort()]

# plot the labeled data and color code by label
x, y, z, l = sl_data.T
#ax.scatter(x,y,z, c=l.astype(np.float))

# find indices to split data, and group the data by labels
split_at = sl_data[:,3].searchsorted(np.unique(km.labels_)+1)
grouped_data = np.split(sl_data, split_at)

# for each group of data 
for group in range(len(grouped_data)-1):
    # create the covariance matrix C
    C = np.cov(grouped_data[group][:,0:3].T)
    # and obtain the eigenvalues and eigenvectors of C
    w, v = LA.eig(C)
    # the normal vector is eigenvector corresponding to lowest eigenvalue
    norm = v[:,np.argmin(w)]
    print '#######---',group,'---######'
    #print C
    #print v
    #print w
    print "N", norm
    major = v[:,np.argmax(w)]
    print "M", major    
    
    # from the centre of each cluster, find endpoints of scaled normal vector
    i, j, k = km.cluster_centers_[group,:]
    ax.text(i,j,k, str(group))
    xs = [i,i+norm[0]*ARROW_SCALE]
    ys = [j,j+norm[1]*ARROW_SCALE]
    zs = [k,k+norm[2]*ARROW_SCALE]
    
    # Plot the normal vectors using fancy function from stack overflow.
    if norm[2] > 0.9:
        a = Arrow3D(xs, ys, zs, mutation_scale=40, lw=1, arrowstyle="-|>", color="k")
        ax.add_artist(a)

#set the labels
ax.set_xlabel('X Label')
ax.set_ylabel('Y Label')
ax.set_zlabel('Z Label')
plt.show()