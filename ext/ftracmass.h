
#include "fortran_defines.h"
/* ==== ==== ==== ==== ==== ==== ==== ==== ==== ==== ==== ==== ==== ==== ==== ==== 
 *
 * ==== ==== ==== ==== ==== ==== ==== ==== ==== ==== ==== ==== ==== ==== ==== ==== */
#define file_open FORTRAN_MANGLE(file_open)
void file_open(int *fd, char *filename, int flen);
#define simple_print FORTRAN_MANGLE(simple_print)
void simple_print(void);

#define tes_readfields FORTRAN_MANGLE(tes_readfields)
void tes_readfields();
