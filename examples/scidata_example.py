import standard_scientific as si

# Possibly the most useful feature of the SciData class it the string interpretor
c = si.SciData.from_str("299792458") # the speed of light! "fixed" from CODATA 2022
Eh = si.SciData.from_str("4.359 744 722 2060(48) x 10-18") #copied from nist!

print(f"The speed of light is {c}")
print(f"The Hartree Energy is {Eh}")

print(f"The value of Eh is : {Eh.value}")
print(f"The standard uncertainty of Eh is : {Eh.unc}")
print(f"The relative standard ucnertainty of Eh is : {Eh.rel_unc}")
