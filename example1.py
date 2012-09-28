'''
Created on Sep 28, 2012

@author: sean
'''
from datetime import datetime, timedelta

#Wrapped fortran trackmass module
from tracmass import _tracmass as tm
from tracmass.projects import Project
from tracmass.utils import read_params
import numpy as np

class Tes(Project):
    def writedata(self,*args):
        '''
        Write out data. this is called for every particle and every iteration.
        This is very slow in python and perhaps should be stored into a numpy array and called only once per iteration. 
        Also: the actual check to write to file is inside `tm.writedata2`
        '''
        #Wrapped from fortran tracmass source/src/loop/f95
        tm.writedata2(*args)
        
    def readfields(self):
        '''
        Robert focus your effort here.
        
        You must access and set the uflux and vflux variables. 
        
        
        '''
        
        #Here are the relevant fortran modules. Static variables are contained within
        param = tm.mod_param
        coord = tm.mod_coord
        time = tm.mod_time
        grid = tm.mod_grid
        vel = tm.mod_vel
        
        #TRY This: print dir(vel) 
        #TRY This: print vel.uflux.shape
        #TRY This: print vel.vflux.shape
        # See source/src/comments.f95 for some more info.
        
        # Wrapped from fortran tracmass.
        # Take a look in source/projects/tes/readfields.f95
        tm.tes_readfields()
    
    
        
    def __init__(self, start, end, delta):
        
        #This sets a lot of the fortran static variables
        Project.__init__(self, start, end, delta)
        
        from os.path import abspath, join, curdir
        filename = abspath(join(curdir, 'results-new', 'data'))
        
        #Initialize for tm.writedata
        tm.fortran_file(56, filename + '_run.asc')       # trajectory path
        tm.fortran_file(57, filename + '_out.asc')       # exit position
        tm.fortran_file(58, filename + '_in.asc')        # entrance position
        tm.fortran_file(59, filename + '_err.asc')       # Error position
    
    

def main():
    
    start = datetime.now()
    end = start + timedelta(days=6)
    delta = timedelta(hours=4)
    
    tes = Tes(start, end, delta)
    
    #Read parameters from yaml files into static fortran variables
    read_params(open('tes_run.yaml'))
    read_params(open('tes_grid.yaml'))

    #Initialize trackmass to only seed once. 
    #seeding can be done here in and outer loop if more times are required
    #This also sets a lot of the fortran static variables 
    seed_locations = np.array([[9.125, 49.125, 4.5], [8.125, 49.125, 4.5], [8.125, 48.125, 4.5]])
    tes.setup_tracmass(seed_locations)
    
    #Runs the main loop
    tes.run()

if __name__ == '__main__':
    main()
