'''
Created on Jun 9, 2013

@author: Robin
@author: Alex
@author: David
'''

from control import matlab
#import matplotlib.pyplot as plt
import sympy
from control.pzmap import pzmap 
import numpy as np
from math import exp,sqrt


def valuesFromDampingRatio(transferFunction, dampingRatio):
    minGainSample = 0
    spacing = 1000
    closerToMGS = False
    gainFound = False
    slopeOfDampingRatioLine = np.abs(np.tan(np.arcsin(dampingRatio)))
    
    while not gainFound :
        data = matlab.rlocus(transferFunction, np.array([minGainSample,minGainSample + (spacing),minGainSample + (2*spacing),
                                minGainSample + (3*spacing),minGainSample + (4*spacing),minGainSample + (5*spacing),
                                minGainSample + (6*spacing),minGainSample + (7*spacing),minGainSample + (8*spacing),
                                minGainSample + (9*spacing),minGainSample + (10*spacing)]))
        for j in range(0, len(data[0][0])):
            for i in range(1, len(data[0])) :
                data_point = data[0][i][j]
                if data_point.imag > 0 :
                    if (data[0][i-1][j].imag > 0 and abs(-1*data_point.real / data_point.imag) <= slopeOfDampingRatioLine 
                            and abs(-1*data[0][i-1][j].real / data[0][i-1][j].imag) >= slopeOfDampingRatioLine) :
                        minGainSample = data[1][i-1]
                        if(data[0][i-1][j].imag > 0 
                                and abs(abs(-1*data_point.real / data_point.imag) - abs(slopeOfDampingRatioLine)) 
                                >= abs(abs(-1*data[0][i-1][j].real / data[0][i-1][j].imag) - abs(slopeOfDampingRatioLine))) :
                            closerToMGS = True
                        else :
                            closerToMGS = False
        if spacing == 0.1:
            gainFound = True
        else :
            spacing = spacing / 10
    if closerToMGS :
        return minGainSample
    else :
        return minGainSample + 0.1

def polesFromTransferFunction(transferFunction) :
    poles, zeros = pzmap(transferFunction, True)
    return poles
    
def overshootFromDampingRatio(transferFunction, dampingRatio):
    exponent = -1*dampingRatio*( np.pi/sqrt(1 - dampingRatio**2))
    overshoot = 100*exp(exponent)
    return overshoot
    
def dampingRatioFromGain(transferFunction, gain):
    data = matlab.rlocus(transferFunction, np.array([gain]))
    damping_ratio = 0
    for j in range(0, len(data[0][0])):
        for i in range(0, len(data[0])):
            data_point = data[0][i][j]
            if data_point.imag > 0:
                return np.sin(np.arctan(abs(-1*data_point.real / data_point.imag)))
    return damping_ratio
                    
def overshootFromGain(transferFunction, gain):
    data = matlab.rlocus(transferFunction, np.array([gain]))
    dampingRatio = 0
    for j in range(0, len(data[0][0])):
        for i in range(0, len(data[0])):
            data_point = data[0][i][j]
            if data_point.imag > 0 :
                dampingRatio = np.sin(np.arctan(abs(-1*data_point.real / data_point.imag)))
    exponent = -1*dampingRatio*( np.pi/sqrt(1 - dampingRatio**2))
    overshoot = 100*exp(exponent)
    return overshoot


def main():
    print "Root Locus Extras"
    print "Methods to add functionality to control.matlab.rlocus"
    print "requires control.matlab package"
    print "suggested usage: import homework8.root_locus_extras as rlx"
    s = sympy.Symbol("s")
    S = 1 / ((s+1)*(s+2)*(s+10))
    
    numerS = map(float, sympy.Poly(S.as_numer_denom()[0], s).all_coeffs()) 
    denomS = map(float, sympy.Poly(S.as_numer_denom()[1], s).all_coeffs())
    
    tf = matlab.tf(numerS, denomS)
    print "Gain ", valuesFromDampingRatio(tf, 0.174)
    print "Poles: ", polesFromTransferFunction(tf)
    print "Overshoot: ", overshootFromDampingRatio(tf, 0.174)
    print "Damping Ratio: ", dampingRatioFromGain(tf, 164.5)
    print "Overshoot: ", overshootFromGain(tf, 164.5)

if __name__=="__main__":
    main()
        