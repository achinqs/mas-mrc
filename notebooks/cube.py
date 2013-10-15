#!/usr/bin/env python
#-*- coding: utf-8 -*-
from mpl_toolkits.mplot3d import Axes3D
import itertools
import matplotlib.pyplot as plt
import numpy
import numpy.linalg
import sympy.physics.mechanics 


def world_frame():
    return sympy.physics.mechanics.ReferenceFrame("W")


def plot3d():
    fig = plt.figure()
    axes = fig.add_subplot(111, projection="3d")
    axes.set_aspect("equal")
    return axes


def pairwise(iterable):
    a, b = itertools.tee(iterable)
    next(b, None)
    return itertools.izip(a, b)


def unit_cube_vertices():
    cube_vertices = numpy.array(list(itertools.product([-1, 1], [-1, 1], [-1, 1])))
    all_edges = itertools.combinations(cube_vertices, 2)
    
    is_valid_edge = lambda start, end: numpy.sum(numpy.abs(start - end)) == 2
    
    valid_cube_edges = [
        zip(start, end) for start, end in all_edges
        if is_valid_edge(start, end)
    ]
    
    return numpy.array(valid_cube_edges)


# d = unit_cube_vertices()
# C = W.orientnew("C", "Axis", (math.radians(-45), W.y))
# R = W.dcm(C)
# e = numpy.empty(d.shape)
# e[..., 0] = [R.dot(x) for x in d[..., 0]]
# e[..., 0] = [R.dot(x) for x in d[..., 1]]
