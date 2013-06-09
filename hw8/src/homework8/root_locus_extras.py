'''
Root Locus Extras - Methods to add functionality to control.matlab.rlocus

requires control.matlab package
suggested usage: import homework8.root_locus_extras as rlx

see/run root_locus_extras.main() for an example

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
    """
    Returns gain found from a given control.matlab.tf transferFunction and dampingRatio
    
    By sampling along matlab.rlocus plot. Converges on an area of the plot by taking smaller sized
    samples (defined by variable 'spacing') in each iteration until spacing = 0.1 , thus the gain will 
    only ever be within 0.1 
    """
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
                    if (data[0][i-1][j].imag > 0 and abs(data_point.real / data_point.imag) <= slopeOfDampingRatioLine 
                            and abs(data[0][i-1][j].real / data[0][i-1][j].imag) >= slopeOfDampingRatioLine) :
                        minGainSample = data[1][i-1]
                        if(data[0][i-1][j].imag > 0 
                                and abs(abs(data_point.real / data_point.imag) - abs(slopeOfDampingRatioLine)) 
                                >= abs(abs(data[0][i-1][j].real / data[0][i-1][j].imag) - abs(slopeOfDampingRatioLine))) :
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
    """
    Finds and returns an array of poles given a control.matlab.tf transferFunction
    
    This is wrapping control.pzmap.pzmap() and discarding zero information.
    """
    poles, _ = pzmap(transferFunction, True)
    return poles
    
def overshootFromDampingRatio(transferFunction, dampingRatio):
    """
    returns overshoot given a control.matlab.tf transferFunction and a dampingRatio
    
    Value is calculated from defined equation.
    """
    overshoot = 0
    if abs(1.0-dampingRatio**2) > 0:
        exponent = -1.0*dampingRatio*( np.pi/sqrt(1.0 - dampingRatio**2))
        overshoot = 100*exp(exponent)
    return overshoot
    
def dampingRatioFromGain(transferFunction, gain):
    """
    Finds and returns DampingRatio given a control.matlab.tf transferFunction and gain
    
    
    """
    data = matlab.rlocus(transferFunction, np.array([gain]))
    damping_ratio = 0
    for j in range(0, len(data[0][0])):
        for i in range(0, len(data[0])):
            data_point = data[0][i][j]
            if data_point.imag > 0:
                return np.sin(np.arctan(abs(-1*data_point.real / data_point.imag)))
    return damping_ratio

def frequencyFromGain(transferFunction, gain):
    """
    Returns frequency from given control.matlab.tf transferFunction and gain.
    
    frequency was observed to equal to the distance from origin to a point on the 
    control.matlab.rlocus plot. 
    """
    data = matlab.rlocus(transferFunction, np.array([gain]))
    frequency = 0
    for j in range(0, len(data[0][0])):
        for i in range(0, len(data[0])):
            data_point = data[0][i][j]
            if data_point.imag > 0:
                return np.sqrt(data_point.real**2 + data_point.imag**2)
    return frequency

                    
def overshootFromGain(transferFunction, gain):
    """
    Finds overshoot of control.matlab.tf transferFunction given gain.
    
    """
    data = matlab.rlocus(transferFunction, np.array([gain]))
    dampingRatio = 0.0
    overshoot = 0.0
    for j in range(0, len(data[0][0])):
        for i in range(0, len(data[0])):
            data_point = data[0][i][j]
            if data_point.imag > 0 :
                dampingRatio = np.sin(np.arctan(abs(data_point.real / data_point.imag)))
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
        