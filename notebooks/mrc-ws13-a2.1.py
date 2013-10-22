# -*- coding: utf-8 -*-
"""
Created on Tue Oct 22 20:36:03 2013

@author: alex
"""


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
    def __init__(self, xs, ys, zs, *args, **kwargs):
        FancyArrowPatch.__init__(self, (0,0), (0,0), *args, **kwargs)
        self._verts3d = xs, ys, zs

    def draw(self, renderer):
        xs3d, ys3d, zs3d = self._verts3d
        xs, ys, zs = proj3d.proj_transform(xs3d, ys3d, zs3d, renderer.M)
        self.set_positions((xs[0],ys[0]),(xs[1],ys[1]))
        FancyArrowPatch.draw(self, renderer)

data = np.load('point_cloud_001.npy')

ARROW_SCALE = 4

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

x, y, z = data.T

km = KMeans().fit(data)
# km.cluster_centers_.shape
# print km.labels_.shape

print km.labels_.shape
print km.cluster_centers_.shape

xc, yc, zc = km.cluster_centers_.T
ax.scatter(xc, yc, zc, c='r', marker='o')
#print km.cluster_centers_

# append labels to the data
l_data = np.column_stack([data, km.labels_])
# sort the labeled data
sl_data = l_data[l_data[:,3].argsort()]

#print sl_data.shape
x, y, z, l = sl_data.T

ax.scatter(x,y,z, c=l.astype(np.float))

split_at = sl_data[:,3].searchsorted(np.unique(km.labels_)+1)

#print np.unique(km.labels_)+1

grouped_data = np.split(sl_data, split_at)

for group in np.arange(len(grouped_data)-1):
    C = np.cov(grouped_data[group][:,0:3].T)
    w, v = LA.eig(C)
    norm = v[np.argmin(w)]
    
    i, j, k = km.cluster_centers_[group,:]
    xs = [i,i+norm[0]*ARROW_SCALE]
    ys = [j,j+norm[1]*ARROW_SCALE]
    zs = [k,k+norm[2]*ARROW_SCALE]
    a = Arrow3D(xs, ys, zs, mutation_scale=20, lw=1, arrowstyle="-|>", color="k")
    
    ax.add_artist(a)




ax.set_xlabel('X Label')
ax.set_ylabel('Y Label')
ax.set_zlabel('Z Label')

plt.show()