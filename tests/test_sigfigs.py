# test_sigfigs.py
#
# Provides interface with Pytest for testing the sigfigs class

import pytest

import standard_scientific as si 

def test_exponent_from_float():

    assert(si.exponent_from_float(    3.14) ==  0)
    assert(si.exponent_from_float(      10) ==  1)
    assert(si.exponent_from_float(     1e6) ==  6)
    assert(si.exponent_from_float(     578) ==  2)
    assert(si.exponent_from_float(    1e-3) == -3)
    assert(si.exponent_from_float(   0.015) == -2)
    assert(si.exponent_from_float(  5.3e-3) == -3)
    assert(si.exponent_from_float('-57e-8') == -7)
    
    with pytest.raises(Exception) as e:
        si.exponent_from_float(None)
        si.exponent_from_float('abc')

def test_bad_construction():
    with pytest.raises(Exception) as e:
        si.SigFig.from_float(value = 1.234, sigfigs = 0)

def test_equalities():
    x  = si.SigFig.from_float(value =  3.14, sigfigs = 2)
    xb = si.SigFig.from_float(value =  3.15, sigfigs = 2)
    y  = si.SigFig.from_float(value =  3.14, sigfigs = 3)
    z  = si.SigFig.from_float(value = -3.14, sigfigs = 2)
    a  = si.SigFig.from_float(value = -3.2,  sigfigs = 2)

    assert(x.value == 3.1)
    assert(x.sigfigs == 2)
    assert(x.exponent == 0)

    assert(x == x)
    assert(x == xb)
    assert(not(x == y))
    assert(not(x == z))

    assert(z < x)
    assert(z <= x)
    assert(z > a)
    assert(z >= a)

    assert(z < 5)
    assert(z > -3.5)

    #check the rounding examples
    assert(y == 3.141)
    assert(y == 3.1449)
    assert(y != 3.1451)
    assert(y != 3.1499)
    assert(y != 3.15)

def test_mult_div():

    # * and / Operations with "exact" digits
    x10 = si.SigFig.from_float(value = 10., sigfigs = 2)
    x100 = si.SigFig.from_float(value = 100., sigfigs = 2)
    y10 = si.SigFig.from_float(value = 10., sigfigs = 3)
    y100 = si.SigFig.from_float(value = 100., sigfigs = 3)

    assert(x100 == (x10 * 10))
    assert(x100 != (y10 * 10))

    assert(x10 == (x100 / 10))
    assert(x10 != (y100 / 10))

    # * and / Operations with other SigFigs
    assert(x100 == (y10 * x10))
    assert(y100 != (y10 * x10))

    assert(x10 == (y100 / x10))
    assert(y10 != (y100 / x10))

