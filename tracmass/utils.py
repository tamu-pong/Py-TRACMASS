'''
Created on Sep 21, 2012

@author: sean
'''

import _tracmass as tm
import types

def read_params(yaml_file):
    import yaml
    data = yaml.load(yaml_file)
    
    for mod_name, values in data.items():
        mod = getattr(tm, mod_name)
        for key, value in values.items():
            try:
                setattr(mod, key.lower(), value)
            except AttributeError as err:
                print "warning", err.message
                
def print_state():
    for mod in sorted(tm.modules, key=lambda mod: mod.modname):
        print "Module:", mod.modname
        for attr in sorted(dir(mod)):
            if attr == 'modname':
                continue 
            if attr.startswith('_'):
                continue
            print '    +', attr,
            value = getattr(mod, attr)
            import numpy as np
            if isinstance(value, np.ndarray):
                print "array shape", value.shape
            elif isinstance(value, types.MethodType):
                print
            elif isinstance(value, (str, unicode)):
                print repr(value.strip())
            else:
                print value
        print
        