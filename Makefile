###############################################################
### TEMPLATE FOR Mac OS X 10.7 with gfortran from fink ###
###############################################################
PROJECT	          = tes
# possible PROJECTS i.e. GCMs: rco, baltix, occ, orc, sim, for, ifs, tes, gomoos
CASE              = $(PROJECT)

#F95COMPILER        = "g95"
F95COMPILER        = "gfortran"

#================================================================

PROJMAKE           := $(wildcard projects/$(PROJECT)/Makefile)
ifneq ($(strip $(PROJMAKE)),)
	include projects/$(PROJECT)/Makefile
endif

PROJECT_FLAG      = -DPROJECT_NAME=\'$(PROJECT)\'
CASE_FLAG         = -DCASE_NAME=\'$(CASE)\'
ARG_FLAGS         = -DARG_INT1=$(INPUT_INT1) -DARG_INT2=$(INPUT_INT2)

#MYCFG            = /usr/local/mysql/bin/mysql_config
#MYI_FLAGS        = `$(MYCFG) --cflags` 
#MYL_FLAGS        = `$(MYCFG) --libs` 

LIB_DIR           = -L/sw/lib -L/sw/opt/netcdf7/lib
INC_DIR           = -I/sw/include -I/sw/opt/netcdf7/include \
                    -I/usr/local/mysql/include

LNK_FLAGS         = -lnetcdf -lnetcdff

#================================================================  

VPATH = src:projects/$(PROJECT)
vpath %.o tmp

ifeq ($(F95COMPILER),"gfortran")
	FF_FLAGS         = -m64 -c -x f95-cpp-input -fconvert=big-endian -gdwarf-2 -fbounds-check
	F90_FLAGS        =-fno-underscoring  
#	FF               = gfortran $(LIB_DIR) $(INC_DIR) $(F90_FLAGS) $(ORM_FLAGS)
	FF               = /sw/bin/gfortran $(LIB_DIR) $(INC_DIR) $(F90_FLAGS) $(ORM_FLAGS)

endif
ifeq ($(F95COMPILER),"g95")
	FF_FLAGS = -c -cpp -fendian=big
	F90_FLAGS        = -O3 -C  -g  -fno-underscoring
	FF               = /Applications/fort/g95/bin/i386-apple-darwin8.11.1-g95 $(LIB_DIR) $(INC_DIR) $(F90_FLAGS) $(ORM_FLAGS)
endif
CC                = gcc -O  $(INC_DIR)

objects           = modules.o seed.o  savepsi.o loop_pos.o init_seed.o \
                    sw_stat.o loop.o time_subs.o getfile.o \
                    vertvel.o coord.o cross.o init_par.o \
                    interp.o interp2.o pos.o \
                    sw_seck.o sw_pres.o sw_dens0.o \
                    writepsi.o writetracer.o turb.o main.o \
		            setupgrid.o readfield.o diffusion.o \
#objwdir = $(patsubst %,tmp/%,$(objects))
#jacket.o

runtracmass : $(objects)
	$(FF)  $(MYI_FLAGS) -o runtracmass $(objects) $(LNK_FLAGS) $(MYL_FLAGS)

%.o : %.f95
	$(FF) $(FF_FLAGS) $(ORM_FLAGS) $(PROJECT_FLAG) $(CASE_FLAG) $(ARG_FLAGS)  $< -o $@

$(objects) : 

#readfield.o:  projects/$(PROJECT)/readfield.f95
#	$(FF) $(FF_FLAGS) $(ORM_FLAGS) projects/$(PROJECT)/readfield.f95 -o tmp/$@

#stat.o:  $(PROJECT)/stat.f95
#	$(FF) $(FF_FLAGS) $(ORM_FLAGS) $(PROJECT)/stat.f95

jacket.o : ../mysql/jacket.c
	$(CC)  -c ../mysql/jacket.c

#main.o : main.f95 
#	$(FF) $(FF_FLAGS) $(ORM_FLAGS) main.f95

.PHONY : clean
clean :
	-rm *.o
	-rm tmp/*.o
	-rm runtracmass  *.mod &> /dev/null



