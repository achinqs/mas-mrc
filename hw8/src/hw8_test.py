#!/usr/bin/env python
from control import matlab
#import matplotlib.pyplot as plt
import sympy
import homework8.root_locus_extras as rlx


def main():
    print "This is an example of homework8 root locus extras"
    #s = sympy.Symbol("s")
    #S = 1 / ((s+1)*(s+2)*(s+10))
    
    #numerS = map(float, sympy.Poly(S.as_numer_denom()[0], s).all_coeffs()) 
    #denomS = map(float, sympy.Poly(S.as_numer_denom()[1], s).all_coeffs())
    numerS = [1]
    denomS = [1,3,2]
    tf = matlab.tf(numerS, denomS)
    
    gain = 0.11
    damping_ratio = 1.0
    
    print "Gain ", rlx.gainFromDampingRatio(tf, damping_ratio)
    print "Poles: ", rlx.polesFromTransferFunction(tf)
    print "Overshoot: ", rlx.overshootFromDampingRatio(tf, damping_ratio)
    print "Damping Ratio: ", rlx.dampingRatioFromGain(tf, gain)
    print "Overshoot: ", rlx.overshootFromGain(tf, gain)
    print "Frequency: ", rlx.frequencyFromGain(tf, gain)
    
    
    """the damping factor, gain, pole locations, overshoot and frequency"""

if __name__=="__main__":
    main()