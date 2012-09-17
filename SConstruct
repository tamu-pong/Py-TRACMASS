
env = Environment()
#-DPROJECT_NAME=\'tes\' -DCASE_NAME=\'tes\' -DARG_INT1=intmin             -DARG_INT2=intrun 
env.AppendUnique(PROJECT_NAME='tes',
                 CPPDEFINES=[('PROJECT_NAME', '$PROJECT_NAME'), ('CASE_NAME', '$PROJECT_NAME'), ('ARG_INT1', 'intmin'), ('ARG_INT2', 'intrun'), 
                             'timestep', 'textwrite', 'zvec1D'],
                 F95FLAGS=['$_CPPDEFFLAGS', '-fno-underscoring', '-m64', '-x', 'f95-cpp-input', '-fconvert=big-endian', '-gdwarf-2', '-fbounds-check'])

env.Object('src/modules.f95')


#/sw/bin/gfortran -L/sw/lib -L/sw/opt/netcdf7/lib -I/sw/include -I/sw/opt/netcdf7/include -I/usr/local/mysql/include -fno-underscoring   -Dtes -Dtimestep       -Dtextwrite       -Dzvec1D            -m64 -c -x f95-cpp-input -fconvert=big-endian -gdwarf-2 -fbounds-check -Dtes -Dtimestep       -Dtextwrite       -Dzvec1D            -DPROJECT_NAME=\'tes\' -DCASE_NAME=\'tes\' -DARG_INT1=intmin             -DARG_INT2=intrun              src/modules.f95 -o modules.o
