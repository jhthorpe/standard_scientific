# test_scidata.py
#
# Provides interface with Pytest for testing the SciData class
# and related functionality

import pytest

import standard_scientific as si 

###############################################################
# Test == comparison
#
@pytest.mark.parametrize("a, b", [
     (si.SciData(si.SigFig.from_float(12.345, 5), si.SigFig.from_float(0.067, 2), si.SigFig.from_float(5.4e-3, 2), False),
      si.SciData(si.SigFig.from_float(12.345, 5), si.SigFig.from_float(0.067, 2), si.SigFig.from_float(5.4e-3, 2), False)),
     (si.SciData(si.SigFig.from_float(12.345, 5), None, None, True),
      si.SciData(si.SigFig.from_float(12.345, 5), None, None, True)) 
    ])
def test_equals_good(a, b):
    assert(a == b)

###############################################################
# Test != comparison
#
@pytest.mark.parametrize("a, b", [
     (si.SciData(si.SigFig.from_float(12.345, 5), si.SigFig.from_float(0.067, 2), si.SigFig.from_float(5.4e-3, 2), False),
      si.SciData(si.SigFig.from_float(12.341, 5),                           None,                            None, True)),
     (si.SciData(si.SigFig.from_float(12.345, 5), si.SigFig.from_float(0.067, 2), si.SigFig.from_float(5.4e-3, 2), False),
      si.SciData(si.SigFig.from_float(12.345, 5), si.SigFig.from_float(0.067, 2), si.SigFig.from_float(5.5e-3, 2), False)),
     (si.SciData(si.SigFig.from_float(12.345, 5), si.SigFig.from_float(0.067, 2), si.SigFig.from_float(5.4e-3, 2), False),
      si.SciData(si.SigFig.from_float(12.345, 5), si.SigFig.from_float(0.067, 2), si.SigFig.from_float(5.4e-3, 3), False)),
     (si.SciData(si.SigFig.from_float(12.345, 5), si.SigFig.from_float(0.068, 2), si.SigFig.from_float(5.4e-3, 2), False),
      si.SciData(si.SigFig.from_float(12.345, 5), si.SigFig.from_float(0.067, 2), si.SigFig.from_float(5.4e-3, 2), False)),
     (si.SciData(si.SigFig.from_float(12.345, 5), si.SigFig.from_float(0.067, 3), si.SigFig.from_float(5.4e-3, 2), False),
      si.SciData(si.SigFig.from_float(12.345, 5), si.SigFig.from_float(0.067, 2), si.SigFig.from_float(5.4e-3, 2), False)),
     (si.SciData(si.SigFig.from_float(12.346, 5), si.SigFig.from_float(0.067, 2), si.SigFig.from_float(5.4e-3, 2), False),
      si.SciData(si.SigFig.from_float(12.345, 5), si.SigFig.from_float(0.067, 2), si.SigFig.from_float(5.4e-3, 2), False)),
     (si.SciData(si.SigFig.from_float(12.345, 6), si.SigFig.from_float(0.067, 2), si.SigFig.from_float(5.4e-3, 2), False),
      si.SciData(si.SigFig.from_float(12.345, 5), si.SigFig.from_float(0.067, 2), si.SigFig.from_float(5.4e-3, 2), False)),
    ])
def test_not_equals_good(a, b):
    assert(a != b)


################################################
# Test generation of SciData fs
#
@pytest.mark.parametrize("v, u, r, ex, c", [
    (           si.SigFig.from_float(12.345, 5), si.SigFig.from_float(0.067, 2), si.SigFig.from_float(5.4e-3, 2), False, 
     si.SciData(si.SigFig.from_float(12.345, 5), si.SigFig.from_float(0.067, 2), si.SigFig.from_float(5.4e-3, 2), False) ),
    (           si.SigFig.from_float(12.345, 5), si.SigFig.from_float(0.067, 2), si.SigFig.from_float(5.4e-3, 2),  True, 
     si.SciData(si.SigFig.from_float(12.345, 5),                           None,                            None,  True) ),
    (           si.SigFig.from_float(12.345, 5), si.SigFig.from_float(0.067, 2),                            None, False, 
     si.SciData(si.SigFig.from_float(12.345, 5), si.SigFig.from_float(0.067, 2), si.SigFig.from_float(5.4e-3, 2), False) )
    ])
