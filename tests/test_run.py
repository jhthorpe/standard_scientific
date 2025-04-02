# tests.py
#
# Provides interface with Pytest 

import pytest

import standard_scientific as si 

def test_exponent_from_float():
    good_input = [3.14, 10, 1E6, '578', 1e-3, 0.015, 5.3e-3] 
    good_exponents = [0, 1, 6, 2, -3, -2, -3]

    for inp, exp in zip(good_input, good_exponents):
        assert(si.exponent_from_float(inp) == exp)
    
    with pytest.raises(Exception) as e:
        si.exponent_from_float(None)
        si.exponent_from_float('abc')
