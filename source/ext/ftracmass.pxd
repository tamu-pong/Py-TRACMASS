
    
cdef extern from "ftracmass.h":
    
    void file_open(int *fd, char *filename, int flen)
    void tes_readfields()