def test_from_SigFig_good(v, u, r, ex, c):
    assert(si.SciData.from_SigFigs(value = v, unc = u, rel_unc = r, is_exact = ex) == c)


################################################
# Test that we get assertion problems from the following 
#
@pytest.mark.parametrize("v, u, r, ex", [
    (si.SigFig.from_float(12.345, 5),                           None, si.SigFig.from_float(5.4e-3, 2), False), 
    (                           None, si.SigFig.from_float(0.067, 2), si.SigFig.from_float(5.4e-3, 2), False), 
    (                           None, si.SigFig.from_float(0.067, 2), si.SigFig.from_float(5.4e-3, 2), True), 
    ])
def test_from_SigFig_bad(v, u, r, ex):
    with pytest.raises(Exception) as e:
        si.SciData.from_SigFigs(value = v, unc = u, rel_unc = r, is_exact = ex) 

################################################
# Test from_str throws an assert in conversions from common mistakes
@pytest.mark.parametrize("s", [
    ("1.23(04)"),
    ("1.23(0.04)")
    ])
def test_from_str_bad(s):
    with pytest.raises(Exception) as e:
        si.SciData.from_str(s)


################################################
# Testing the from_str, these should all pass without
# errors or warnings. 
@pytest.mark.parametrize("s, c", [
    ("+12.3", 
     si.SciData.from_SigFigs(value = si.SigFig.from_float(12.3, 3), 
                             unc = None, 
                             rel_unc = None,  
                             is_exact = True)), 
    ("-0.01234", 
     si.SciData.from_SigFigs(value = si.SigFig.from_float(-0.01234, 4), 
                             unc = None, 
                             rel_unc = None, 
                             is_exact = True)), 
    ("123", 
     si.SciData.from_SigFigs(value = si.SigFig.from_float(123, 3), 
                             unc = None, 
                             rel_unc = None, 
                             is_exact = True)), 
    ("0123", 
     si.SciData.from_SigFigs(value = si.SigFig.from_float(123, 3), 
                             unc = None, 
                             rel_unc = None, 
                             is_exact = True)), 
    ("01230", 
     si.SciData.from_SigFigs(value = si.SigFig.from_float(1230, 4), 
                             unc = None, 
                             rel_unc = None, 
                             is_exact = True)), 
    ("+00.0013(3)",
     si.SciData.from_SigFigs(value = si.SigFig.from_float(0.0013, 2), 
                             unc = si.SigFig.from_float(0.0003, 1),  
                             rel_unc = si.SigFig.from_float(0.0003 / 0.0013, 1), 
                             is_exact = False)),
    ("-0012.345(67)e-4",
     si.SciData.from_SigFigs(value = si.SigFig.from_float(-0.0012345, 5), 
                             unc = si.SigFig.from_float(  0.0000067, 2),  
                             rel_unc = si.SigFig.from_float(0.0000067 / 0.0012345, 2), 
                             is_exact = False)),
    ("1.2(345)",
     si.SciData.from_SigFigs(value = si.SigFig.from_float(1.2, 2), 
                             unc = si.SigFig.from_float( 34.5, 3),  
                             rel_unc = si.SigFig.from_float(34.5 / 1.2, 2), 
                             is_exact = False)),
    ("1.2(345)e1",
     si.SciData.from_SigFigs(value = si.SigFig.from_float(12, 2), 
                             unc = si.SigFig.from_float( 345, 3),  
                             rel_unc = si.SigFig.from_float(345 / 12, 2), 
                             is_exact = False)),
    ])
def test_from_str_good(s, c):
    assert(si.SciData.from_str(s) == c)

