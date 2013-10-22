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

def do_transformation(data):
	YBx = data[:, 0]
	YBy = data[:, 1]
	YBz = data[:, 2]

	W = sympy.physics.mechanics.ReferenceFrame("W")

	C = W.orientnew("C", "Axis", (np.deg2rad(-90), W.x))

	R = W.dcm(C)


	rData = np.empty(data.shape)
	#rData[:] = [R.dot(x) for x in data[:]]
	return rData

def main():
	data = np.load('youbot_drawing_points.npy')


	rData = do_transformation(data)

	PTx = rData[:, 0]
	PTy = rData[:, 1]
	PTz = rData[:, 2]


	fig = plt.figure()
	axes = fig.add_subplot(111)
	axes.set_aspect("equal")
	plt.scatter(PTx, PTy, c=PTz, marker='.', alpha=0.03, cmap=mpl.cm.gray)

	plt.show()

if __name__ == '__main__':
	main()