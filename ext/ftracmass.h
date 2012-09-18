
#define FORTRAN_MODULE mod_param

#define FORTRAN_MANGLE(ATTR) ATTR
#define FORTRAN_MANGLE_MOD(MOD, ATTR) __## MOD ## _MOD_ ## ATTR

/* ==== ==== ==== ==== ==== ==== ==== ==== ==== ==== ==== ==== ==== ==== ==== ==== 
 *
 * ==== ==== ==== ==== ==== ==== ==== ==== ==== ==== ==== ==== ==== ==== ==== ==== */
#define file_open FORTRAN_MANGLE(file_open)
void file_open(int *fd, char *filename, int flen);
#define simple_print FORTRAN_MANGLE(simple_print)
void simple_print(void);


#define tes_readfields FORTRAN_MANGLE(tes_readfields)
void tes_readfields();

/* ==== ==== ==== ==== ==== ==== ==== ==== ==== ==== ==== ==== ==== ==== ==== ==== 
 *
 * ==== ==== ==== ==== ==== ==== ==== ==== ==== ==== ==== ==== ==== ==== ==== ==== */

#define ntracmax FORTRAN_MANGLE_MOD(mod_param, ntracmax)
#define partQuant FORTRAN_MANGLE_MOD(mod_param, partquant)
#define voltr FORTRAN_MANGLE_MOD(mod_param, voltr)

extern int ntracmax;
extern double partQuant, voltr;

/* ==== ==== ==== ==== ==== ==== ==== ==== ==== ==== ==== ==== ==== ==== ==== ==== 
 *
 * ==== ==== ==== ==== ==== ==== ==== ==== ==== ==== ==== ==== ==== ==== ==== ==== */

#define loop FORTRAN_MANGLE(loop)
void loop(void);

#define coordinat FORTRAN_MANGLE(coordinat)
void coordinat(void);

/* ==== ==== ==== ==== ==== ==== ==== ==== ==== ==== ==== ==== ==== ==== ==== ==== 
 * MODULE mod_name
 * ==== ==== ==== ==== ==== ==== ==== ==== ==== ==== ==== ==== ==== ==== ==== ==== */

#define outDataFile FORTRAN_MANGLE_MOD(mod_name, outdatafile)
extern char outDataFile[200];
#define outDataDir FORTRAN_MANGLE_MOD(mod_name, outdatadir)
extern char outDataDir[200];


#define GCMname FORTRAN_MANGLE_MOD(mod_name, gcmname)
extern char GCMname[200];
#define gridName FORTRAN_MANGLE_MOD(mod_name, gridname)
extern char gridName[200];
#define caseName FORTRAN_MANGLE_MOD(mod_name, casename)
extern char caseName[200];
#define caseDesc FORTRAN_MANGLE_MOD(mod_name, casedesc)
extern char caseDesc[200];
#define intminInOutFile FORTRAN_MANGLE_MOD(mod_name, intmininoutfile)
int intminInOutFile;

//   CHARACTER(LEN=200)                         :: outDataFile
//   INTEGER                                    :: intminInOutFile
//   CHARACTER(LEN=200)                         :: inDataDir ,outDataDir, topoDataDir
//   CHARACTER(LEN=200)                         :: projDesc
//   CHARACTER(LEN=200)                         :: GCMname   ,GCMsource
//   CHARACTER(LEN=200)                         :: gridName  ,gridSource
//   CHARACTER(LEN=200)                         :: gridDesc
//   CHARACTER(LEN=200)                         :: caseName  ,caseDesc
// ENDMODULE mod_name

/* ==== ==== ==== ==== ==== ==== ==== ==== ==== ==== ==== ==== ==== ==== ==== ==== 
 *
 * ==== ==== ==== ==== ==== ==== ==== ==== ==== ==== ==== ==== ==== ==== ==== ==== */


#define nff FORTRAN_MANGLE_MOD(mod_seed, nff)
#define nqua FORTRAN_MANGLE_MOD(mod_seed, nqua)
#define num FORTRAN_MANGLE_MOD(mod_seed, num)

extern int nff, nqua, num;


#define init_seed FORTRAN_MANGLE(init_seed)
void init_seed(void);



/* ==== ==== ==== ==== ==== ==== ==== ==== ==== ==== ==== ==== ==== ==== ==== ==== 
 *
 * ==== ==== ==== ==== ==== ==== ==== ==== ==== ==== ==== ==== ==== ==== ==== ==== */

#define intmin FORTRAN_MANGLE_MOD(mod_time, intmin)
#define intmax FORTRAN_MANGLE_MOD(mod_time, intmax)
#define intstart FORTRAN_MANGLE_MOD(mod_time, intstart)
#define intend FORTRAN_MANGLE_MOD(mod_time, intend)

extern int intmin, intmax, intstart, intend;









