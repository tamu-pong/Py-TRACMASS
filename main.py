#!/usr/bin/env python
'''
Created on Sep 18, 2012

@author: sean
'''

import tracmass as tm
from os.path import abspath, join, curdir
    
def writesetup():

    print '======================================================'
    print '=== tm lagrangian off-line particle tracking ==='
    print '------------------------------------------------------'
    print 'Start date  : '
    print 'Start time  : '
    print 'Model code  : ', tm.name.gcm_name.strip()
    print 'Data surce  : ', tm.name.grid_name.strip()
    print 'Run name    : ', tm.name.case_name.strip()
    print 'Description : ', tm.name.case_desc.strip()
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
    
    print 'tm.time.intmin', tm.time.intmin
    print 'tm.time.intmax', tm.time.intmax
    
    if tm.seed.nff == 1: #Forward
        print "Forward"
        tm.time.intstart = tm.time.intmin          
        tm.time.intend = tm.time.intmax
    else: #Backward
        print "Backward"
        tm.time.intstart = tm.time.intmin          
        tm.time.intend = tm.time.intmax
    
    print "tm.time.intstart", tm.time.intstart
    print "tm.time.intend", tm.time.intend
    tm.seed.init()
    
    filename = abspath(join(curdir, 'results-new', 'data'))
        
    print "filename", filename
    print "tm.seed.nqua", tm.seed.nqua
    if tm.seed.nqua == 1:  # number of trajectories (per time resolution)
        # num=NTRACMAX
        print "tm.params.part_quant", tm.params.part_quant, tm.seed.num
        tm.seed.num = tm.params.part_quant
    elif tm.seed.nqua == 2: 
        tm.params.voltr = tm.params.part_quant 
    elif tm.seed.nqua == 3: 
        tm.params.voltr = tm.params.part_quant
    
    tm.fortran_file(56, filename + '_run.asc' ) # trajectory path
    tm.fortran_file(57, filename + '_out.asc' )       # exit position
    tm.fortran_file(58, filename + '_in.asc' )        # entrance position
    tm.fortran_file(59, filename + '_err.asc')       # Error position
    
    
    tm.loop.readfields = tm.tes_readfields
    tm.loop()
    
    print "Done!"
    
if __name__ == '__main__':
    main()
