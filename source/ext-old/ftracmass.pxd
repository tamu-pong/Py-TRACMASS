
    
cdef extern from "ftracmass.h":
    
    void file_open(int *fd, char *filename, int flen)

      
    void init_params()
    int ntracmax
    
    # Module Name
    char outDataFile[200]
    char outDataDir[200]
    char GCMname[200]
    char gridName[200]
    char caseName[200]
    char caseDesc[200]
    int intminInOutFile
    
    # Module Seed
    int nff
    int nqua
    int num
    
    void init_seed()
    # Module Time
    int intmin, intmax, intstart, intend
    double partQuant, voltr
    
    void simple_print()
    
    
    # Module Vel
    
    float *uflux, *vflux
    void get_uflux_shape(int*)
    void get_vflux_shape(int*)