def test_add_sub():

    # + operation 
    a = si.SigFig.from_float(value = 1001.5, sigfigs = 5)
    b = si.SigFig.from_float(value = 1012.0, sigfigs = 5) 
    c = si.SigFig.from_float(value = 10.49, sigfigs = 4)
    d = si.SigFig.from_float(value = 10.490, sigfigs = 5)
    e = si.SigFig.from_float(value = 10.4900, sigfigs = 6)

    #these will round to the tenth's place
    assert(a + c == b)      #this should round 1001.5 + 10.49   to 1012.0, sf = 5
    assert(a + c.value == b)#this should be the same as above
    assert(a + d == b)      #this should round 1001.5 + 10.490  to 1012.0, sf = 5 
    assert(a + d.value == b)#this should be the same as above
    assert(a + e == b)      #this should round 1001.5 + 10.4900 to 1012.0, sf = 5 
    assert(a + e.value == b)#this should be the same as above

    #for tests with decreasing sig figs 
    fx = si.SigFig.from_float(value = 10.5, sigfigs = 3)
    fy = si.SigFig.from_float(value = 1012.0, sigfigs = 5)
    gx = si.SigFig.from_float(value = 11, sigfigs = 2)
    gy = si.SigFig.from_float(value = 1012, sigfigs = 4)
    hx = si.SigFig.from_float(value = 10, sigfigs = 1)
    hy = si.SigFig.from_float(value = 1010, sigfigs = 3)
    ix = si.SigFig.from_float(value = 100, sigfigs = 1)
    iy = si.SigFig.from_float(value = 1100, sigfigs = 2)
    assert(a + fx == fy) #this should round 1001.5 + 10.5 to 1012.0, sf = 5
    assert(a + gx == gy) #this should round 1001.5 + 11.  to 1012. , sf = 4 
    assert(a + hx == hy) #this should round 1001.5 + 1e1  to 1.01e3, sf = 3
    assert(a + ix == iy) #this should round 1001.5 + 1e2  to 1.1e3 , sf = 2

    #testing going up an order of magnatude
    jx = si.SigFig.from_float(value = 99.9, sigfigs = 3)
    jy = si.SigFig.from_float(value =  1.0, sigfigs = 2)
    jz = si.SigFig.from_float(value = 100.9, sigfigs = 4)
    assert(jx + jy == jz)

    #  - operation 
    a = si.SigFig.from_float(value = 1001.5, sigfigs = 5)
    b = si.SigFig.from_float(value = 1012.0, sigfigs = 5) 
    c = si.SigFig.from_float(value = 10.49, sigfigs = 4)
    d = si.SigFig.from_float(value = 10.490, sigfigs = 5)
    e = si.SigFig.from_float(value = 10.4900, sigfigs = 6)

    #these will round to the tenth's place
    assert(b - c == a)      #this should round 1012.0 - 10.49   to 1001.5, sf = 5
    assert(b - c.value == a)#this should round 1012.0 - 10.49   to 1001.5, sf = 5
    assert(b - d == a)      #this should round 1012.0 - 10.490  to 1001.5, sf = 5
    assert(b - d.value == a)#this should round 1012.0 - 10.490  to 1001.5, sf = 5
    assert(b - e == a)      #this should round 1012.0 - 10.4900 to 1001.5, sf = 5
    assert(b - e.value == a)#this should round 1012.0 - 10.4900 to 1001.5, sf = 5

    #these will round to variable places
    fx = si.SigFig.from_float(value = 10.5, sigfigs = 3)
    fy = si.SigFig.from_float(value = 1012.0, sigfigs = 5)
    gx = si.SigFig.from_float(value = 11, sigfigs = 2)
    gy = si.SigFig.from_float(value = 1012, sigfigs = 4)
    assert(fy - fx == a) #this should round 1012.0 - 10.5   to 1001.5, sf = 5
    assert(fy - a == fx) #this should round 1012.0 - 1001.5 to   10.5, sf = 3 
'''

    #for tests with decreasing sig figs 
    fx = si.SigFig.from_float(value = 10.5, sigfigs = 3)
    fy = si.SigFig.from_float(value = 1012.0, sigfigs = 5)
    gx = si.SigFig.from_float(value = 11, sigfigs = 2)
    gy = si.SigFig.from_float(value = 1012, sigfigs = 4)
    hx = si.SigFig.from_float(value = 10, sigfigs = 1)
    hy = si.SigFig.from_float(value = 1010, sigfigs = 3)
    ix = si.SigFig.from_float(value = 100, sigfigs = 1)
    iy = si.SigFig.from_float(value = 1100, sigfigs = 2)
    assert(a + fx == fy) #this should round 1001.5 + 10.5 to 1012.0, sf = 5
    assert(a + gx == gy) #this should round 1001.5 + 11.  to 1012. , sf = 4 
    assert(a + hx == hy) #this should round 1001.5 + 1e1  to 1.01e3, sf = 3
    assert(a + ix == iy) #this should round 1001.5 + 1e2  to 1.1e3 , sf = 2

    #testing going up an order of magnatude
    jx = si.SigFig.from_float(value = 99.9, sigfigs = 3)
    jy = si.SigFig.from_float(value =  1.0, sigfigs = 2)
    jz = si.SigFig.from_float(value = 100.9, sigfigs = 4)
    assert(jx + jy == jz)
'''
    
def test_strings():
    x = si.SigFig.from_float(value = 1.234, sigfigs = 2)
    y = si.SigFig.from_float(value = 0.1234, sigfigs = 2)
    z = si.SigFig.from_float(value = 12.34, sigfigs = 2)
    assert(str(x) == '1.2e+00')
    assert(str(y) == '1.2e-01')
    assert(str(z) == '1.2e+01')
