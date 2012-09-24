'''
Created on Sep 24, 2012

@author: sean
'''
from argparse import ArgumentParser
from tracmass.projects import get_projects
import netCDF4
import numpy as np


def main():
    parser = ArgumentParser()
    parser.add_argument('--seed')
    
    subparsers = parser.add_subparsers(help='sub-command help')
    
    for name, project in get_projects():
        sub_parser = subparsers.add_parser(name)
        project.commandline_args(sub_parser)
        
    args = parser.parse_args()
    
    prj = args.project(args)
    
    particle_locations = prj.seed(args)
    
    if particle_locations.shape[1] == 2:
        locations = np.zeros([particle_locations.shape[0], 3], dtype='float64')
        locations[:, :2] = particle_locations
        locations[:, 2] = 4.5
    else:
        locations = particle_locations
    
    dataset = netCDF4.Dataset(args.seed, 'w')
    dataset.createDimension('particle', locations.shape[0])
    dataset.createDimension('loc', 3)
    nc_locations = dataset.createVariable('locations', 'f8', ('particle', 'loc'))
    nc_locations[:] = locations
    dataset.close()


    
if __name__ == '__main__':
    main()

