#!/usr/bin/env python
from control import matlab
#import matplotlib.pyplot as plt
import sympy
import homework8.root_locus_extras as rlx


def main():
    print "This is an example of homework8 root locus extras"
    s = sympy.Symbol("s")
    S = 1 / ((s+1)*(s+2)*(s+10))
    
    numerS = map(float, sympy.Poly(S.as_numer_denom()[0], s).all_coeffs()) 
    denomS = map(float, sympy.Poly(S.as_numer_denom()[1], s).all_coeffs())
    
    tf = matlab.tf(numerS, denomS)
    print "Gain ", rlx.gainFromDampingRatio(tf, 0.174)
    print "Poles: ", rlx.polesFromTransferFunction(tf)
    print "Overshoot: ", rlx.overshootFromDampingRatio(tf, 0.174)
    print "Damping Ratio: ", rlx.dampingRatioFromGain(tf, 164.5)
    print "Overshoot: ", rlx.overshootFromGain(tf, 164.5)
    print "Frequency: ", rlx.frequencyFromGain(tf, 164.5)
    
    
    """the damping factor, gain, pole locations, overshoot and frequency"""

if __name__=="__main__":
    main()