'''
Created on Sep 21, 2012

@author: sean
'''
from argparse import ArgumentParser, FileType
from tracmass.utils import read_params, print_state
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
    parser.add_argument('-r', '--run-params', type=FileType('r'))
    parser.add_argument('-g', '--grid-params', type=FileType('r'))
    parser.add_argument('-s', '--set', nargs=2, action='append')
    parser.add_argument('--seed')
    parser.add_argument('--exit')
    parser.add_argument('--path')
    parser.add_argument('--start')
    parser.add_argument('--end')
    parser.add_argument('--delta-hours')
    parser.add_argument('--delta-minutes')
    parser.add_argument('--delta-seconds')
    parser.add_argument('--print-state', action='store_true')
    
    args = parser.parse_args()
    
    read_params(args.run_params)
    read_params(args.grid_params)
    
    tm.init_params2()
    tm.coordinat()
    setup()
    
    
    tm.mod_grid.kmt[:] = tm.mod_param.km
    
    tm.allocate_seed(1)
    tm.mod_seed.isec = 5
    tm.mod_seed.seed_ijk[:,:] = 2 
    tm.mod_seed.seed_xyz[:,:] = [[9.125,  49.125, 4.5]] 
    tm.mod_seed.seed_set[:] = [tm.mod_seed.isec, tm.mod_seed.idir] 

    if args.print_state:
        print_state()
        return
    
    print tm.mod_traj.trj.shape
    print tm.mod_traj.trj[:1,:]
    
    def writedata(*args):
        print tm.mod_traj.trj[:1,:]
        print tm.writedata2(*args)
        
    tm.loop.writedata = tm.writedata2
    tm.loop.readfields = tm.tes_readfields
    
    tm.loop()
    
    print "Done!"
    
    
if __name__ == '__main__':
    main()
