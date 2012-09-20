
cimport ftracmass
cimport numpy
cimport cpython
from numpy_supplement cimport *
import numpy

cdef extern from "stdlib.h":
    void* malloc(size_t)
    
cdef extern from "Python.h":
    object PyMemoryView_FromBuffer(Py_buffer *)
        
def coordinat():
    ftracmass.coordinat()

def tes_readfields():
    ftracmass.tes_readfields()
    
def simple_print():
    ftracmass.simple_print()
    
class fortran_file():
    def __init__(self, fd, filename):
        
        cdef int _fd = 0
        cdef char *_filename = NULL
        
        _fd = fd
        
        if filename:
            tmp = filename.encode()
            _filename = tmp
            
        cdef int _len = len(tmp)
        ftracmass.file_open(&_fd, _filename, _len)
        
        self.fortran_fileno = fd
        self.filename = filename
    
class _LOOP_(object):
    def __init__(self, readfields=None):
        self.readfields = readfields
        
    def __call__(self):
        if self.readfields is None:
            raise AttributeError("must set loop.readfields before inital call!")
        
        with nogil:
            ftracmass.loop()

loop = _LOOP_()

cdef public void readfields() nogil:
    with gil:
        loop.readfields()

def init_params():
    ftracmass.init_params()
    
class _PARAMS_(object):
    def __repr__(self):
        '''
        Wrapper of fortran module params 
        '''
    def _get_ntracmax(self):
        return ftracmass.ntracmax
    
    def _set_ntracmax(self, value):
        ftracmass.ntracmax = value

    ntracmax = property(_get_ntracmax, _set_ntracmax)
    
    def _get_voltr(self):
        return ftracmass.voltr
    def _set_voltr(self, value):
        ftracmass.voltr = value
    voltr = property(_get_voltr, _set_voltr)

    def _get_partQuant(self):
        return ftracmass.partQuant
    def _set_partQuant(self, value):
        ftracmass.partQuant = value
    part_quant = property(_get_partQuant, _set_partQuant)

class _TIME_(object):
    def _get_intstart(self):
        return ftracmass.intstart
    def _set_intstart(self, value):
        ftracmass.intstart = value
    intstart = property(_get_intstart, _set_intstart)

    def _get_intend(self):
        return ftracmass.intend
    
    def _set_intend(self, value):
        ftracmass.intend = value
        
    intend = property(_get_intend, _set_intend)

    def _get_intmin(self):
        return ftracmass.intmin
    def _set_intmin(self, value):
        ftracmass.intmin = value
    intmin = property(_get_intmin, _set_intmin)
    
    def _get_intmax(self):
        return ftracmass.intmax
    def _set_intmax(self, value):
        ftracmass.intmax = value
    intmax = property(_get_intmax, _set_intmax)

    
class _SEED_(object):
    
    def init(self):
        ftracmass.init_seed()
        
    def _get_nff(self):
        return ftracmass.nff
    def _set_nff(self, value):
        ftracmass.nff = value
    nff = property(_get_nff, _set_nff)
    
    def _get_nqua(self):
        return ftracmass.nqua
    def _set_nqua(self, value):
        ftracmass.nqua = value
    nqua = property(_get_nqua, _set_nqua)

    def _get_num(self):
        return ftracmass.num
    def _set_num(self, value):
        ftracmass.num = value
    num = property(_get_num, _set_num)

class _NAME_(object):
    
    def _get_intminInOutFile(self):
        return ftracmass.intminInOutFile
    
    def _set_intminInOutFile(self, value):
        ftracmass.intminInOutFile = value
        
    int_min_inout_file = property(_get_intminInOutFile, _set_intminInOutFile)


    def _get_outDataFile(self):
        return bytes(ftracmass.outDataFile[:200])
    
    def _set_outDataFile(self, value):
        ftracmass.outDataFile[:200] = value[:200]

    data_file = property(_get_outDataFile, _set_outDataFile)
    
    def _get_outDataDir(self):
        return ftracmass.outDataDir[:200]
    
    def _set_outDataDir(self, value):
        ftracmass.outDataDir[:200] = value
        
    data_dir = property(_get_outDataDir, _set_outDataDir)

    def _get_GCMname(self):
        return bytes(ftracmass.GCMname[:200])
    
    def _set_GCMname(self, value):
        ftracmass.GCMname[:200] = value[:200]

    gcm_name = property(_get_GCMname, _set_GCMname)
    
    def _get_gridName(self):
        return bytes(ftracmass.gridName[:200])
    
    def _set_gridName(self, value):
        ftracmass.gridName[:200] = value[:200]

    grid_name = property(_get_gridName, _set_gridName)
    
    def _get_caseName(self):
        return bytes(ftracmass.caseName[:200])
    
    def _set_caseName(self, value):
        ftracmass.caseName[:200] = value[:200]

    case_name = property(_get_caseName, _set_caseName)
    
    def _get_caseDesc(self):
        return bytes(ftracmass.caseDesc[:200])
    
    def _set_caseDesc(self, value):
        ftracmass.caseDesc[:200] = value[:200]

    case_desc = property(_get_caseDesc, _set_caseDesc)
    

class _VEL_(object):
    
    def _get_uflux(self):
        
        cdef int uflux_shape[4]
        cdef numpy.npy_intp dims[4]
        ftracmass.get_uflux_shape(uflux_shape)
        
        dims[0] = uflux_shape[0]
        dims[1] = uflux_shape[1]
        dims[2] = uflux_shape[2]
        dims[3] = uflux_shape[3]
        
        print dims[0],dims[1], dims[2], dims[3] 
        return PyArray_New(&PyArray_Type, 4, dims, NPY_FLOAT, NULL, ftracmass.uflux, 0, NPY_FARRAY, None)
    
    uflux = property(_get_uflux)

    def _get_vflux(self):
            
        cdef int _shape[4]
        cdef numpy.npy_intp dims[4]
        ftracmass.get_vflux_shape(_shape)
        
        dims[0] = _shape[0]
        dims[1] = _shape[1]
        dims[2] = _shape[2]
        dims[3] = _shape[3]
        
        return PyArray_New(&PyArray_Type, 4, dims, NPY_FLOAT, NULL, ftracmass.vflux, 0, NPY_FARRAY, None)
        
    vflux = property(_get_vflux)


vel = _VEL_()
time = _TIME_()
seed = _SEED_()
params = _PARAMS_()
name = _NAME_()


import_array()
