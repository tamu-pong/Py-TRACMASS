
cimport ftracmass

def tes_readfields():
    ftracmass.tes_readfields()
    
class fortran_file():
    def __init__(self, fd, filename):
        
        cdef int _fd = 0
        cdef char * _filename = NULL
        
        _fd = fd
        
        if filename:
            tmp = filename.encode()
            _filename = tmp
            
        cdef int _len = len(tmp)
        ftracmass.file_open(& _fd, _filename, _len)
        
        self.fortran_fileno = fd
        self.filename = filename


class _LOOP_(object):
    def __init__(self, readfields=None, writedata=None):
        self.readfields = readfields
        self.writedata = writedata
        self.exc = None
    def __call__(self):
        if self.readfields is None:
            raise AttributeError("must set loop.readfields before inital call!")
        if self.writedata is None:
            raise AttributeError("must set loop.writedata before inital call!")
        
        self.exc = None
        with nogil:
            helper.fw_loop()

        if self.exc is not None:
            raise self.exc[0], self.exc[1], self.exc[2]


loop = _LOOP_()

import sys
cimport cpython
cdef public void readfields(int * err) nogil:
    with gil:
        try:
            loop.readfields()
        except BaseException:
            loop.exc = sys.exc_info()
            err[0] = 1
            return
        
    err[0] = 0


cdef public void writedata(int * sel, double * t0, float * temp, double * x1, double * y1, double * z1, int * niter, float * salt, float * dens, int * err) nogil:
    with gil:
        try:
            loop.writedata(sel[0], t0[0], temp[0], x1[0], y1[0], z1[0], niter[0], salt[0], dens[0])
        except BaseException:
            loop.exc = sys.exc_info()
            err[0] = 1
            return
        
    err[0] = 0
    


