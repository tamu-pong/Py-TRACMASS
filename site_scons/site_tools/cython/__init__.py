import SCons.Action
import SCons.Builder
import SCons.Errors

def generate(env):

    CythonBuilder = SCons.Builder.Builder(action='cython $SOURCE -o $TARGET $_CPPINCFLAGS',
                      src_suffix='.pyx',
                      suffix='.c',
                          )
    
    env.Append(BUILDERS = {'Cython':CythonBuilder})
    
def exists(env):
    return 1
