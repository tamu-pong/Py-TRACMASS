import distutils.sysconfig
import os
import re
import sys

import SCons.Script

def TOOL_DISTUTILS(env):
    """Add stuff needed to build Python/Pyrex extensions [with MSVC]."""
    (cc, opt, so_ext, LDCXXSHARED, CFLAGS) = distutils.sysconfig.get_config_vars('CC', 'OPT', 'SO', 'LDSHARED', 'CFLAGS')
    
    LDCXXSHARED = LDCXXSHARED.split()
    del LDCXXSHARED[0]
    i =0
    while i < len(LDCXXSHARED):
        if '-arch' == LDCXXSHARED[i]:
            del LDCXXSHARED[i]
            del LDCXXSHARED[i]
        else:
            i+=1
            
    env.AppendUnique(LDMODULEFLAGS=LDCXXSHARED[1:])
#    print 'CFLAGS', CFLAGS
#    ld_shared = print SCons.Script.Split(LDCXXSHARED)
    
    if cc:
        env['CC'] = cc
        
    env.AppendUnique(CPPPATH=[distutils.sysconfig.get_python_inc()])
    env.AppendUnique(LIBPATH=[distutils.sysconfig.PREFIX + "/lib"])
    
    env['SHLIBPREFIX'] = ""   # gets rid of lib prefix
    env['SHLIBSUFFIX'] = so_ext



def generate(env):
    TOOL_DISTUTILS(env)
    
def exists(env):
    return 1
