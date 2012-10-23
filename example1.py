'''
Created on Sep 28, 2012

@author: sean
'''
from datetime import datetime, timedelta

#Wrapped fortran trackmass module
from tracmass import _tracmass as tm
from tracmass.projects import Project
import numpy as np
from argparse import ArgumentParser
import netCDF4

class ROMS(Project):
    def writedata(self, sel, t0, temp, x1, y1, z1, niter, salt, dens):
        '''
        Write out data. this is called for every particle and every iteration.
        This is very slow in python and perhaps should be stored into a numpy array and called only once per iteration. 
        Also: the actual check to write to file is inside `tm.writedata2`
        '''
        #Wrapped from fortran tracmass source/src/loop/f95
        
        if tm.mod_traj.nrj[tm.mod_param.ntrac - 1, 3] == niter - 1:
            self.trajectory[tm.mod_param.ntrac - 1].append((x1, y1, z1))
        
    def readfields(self):
        '''
        Robert focus your effort here.
        
        You must access and set the uflux and vflux variables. 
        
        '''
        #Here are the relevant fortran modules. Static variables are contained within
        param = tm.mod_param
        time = tm.mod_time
        grid = tm.mod_grid
        vel = tm.mod_vel
        
        FIXME_AREA =  1000000
        
        if time.ints == time.intstart:
            print time.ints
            vel.hs[:] = 0
            
            print vel.uflux.shape
            print vel.vflux.shape
            print self.u.shape
            print self.v.shape
            
            vel.uflux[:] = 0
            vel.vflux[:] = 0
            
            vel.uflux[:-1, :, :, 1] = self.u[time.ints].transpose(2, 1, 0) * FIXME_AREA
            vel.vflux[:, :-2, :, 1] = self.v[time.ints].transpose(2, 1, 0) * FIXME_AREA
            
            grid.kmt[:] = param.km
        
            tm.coordinat()
            
        #Assign
        vel.uflux[:, :, :, 0] = vel.uflux[:, :, :, 1]
        vel.vflux[:, :, :, 0] = vel.vflux[:, :, :, 1]
        
        vel.uflux[:-1, :, :, 1] = self.u[time.ints].transpose(2, 1, 0) * FIXME_AREA
        vel.vflux[:, :-2, :, 1] = self.v[time.ints].transpose(2, 1, 0) * FIXME_AREA
        
        print 'ints', time.ints
        
    def __init__(self, nc, start, end, delta):
        
        #This sets a lot of the fortran static variables
        Project.__init__(self, nc.variables['ocean_time'].size, start, end, delta)
        
        self.nc = nc
        self.u = nc.variables['u']
        self.v = nc.variables['v']
        
        tm.mod_param.imt = len(nc.dimensions['xi_rho'])
        tm.mod_param.jmt = len(nc.dimensions['eta_rho'])
        tm.mod_param.km = len(nc.dimensions['s_rho'])
        
        ngcm = (nc.variables['ocean_time'][1] - nc.variables['ocean_time'][0]) / (3600)
        tm.mod_param.ngcm = ngcm
        
        tm.mod_param.iter = 100 # iteration between two gcm data sets (always =1 for timeanalyt)
        
    
        
def main():
    
    parser = ArgumentParser()
    parser.add_argument('-i', '--input')
    
    args = parser.parse_args()
    
    nc = netCDF4.Dataset(args.input)
    
    start = datetime.now()
    end = start + timedelta(days=6)
    delta = timedelta(hours=4)
    
    roms = ROMS(nc, start, end, delta)
    
    #Initialize trackmass to only seed once. 
    #seeding can be done here in and outer loop if more times are required
    #This also sets a lot of the fortran static variables
     
    seed_locations = np.array([
                               [207.125, 55.125, 4.5],
                               [210.125, 55.125, 4.5],
                               [213.125, 55.125, 4.5],

                               [207.125, 57.125, 4.5],
                               [210.125, 57.125, 4.5],
                               [213.125, 57.125, 4.5],

                               [207.125, 59.125, 4.5],
                               [210.125, 59.125, 4.5],
                               [213.125, 59.125, 4.5],
                               ])
    
    roms.setup_tracmass(seed_locations)
    
#    tm.init_seed()
    #Runs the main loop
    roms.run()
    
    import pickle
    pickle.dump(roms.trajectory, open('roms.trajectory.pickle', 'w'))
    

if __name__ == '__main__':
    main()
