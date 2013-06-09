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


def gainFromDampingRatio(transferFunction, dampingRatio):
    minGainSample = 0.0
    spacing = 1000.0
    closerToMGS = False
    gainFound = False
    slopeOfDampingRatioLine = abs(sympy.tan(sympy.asin(dampingRatio)))
    while not gainFound :
        data = matlab.rlocus(transferFunction, np.array([minGainSample,minGainSample + (1.0*spacing),minGainSample + (2.0*spacing),
                                minGainSample + (3.0*spacing),minGainSample + (4.0*spacing),minGainSample + (5.0*spacing),
                                minGainSample + (6.0*spacing),minGainSample + (7.0*spacing),minGainSample + (8.0*spacing),
                                minGainSample + (9.0*spacing),minGainSample + (10.0*spacing)]))        
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
    ## End While Loop
    if closerToMGS :
        return minGainSample
    else :
        return minGainSample + 0.1

def polesFromTransferFunction(transferFunction) :
    poles, _ = pzmap(transferFunction, True)
    return poles
    
def overshootFromDampingRatio(transferFunction, dampingRatio):
    overshoot = 0
    if abs(1.0-dampingRatio**2) > 0:
        exponent = -1.0*dampingRatio*( np.pi/sqrt(1.0 - dampingRatio**2))
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

def frequencyFromGain(transferFunction, gain):
    data = matlab.rlocus(transferFunction, np.array([gain]))
    frequency = None
    print len(data)
    for j in range(0, len(data[0][0])):
        for i in range(0, len(data[0])):
            print "j = ", j, "i = ", i
            data_point = data[0][i][j]
            if data_point.imag > 0:
                return np.sin(data_point.real**2 + data_point.imag**2)
    return frequency

                    
def overshootFromGain(transferFunction, gain):
    data = matlab.rlocus(transferFunction, np.array([gain]))
    dampingRatio = 0.0
    overshoot = 0.0
    for j in range(0, len(data[0][0])):
        for i in range(0, len(data[0])):
            data_point = data[0][i][j]
            if data_point.imag > 0 :
                dampingRatio = np.sin(np.arctan(abs(-1*data_point.real / data_point.imag)))
    if abs(1-dampingRatio**2) > 0:
        exponent = -1*dampingRatio*( np.pi/sqrt(1 - dampingRatio**2))
        overshoot = 100*exp(exponent)
    return overshoot

def main():
    print "Root Locus Extras"
    print "Methods to add functionality to control.matlab.rlocus"
    print "requires control.matlab package"
    print "suggested usage: import homework8.root_locus_extras as rlx"
    _s = sympy.Symbol("s")
    _S = 1 / ((_s+1)*(_s+2)*(_s+10))
    
    _numerS = map(float, sympy.Poly(_S.as_numer_denom()[0], _s).all_coeffs()) 
    _denomS = map(float, sympy.Poly(_S.as_numer_denom()[1], _s).all_coeffs())
    
    _tf = matlab.tf(_numerS, _denomS)
    
    _gain = 164.5
    _damping_ratio = 0.174
    
    _gain = gainFromDampingRatio(_tf, _damping_ratio)
    _poles = polesFromTransferFunction(_tf)
    _overshoot = overshootFromDampingRatio(_tf, _damping_ratio)
    _damping_ratio = dampingRatioFromGain(_tf, _gain)
    
    print "example: "
    print "system = ", _tf
    
    print "Damping Ratio provided: ", _damping_ratio
    print "Calculated values:"
    
    print "Gain: ", _gain
    print "Poles: ", _poles
    print "Overshoot: ", _overshoot
    print "Damping Ratio: ", dampingRatioFromGain(_tf, _gain)
    print "Overshoot: ", overshootFromGain(_tf, _gain)
    print "Frequency:", frequencyFromGain(_tf, _gain)

if __name__=="__main__":
    main()
        