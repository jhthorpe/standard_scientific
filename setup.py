# setup.py
#
# Setup script for installing this package
#
# Revision History:
#   April 2, 2025 : JHT added
# 

from setuptools import setup
from setuptools import find_packages 

setup(
    name='standard_scientific',
    verion='0.0.1',
    author='James H. Thorpe',
    author_email='james.thorpe@utexas.edu',
    description='Supports data using standard scientific notation and sig. figs.',
    license='MIT',
    packages=find_packages(), 
    long_description=open('README.md').read(),
    python_requires='>=3.0'
)
