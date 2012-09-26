
from os.path import dirname
from pkgutil import walk_packages
import numpy as np
from tracmass import _tracmass as tm

class Project(object):
    
    def __init__(self, args):
        
        self.times = times = []
        
        delta = args.delta_days + args.delta_hours
         
        if not delta:
            raise Exception('Time delta can not be zero!')
        forward = self.args.start < self.args.end
        
        if forward:
            dt = args.start
            while dt <= args.end:
                times.append(dt)
                dt += delta
        else:
            dt = args.end
            while dt >= args.start:
                times.append(dt)
                dt -= delta
        
        self.args = args
        
    def setup_tracmass(self, seed_locations):
        
        tm.loop.writedata = self.writedata
        tm.loop.readfields = self.readfields
        
        #Constants in this run
        tm.mod_param.lbt = 1
        tm.mod_param.nend = tm.mod_param.lbt + 1
        
        tm.init_params2()
        tm.coordinat()
        
        tm.mod_time.intrun = len(self.times)
        
        if self.args.start > self.args.end: #Backward 
            self.mod_seed.nff = 2
            self.mod_time.intstep = -1
            tm.mod_time.intstart = self.args.end.toordinal()
            tm.mod_time.intend = self.args.start.toordinal() 
        else: #Forward
            self.mod_time.intstep = 1
            self.mod_seed.nff = 1
            tm.mod_time.intstart = self.args.start.toordinal()   
            tm.mod_time.intend = self.args.end.toordinal()
        
        tm.mod_grid.kmt[:] = tm.mod_param.km
            
        if tm.mod_seed.nqua == 1:  # number of trajectories (per time resolution)
            # num=NTRACMAX
            tm.mod_seed.num = tm.mod_param.partquant
        elif tm.mod_seed.nqua == 2: 
            tm.mod_param.voltr = tm.mod_param.partquant 
        elif tm.mod_seed.nqua == 3: 
            tm.mod_param.voltr = tm.mod_param.partquant
        
        tm.mod_grid.kmt[:] = tm.mod_param.km
        
        tm.allocate_seed(seed_locations.shape[0])
        tm.mod_seed.isec = 5
        tm.mod_seed.seed_ijk[:, :] = 2 
        tm.mod_seed.seed_xyz[:, :] = seed_locations
        tm.mod_seed.seed_set[:] = [tm.mod_seed.isec, tm.mod_seed.idir] 


    
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

