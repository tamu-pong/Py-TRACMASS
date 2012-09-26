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
        parser.add_argument('--run')
        parser.set_defaults(project=cls)
        
        
    def __init__(self, args):
        Project.__init__(self, args)
        
        from os.path import abspath, join, curdir
        filename = abspath(join(curdir, 'results-new', 'data'))
        
        tm.fortran_file(56, filename + '_run.asc')       # trajectory path
        tm.fortran_file(57, filename + '_out.asc')       # exit position
        tm.fortran_file(58, filename + '_in.asc')        # entrance position
        tm.fortran_file(59, filename + '_err.asc')       # Error position
    
    
    def seed(self, args):
        '''
        Seed should return an array of particles. coords are in lat, lon, with optional depth
        '''
        particles = np.array([[9.125, 49.125], [8.125, 49.125], [8.125, 48.125]])
        return particles

project = Tes
