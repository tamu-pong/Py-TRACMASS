
#===============================================================================
# 
#===============================================================================
CPPDEFINES = [('PROJECT_NAME', '\\\'$PROJECT_NAME\\\''), ('CASE_NAME', '\\\'$PROJECT_NAME\\\''), ('ARG_INT1', 'intmin'), ('ARG_INT2', 'intrun'),
               'timestep', 'textwrite', 'zvec1D', '$PROJECT_NAME']

F95FLAGS = ['$_CPPDEFFLAGS', '-fno-underscoring', '-x', 'f95-cpp-input', '-fconvert=big-endian', '-gdwarf-2', '-fbounds-check']

#===============================================================================
# 
#===============================================================================
env = Environment(tools=['default', 'distutils', 'cython'])
py_tracmass = env.Cython('ext/tracmass.pyx')

params_obj = env.SharedObject(py_tracmass)


#===============================================================================
# 
#===============================================================================
fortran_env = Environment()

fortran_env.AppendUnique(PROJECT_NAME='tes', CPPDEFINES=CPPDEFINES, F95FLAGS=F95FLAGS)

ftracmass_helper = fortran_env.SharedObject('ext/ftracmass.f95')
tes_readfield = fortran_env.SharedObject('projects/tes/tes_readfield.f95')

objects_modules = fortran_env.SharedObject(Glob('src/*.f95'))
fortran_env.Depends('src/loop.os', ['mod_pos.mod'])

objects = [obj for obj in objects_modules if obj.suffix == '.os']
modules = [obj for obj in objects_modules if obj.suffix == '.mod']

#===============================================================================
# 
#===============================================================================
env.SharedLibrary('tracmass', [params_obj, ftracmass_helper, objects, tes_readfield])


env.Program('cmain', ['test.f95','cmain.c'])


