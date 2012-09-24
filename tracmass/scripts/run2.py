'''
Created on Sep 24, 2012

@author: sean
'''
from argparse import ArgumentParser
from tracmass.projects import get_projects
import netCDF4
import numpy as np
from tracmass.utils import read_params
from tracmass import _tracmass as tm

def setup():
    
    if tm.mod_seed.nff == 1: #Forward
        tm.mod_time.intstart = tm.mod_time.intmin          
        tm.mod_time.intend = tm.mod_time.intmax
    else: #Backward
        tm.mod_time.intstart = tm.mod_time.intmin          
        tm.mod_time.intend = tm.mod_time.intmax
    
    tm.mod_grid.kmt[:] = tm.mod_param.km
    from os.path import abspath, join, curdir
     
    filename = abspath(join(curdir, 'results-new', 'data'))
        
    if tm.mod_seed.nqua == 1:  # number of trajectories (per time resolution)
        # num=NTRACMAX
        tm.mod_seed.num = tm.mod_param.partquant
    elif tm.mod_seed.nqua == 2: 
        tm.mod_param.voltr = tm.mod_param.partquant 
    elif tm.mod_seed.nqua == 3: 
        tm.mod_param.voltr = tm.mod_param.partquant
    
    tm.fortran_file(56, filename + '_run.asc')       # trajectory path
    tm.fortran_file(57, filename + '_out.asc')       # exit position
    tm.fortran_file(58, filename + '_in.asc')        # entrance position
    tm.fortran_file(59, filename + '_err.asc')       # Error position
    
def main():
    parser = ArgumentParser()
    parser.add_argument('--seed', required=True)
    
    subparsers = parser.add_subparsers(help='sub-command help')
    
    for name, project in get_projects():
        sub_parser = subparsers.add_parser(name)
        project.commandline_args(sub_parser)
    
    args = parser.parse_args()
    
    prj = args.project(args)
    
    dataset = netCDF4.Dataset(args.seed, 'r')
    locations = dataset.variables['locations']
    
    
    read_params(open('tes_run.yaml'))
    read_params(open('tes_grid.yaml'))
    
    tm.init_params2()
    tm.coordinat()
    setup()
    
    tm.mod_grid.kmt[:] = tm.mod_param.km
    
    tm.allocate_seed(locations.shape[0])
    tm.mod_seed.isec = 5
    tm.mod_seed.seed_ijk[:,:] = 2 
    tm.mod_seed.seed_xyz[:,:] = locations
    tm.mod_seed.seed_set[:] = [tm.mod_seed.isec, tm.mod_seed.idir] 


    tm.loop()

    
if __name__ == '__main__':
    main()

