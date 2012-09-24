'''
Created on Sep 21, 2012

@author: sean
'''
from argparse import ArgumentParser, FileType
from tracmass.utils import read_params
from tracmass import _tracmass as tm

def main():
    parser = ArgumentParser()
    parser.add_argument('-g', '--grid-params', type=FileType('r'), required=True)
    parser.add_argument('--part-quant', default=1)
    parser.add_argument('--isec', default=4)
    parser.add_argument('--idir', default=0)
    parser.add_argument('--nqua', default=1)
    
    parser.add_argument('--ist1', default=10)
    parser.add_argument('--ist2', default=10)
    parser.add_argument('--jst1', default=50)
    parser.add_argument('--jst2', default=50)
    parser.add_argument('--kst1', default=5)
    parser.add_argument('--kst2', default=5)
    
    args  = parser.parse_args()

    read_params(args.grid_params)
    
    tm.mod_param.partquant = args.part_quant
    tm.mod_param.partquant = args.part_quant
    tm.mod_seed.isec = args.isec
    tm.mod_seed.idir = args.idir
    tm.mod_seed.nqua = args.nqua
    tm.mod_seed.seedtype = 1
    
    tm.mod_seed.ist1 = args.ist1
    tm.mod_seed.ist2 = args.ist2
    tm.mod_seed.jst1 = args.jst1
    tm.mod_seed.jst2 = args.jst2
    tm.mod_seed.kst1 = args.kst1
    tm.mod_seed.kst2 = args.kst2

    
    tm.init_params2()
    tm.coordinat()
    
    tm.mod_grid.kmt[:] = tm.mod_param.km
    
    if tm.mod_seed.nqua == 1:  # number of trajectories (per time resolution)
        # num=NTRACMAX
        tm.mod_seed.num = tm.mod_param.partquant
    elif tm.mod_seed.nqua == 2: 
        tm.mod_param.voltr = tm.mod_param.partquant 
    elif tm.mod_seed.nqua == 3: 
        tm.mod_param.voltr = tm.mod_param.partquant
        
    tm.mod_traj.trj[:] = 0
    tm.mod_traj.nrj[:] = 0
    
    tm.init_seed()
    
    tm.mod_seed.seed(0, 0)
    
    print tm.mod_seed.seed_ijk
    print tm.mod_traj.trj
    

if __name__ == '__main__':
    main()
    
