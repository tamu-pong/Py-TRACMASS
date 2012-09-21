'''
Created on Sep 21, 2012

@author: sean
'''
from argparse import ArgumentParser, FileType
from tracmass.utils import read_params, print_state
from tracmass import _tracmass as tm

def setup():
    print 'tm.time.intmin', tm.mod_time.intmin
    print 'tm.time.intmax', tm.mod_time.intmax
    
    if tm.mod_seed.nff == 1: #Forward
        print "Forward"
        tm.mod_time.intstart = tm.mod_time.intmin          
        tm.mod_time.intend = tm.mod_time.intmax
    else: #Backward
        print "Backward"
        tm.mod_time.intstart = tm.mod_time.intmin          
        tm.mod_time.intend = tm.mod_time.intmax
    
    print "tm.time.intstart", tm.mod_time.intstart
    print "tm.time.intend", tm.mod_time.intend
    tm.mod_grid.kmt[:] = tm.mod_param.km
    tm.init_seed()
    
    from os.path import abspath, join, curdir
     
    filename = abspath(join(curdir, 'results-new', 'data'))
        
    print "filename", filename
    print "tm.mod_seed.nqua", tm.mod_seed.nqua
    
    if tm.mod_seed.nqua == 1:  # number of trajectories (per time resolution)
        # num=NTRACMAX
        print "tm.params.part_quant", tm.mod_param.partquant, tm.mod_seed.num
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
    parser.add_argument('--start-time')
    parser.add_argument('--end-time')
    parser.add_argument('--delta-time')
    
    args = parser.parse_args()
    
    read_params(args.run_params)
    read_params(args.grid_params)
    
    tm.init_params2()
    tm.coordinat()
    setup()
    
    tm.loop.writedata = tm.writedata2
    
    
    print "Done!"
    
    
if __name__ == '__main__':
    main()
