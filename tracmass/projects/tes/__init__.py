'''
The tes project command line  
'''

from tracmass.projects import Project
from tracmass import _tracmass as tm
import numpy as np

class Tes(Project):
    writedata = tm.writedata2
    readfields = tm.tes_readfields
    
    @classmethod
    def commandline_args(cls, parser):
        '''
        Add any extra command line arguments here.

        The *subcommand* name 'tes' is gotted from this module's name.
           
        '''
        parser.add_argument('--grid')
        parser.set_defaults(project=cls)
        
    def seed(self, args):
        '''
        Seed should return an array of particles. coords are in lat, lon, with optional depth
        '''
        particles = np.array([[9.125, 49.125], [8.125, 49.125], [8.125, 48.125]])
        return particles

project = Tes
