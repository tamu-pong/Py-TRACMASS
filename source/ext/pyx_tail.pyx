
cimport ftracmass

def tes_readfields():
    ftracmass.tes_readfields()
    
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
            helper.fw_loop()

loop = _LOOP_()

cdef public void readfields() nogil:
    with gil:
        loop.readfields()
