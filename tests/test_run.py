# tests.py
#
# Provides interface with Pytest 

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

def test_equalities():
    x  = si.Sigfig.from_float(value =  3.14, sigfigs = 2)
    xb = si.Sigfig.from_float(value =  3.15, sigfigs = 2)
    y  = si.Sigfig.from_float(value =  3.14, sigfigs = 3)
    z  = si.Sigfig.from_float(value = -3.14, sigfigs = 2)
    a  = si.Sigfig.from_float(value = -3.2, sigfigs = 2)

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
