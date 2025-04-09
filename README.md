# standard_scientific 
Package that facilitates the representation and interpretation of data in scientific notation. The main features are two classes, the `SigFig` class and the `SciData` class.  

## `SigFig`
This class is used to represent data with significant figures, and supports basic operations (+,-,\*, and /) with rules in place that ensure the correct number of figures in the result. It should be noted that the constructors generated by @dataclass should NOT be trusted to generate true "sigfigs", since they are just copying data. To generate a sigfig, it is *strongly* recommended that you use the `from_float` function to specify the value and the number of significant figures you want it to have. For instance, the following operations proceed correctly:
```
import standard_scientific as si
a = si.SigFig.from_float(99.9001, 3) #99.9001 rounded to 3 sig figs
b = si.SigFig.from_float(0.1, 2) #0.1 with 2 sig figs (assuming trailing zeros)
a + b == si.SigFig.from_float(1e3, 4), #100.0 with 4 sig figs (asuming trailing zeros)
```
Where the number of sig figs passed in are used to round the provided value to the correct number of digits (with an important exception discussed below). 

### A Note on SigFig Comparison. 
Comparison of floating point numbers is inherently a dangerous and complicated process. The inclusion of Significant Figures simplifies this process to some extent, as it provides a rigerous description of exactly which places in a number can be considered, which, *generally*, is far fewer places than significant figures in floating point (double precision) numbers. *However*, there are still edge cases that can be the source of frustration. Take for example the following code snippit:

```
x = si.SigFig.from_float(value = 1.5, sigfigs = 1) #Does this round to 1 or 2?
``` 

The obvious problem is that this exact scenario is a grey zone in the practical implementation of significant figures, the problem being that 1.5 is not actually 1.5 (exactly 3/2), but rather float(1.5), which comes with questions of machine precision. In this case we can resolve the problem by taking the rounding out of the hands of the SigFig class, and instead using `x = si.SigFig(value = 2, sigfigs = 1)`. However, a more insidious problem arrises when:

```
x = si.SigFig.from_float(value = 1, sigfigs = 1)
y = si.SigFig.from_float(value = 0.50, sigfigs = 2)
z = x - y #will this be 1 or 0?? 
```

where we encounter the strange situation that `1 - 0.50` might, in fact, be either `1` or `0` *depending on the machine noise of the difference in the values*, and that either result *should* be considered as different values in significant figures! This is a natural consequence of the issues comparing floating point number (for a better description, see *https://randomascii.wordpress.com/2012/02/25/comparing-floating-point-numbers-2012-edition/*). This problem is somewhat alleviated when uncertainties are provided with the given value, but in the SigFigs class we must settle for providing the user with a warning when it detects the rounding in the `from_float` constructor is sensitive to noise. For you precision nerds out there, this is currently implemented as a check that  `x + x*eps` and `x - x*eps` round to the same SigFig if `|x| > 1` and compares the rounding between `x + eps` and `x - eps` otherwise. The comparison between SigFigs is implemented as a check that they differ by less than 0.5 in the last significant digit.  

## `SciData`
Class that supports the representation of scientific data. Implicit within this is that each datum is given in four parts, the *value* (`obj.value`) of the data and the *standard uncertainty* (`obj.unc`) of the data, the *relative standard uncertainty* (`obj.rel_unc`), and a flag controlling the *exactness* of the class (`obj.is_exact`). While the relative standard uncertainty is not  There is additional support for *exact* (see below for additional comments) vs *inexact* data, as the former is required for particular definitions. 

### Construction of SciData
As in the SigFig class, the default constructors are generated by @dataclass and should *only* be used for copying and moving instances of SciData. For proper construction, please us the following functions: 
    - `from_str(string)` 
    - `from_SigFigs(value, unc, rel_unc, is_exact)`
    - `exact_from_float(float)` 

The string construction, in part, also serves as a significant figure interpreter. It accepts strings of the following form:
`"12.345(67) x 10-23"`, and parses the string into a value, an uncertainty, and an exponent section (the last of which may be indicated with the following list of strings: `E, e, x10**, x10^, x10` [invariant to whitespace]). *THIS IMPLEMENTATION IS UNDER CONSTRUCTION*. If no exponent section is given, the exponent is taken as unity. The uncertainty indicated "inherits" the last *n* digits of the given value, where *n* is the number of significant figures in the value minus the number of significant figures in the uncertainty. In the above example, the given uncertainty would be `0.067 x 10-23`. If no uncertainty is given, the value is taken to be exact (see comments on the corresponding complexities in the later section). Significant figures for the value and standard uncertainty are determined from the number of provided digits (in inexact cases) or from specific cases listed below when the value is indicated to be exact. 

The usual significant figure rules apply---leading zeros are never considered significant, all digits after a decimal are considered significant---but with an added convention that the placement of the uncertainty section indicates the final significant digit even in cases of trailing zeros. That is, `123000(1)` is taken as `1.23000e5` (six significant figures) with an uncertainty of `1e0` (one significant figure). 


### Utilities in SciData
Under construction.


### A note on "exact" SciData
There are often times where scientific data is not represented with a standard uncertainty because the data comes from a source that is defined exactly. For instance, the speed of light in CODATA 2022 is defined as *exactly*, 299 792 458 m s-1, a statement that implies this values has an *infinite* number of significant figures. However, this comes with two significant caviats. First, as above, numerical precision in floating point arithmatic demands that we are actually *not* exactly certain of the value, just certain of this value up to machine precision. Further, the user may construct a piece of scientific data from a string where only the first *n* digits of an infinite number of digits is given (think pi). In which case, our *actual* uncertainty is the number of digits given by the string. 

As such, we are forced to adopt the following conventions. 
    - If the SciData is generated with `from_str`, we take an exact value, `x`, to have significant figures to either the number of decimal places writen (only if there is a "." in the string) or the negative of the exponent of `x * eps`, whichever is smaller.
    - If the SciData is generated from a SigFig, we use the exact values contained within input.
    - If the SciData is generated from `exact_from_float`, we take the exact value, `x`, to have significant figures equal to the negative of the exponent of `x * eps`. 

## Requirements
    * pytest
    * python3.0 or later
    * numpy

## Installation
    `python3 -m pip install .`

Testing provided by executing `pytest -W error` within the tests directory. 

## Import
    `import standard_scientific as si`


