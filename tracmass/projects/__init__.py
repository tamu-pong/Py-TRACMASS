
from os.path import dirname
from pkgutil import walk_packages
import numpy as np
from tracmass import _tracmass as tm

class Project(object):
    
    def __init__(self, args):
        tm.loop.writedata = self.writedata
        tm.loop.readfields = self.readfields
        self.args = args
    
    @classmethod
    def commandline_args(cls, parser):
        '''
        Add any extra command line arguments here.
        '''
        parser.set_defaults(project=cls)

__all__ = ['get_commands']

def command_names():
    for _, name, _ in walk_packages([dirname(__file__)]):
        yield name
    
def get_projects():
    for imprt, name, _ in walk_packages([dirname(__file__)]):
        mod = imprt.find_module(name).load_module(name)
        
        if not hasattr(mod, 'project'):
            raise Exception("Command module %s not a valid command file requires function 'project'" % (name))
        
        yield name, mod.project

