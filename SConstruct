import os

#===============================================================================
# 
#===============================================================================
CPPDEFINES = [('PROJECT_NAME', '\\\'$PROJECT_NAME\\\''), ('CASE_NAME', '\\\'$PROJECT_NAME\\\''), ('ARG_INT1', 'intmin'), ('ARG_INT2', 'intrun'),
               'timestep', 'textwrite', 'zvec1D', '$PROJECT_NAME']

F95FLAGS = ['$_CPPDEFFLAGS', '-fno-underscoring', '-x', 'f95-cpp-input', '-fconvert=big-endian', '-gdwarf-2', '-fbounds-check', '-O0', '-g3']

#===============================================================================
# 
#===============================================================================
import numpy
CPPPATH = [numpy.get_include()] 
env = Environment(tools=['default', 'distutils', 'cython'])
env.AppendUnique(CPPPATH=CPPPATH, CFLAGS=['-O0', '-g3'])
py_tracmass = env.Cython('ext/tracmass.pyx')

#params_obj = env.SharedObject(py_tracmass)


#===============================================================================
# 
#===============================================================================
fortran_env = Environment(ENV= {'PATH':os.environ['PATH']})
fortran_env.AppendUnique(PROJECT_NAME='tes', CPPDEFINES=CPPDEFINES, F95FLAGS=F95FLAGS)
f95_src = Glob('src/*.f95')

fortran_env.Command(['fhelper.f95', 'cheader.h', 'helper.pxd', 'tracmass.pyx'], ['simple_wrap.py', 'pyx_tail.pyx', f95_src],
                    './$SOURCE ${SOURCES[2:]} -f ${TARGETS[0]} -c ${TARGETS[1]} --pxd ${TARGETS[2]} --pyx ${TARGETS[3]} --pyx-tail  ${SOURCES[1]}  ${_CPPDEFFLAGS} --ignore-module mod_stat')

pyx_helper = env.Cython('tracmass.pyx')
Depends(pyx_helper, ['helper.pxd'])

pyx_helper_c = env.SharedObject(pyx_helper)
f_helper = fortran_env.SharedObject('fhelper.f95')
f_tm = fortran_env.SharedObject('ext/ftracmass.f95')


#ftracmass_helper = fortran_env.SharedObject('ext/ftracmass.f95')
tes_readfield = fortran_env.SharedObject('projects/tes/tes_readfield.f95')


objects_modules = fortran_env.SharedObject(f95_src)
fortran_env.Depends('src/loop.os', ['mod_pos.mod'])
fortran_env.Depends('src/loop_pos.os', ['mod_psi.mod'])
#fortran_env.Depends(ftracmass_helper, ['mod_time.mod'])

objects = [obj for obj in objects_modules if obj.suffix == '.os']
modules = [obj for obj in objects_modules if obj.suffix == '.mod']

#===============================================================================
# 
#===============================================================================
env.SharedLibrary('tracmass', [f_helper, objects, tes_readfield, pyx_helper_c, f_tm])


#env.Program('cmain', ['test.f95','cmain.c'])


