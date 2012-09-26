'''
Created on Sep 24, 2012

@author: sean
'''
from argparse import ArgumentParser, ArgumentTypeError
from tracmass.projects import get_projects
import netCDF4
import numpy as np
from tracmass.utils import read_params
from tracmass import _tracmass as tm

from datetime import datetime, timedelta

TIME_FMT1 =  '%d/%m/%Y'
TIME_FMT =  '%d/%m/%Y-%H:%M:%S'

def timedeltatype(key):
    def TimeDelta(arg):
        return timedelta(**{key:float(arg)})
    return TimeDelta

def timetype(arg):
    try:
        return datetime.strptime(arg, TIME_FMT1)
    except ValueError as err:
        pass
    
    try:
        return datetime.strptime(arg, TIME_FMT)
    except ValueError as err:
        raise ArgumentTypeError(err.message)

    
def main():
    
    parser = ArgumentParser()
    parser.add_argument('--seed', required=True)
    parser.add_argument('--start', type=timetype)
    parser.add_argument('--end', type=timetype)
    parser.add_argument('--delta-hours', type=timedeltatype('hours'), default=timedelta(hours=0))
    parser.add_argument('--delta-days', type=timedeltatype('days'), default=timedelta(days=0))
    
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
    
    prj.setup_tracmass(locations)
    


#    tm.loop()

    
if __name__ == '__main__':
    main()

