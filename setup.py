'''
Created on Sep 20, 2012

@author: sean
'''

from setuptools import find_packages, setup

setup(
      name='tracmass',
      version='dev',
      packages=find_packages(),
      entry_points={
        'console_scripts': [
            'tracmass = tracmass.scripts.main:main',
            'tracmass_run = tracmass.scripts.run2:main',
            'tracmass_seed = tracmass.scripts.seed2:main',
        ],
    },

)
