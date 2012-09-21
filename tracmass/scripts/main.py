#!/usr/bin/env python
'''
Created on Sep 18, 2012

@author: sean
'''

from tracmass import _tracmass as tm
from os.path import abspath, join, curdir
import math
import numpy as np
from tracmass.utils import print_state
    
def readfields():
    param = tm.mod_param
    coord = tm.mod_coord
    time = tm.mod_time
    grid = tm.mod_grid
    tm.mod_name
    vel = tm.mod_vel
    tm.mod_dens
    
    tm.tes_readfields()
    return 
    
    time.ihour = time.ihour + 6
    if time.ihour == 24:
        time.ihour = 0
        time.iday = time.iday + 1
        if time.iday > coord.idmax[time.imon-1, time.iyear-1000]:
#        if time.iday > 30:
            time.iday = 1
            time.imon = time.imon + 1
            if time.imon == 13:
                time.imon = 1
                time.iyear = time.iyear + 1
                if time.iyear > time.yearmax: time.iyear = time.yearmin # recycle over gcm outputdata

#    print time.ints, time.intstart
#    return

    deg = 6371229.* (math.pi / 180.)
    
    if time.ints == time.intstart:
        print "Init Fields"
        vel.hs[:] = 0
        vel.uflux[:] = 0
        vel.vflux[:] = 0
        grid.kmt[:] = param.km
        
        coord.dxdeg = coord.dx * deg
        coord.dydeg = coord.dy * deg
        
        time.iyear = time.startyear
        time.imon = time.startmon
        time.iday = time.startday
        time.ihour = time.starthour
        
        print 'iyear=', time.iyear, time.imon, time.iday, time.ihour, coord.dxdeg, coord.dydeg
        
        tm.coordinat()
        
    vel.uflux[:, :, :, 0] = vel.uflux[:, :, :, 1]
    vel.vflux[:, :, :, 0] = vel.vflux[:, :, :, 1]

    time.ntime = 1000000 * time.iyear + 10000 * time.imon + 100 * time.iday + time.ihour

    time.omtime = time.ints / 5. + 1.
    

    cox = 0.5 + 0.5 * np.cos(time.omtime)
    coy = 0.5 + 0.5 * np.cos(time.omtime + np.pi)
    
    #    ! cox = 0.d0 ! stationary
    uwe = -0.4
    dl = time.ints * 0.01 * np.pi
    
    ii = np.cos(np.pi * (np.arange(param.imt) - param.imt / 2.) / (param.imt) + dl).reshape([param.imt, 1, 1])
    jj = np.sin(-np.pi * (np.arange(param.jmt) - param.jmt / 2.) / (param.jmt)).reshape([1, param.jmt, 1])
    
    vel.uflux[:, :, :, 1] = ((coord.dy * deg * cox * grid.dz) * (ii * jj + (uwe + np.cos(time.omtime))))
    
    ii = np.sin(np.pi * (np.arange(param.imt) - param.imt / 2.) / (param.imt) + dl).reshape([param.imt, 1, 1])
    jj = np.cos(np.pi * (np.arange(param.jmt) - param.jmt / 2.) / (param.jmt)).reshape([1, param.jmt, 1])

    vel.vflux[:, 1:, :, 1] = ((coord.dx * deg * coy * grid.dz) * (ii * jj + np.sin(time.omtime)))
    
    vel.vflux[:, 0, :, :] = 0.
    vel.vflux[:, param.jmt, :, :] = 0.

    import pickle
    pickle.dump(vel.uflux, open('vel.uflux-new.picle', 'w'))
    return 

def writesetup():

    print '======================================================'
    print '=== tm lagrangian off-line particle tracking ==='
    print '------------------------------------------------------'
    print 'Start date  : '
    print 'Start time  : '
    print 'Model code  : ', tm.mod_name.gcmname.strip()
    print 'Data surce  : ', tm.mod_name.gridname.strip()
    print 'Run name    : ', tm.mod_name.casename.strip()
    print 'Description : ', tm.mod_name.casedesc.strip()
    print '------------------------------------------------------'
    
    '''
      subroutine writesetup
        character (len=15)                           :: currDate ,currTime
        
        call date_and_time(currDate, currTime)
        
        print *,'======================================================'
        print *,'=== tm lagrangian off-line particle tracking ==='
        print *,'------------------------------------------------------'
        print *,'Start date  : '//currDate(1:4)//'-'//currDate(5:6)//'-'//currDate(7:8)
        print *,'Start time  : '//currTime(1:2)// ':'//currTime(3:4)// ':'//currTime(5:6)
        print *,'Model code  : '//trim(GCMname)
        print *,'Data surce  : '//trim(gridName)
        print *,'Run name    : '//trim(caseName)
        print *,'Description : '//trim(caseDesc)
        print *,'------------------------------------------------------'
    #ifdef timeanalyt 
        print *,'Analytical time scheme used to solve the differential Eqs.'
    #elif defined timestep
        print *,'Time steps with analytical stationary scheme used to solve the differential Eqs.'
    #elif defined timestat
        print *,'Steady state velocity fields with analytical stationary scheme used to solve the differential Eqs.'
    #endif
    #if defined tempsalt
    #if defined ifs
        print *,'Temperature and humidity fields included'
    #else
        print *,'Temperature and salinity fields included'
    #endif
    #endif
    #if defined turb
        print *,'with sub-grid turbulence parameterisation'
    #endif
    #if defined diffusion
        print *,'with diffusion parameterisation, Ah=',ah,'m2/s and Av=',av,'m2/s'
    #if defined anisodiffusion
        print *,'with anisotropic elliptic diffusion along the isopleths'
    #endif
    #endif
    #if defined rerun
        print *,'Rerun in order to store the Lagrangian stream functions in the different basins'
    #endif
    #if defined twodim                                             
        print *,'Two-dimensional trajectories, which do not change depth'
    #endif
    #if defined full_wflux
        print *,' 3D vertival volume flux field.'
    #endif
    #if defined explicit_w
        print *,'Given vertical velocity.'
    #endif
    #if defined sediment                                             
        print *,'Sedimentation including resuspension activated'
    #endif
    
    
    #if defined streamxy
        print *,'Lagrangian horizontal stream function stored'
    #endif
        
    #if defined streamv
        print *,'Lagrangian vertical depth stream function stored'
    #endif
        
    #if defined streamr
    #if defined streamts
    #if defined ifs
        print *,'Lagrangian density, temperature and humidity stream function stored'
    #else
        print *,'Lagrangian density, temperature and salinity stream function stored'
    #endif
    #else
        print *,'Lagrangian density stream function stored'
    #endif
    #endif
    
    #if defined stream_thermohaline
        print *,'Lagrangian thermohaline stream function stored'
    #endif
        
    #if defined tracer
        print *,'Lagrangian trajectory particle tracer stored'
    #endif
    
      end subroutine writesetup
    '''
def main():
    
    
    tm.init_params()
    tm.coordinat()
    writesetup()
    
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
    tm.init_seed()
    
    filename = abspath(join(curdir, 'results-old', 'data'))
        
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
    
    tm.loop.readfields = readfields
    
#    print_state()
    tm.loop()
    print "Done!"
    
if __name__ == '__main__':
    main()
