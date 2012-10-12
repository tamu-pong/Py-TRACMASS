#!/usr/bin/env python
'''
Created on Sep 19, 2012

@author: sean
'''
import re
from argparse import ArgumentParser, FileType
from os.path import splitext
from os.path import basename

states = (
   ('directive', 'inclusive'),
)

TYPES = ('integer', 'real', 'character', 'logical')

RESERVED = {
  "module": "MODULE",
  "endmodule": "ENDMODULE",
  "subroutine": "SUBROUTINE",
  "endroutine": "ENDSUBROUTINE",
  "function": "FUNCTION",
  "endfunction": "ENDFUNCTION",
  "end": "END",
  "if": "IF",
  "endif": "ENDIF",
  "return": "RETURN",
  "program": "PROGRAM",
  "contains": "CONTAINS",
  "allocatable": "TYPESPEC",
  "dimension": "TYPESPEC",
  "parameter": "TYPESPEC",
#  "end":"END",
  }

RESERVED_TOKENS = tuple(set(RESERVED.values()))
tokens = RESERVED_TOKENS + (
    'NAME', 'NUMBER', 'NEWLINE',
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'EQUALS', 'OR',
    'GT', 'LT', 'GTE', 'LTE',
    'LPAREN', 'RPAREN', 'COMMENT', 'CCOMMENT', 'COLON', 'DCOLON', 'DIMSHAPE', 'TYPE', 'DIMLEN', 'DIRECTIVE',
    'STRING', 'MACRO_DIRECTIVE', 'NOT', 'AND',
    )

# Tokens

t_GT = r'>'
t_LT = r'<'
t_GTE = r'>='
t_LTE = r'<='
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_EQUALS = r'='
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_directive_OR = r'\|\|'
t_directive_AND = r'\&\&'

t_COLON = r':'
t_DCOLON = r'::'

def t_DIRECTIVE(t):
    r'[ ]*\043.[a-zA-Z_][a-zA-Z0-9_]*'
    t.lexer.begin('directive')
    return t

#def t_STRING(t):
#    r'[\'\"][.*?][\'\"]'
#    return t
    
def t_DIMSHAPE(t):
    r'\(.*?\)'
    m = re.match('.*len=(\d*).*', t.value, flags=re.I)
    if m:
        t.type = 'DIMLEN'
        t.length = m.groups()[0]
    return t

def t_directive_NOT(t):
    r"!"
    return t

def t_comment(t):
    r"[ ]*![^\n]*"
    pass

def t_ccomment(t):
    r"/\*.*?\*/"
    pass

directives = {'defined'}
def t_directive_NAME(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    if t.value.lower() in directives: 
        t.value = t.value.lower()
        t.type = 'MACRO_DIRECTIVE'
    return t

def t_NAME(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    if t.value.lower() in RESERVED: 
        t.value = t.value.lower()
        t.type = RESERVED[t.value]
        
    if t.value.lower() in TYPES:
        t.type = 'TYPE'
    return t

def t_NUMBER(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print("Integer value too large %d", t.value)
        t.value = 0
    return t

# Ignored characters
t_ignore = " \t"

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")
    t.type = 'NEWLINE'
    t.lexer.begin('INITIAL')
    return t
    
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)
    
literals = ",;.&\"\'[]%"

class FortranType(object):
    def __init__(self):
        self.name = None
        self.length = None
        self.ndim = None
        self.size = None
    def __repr__(self):
        self.name
        if self.size:
            name = '%s%i' % (self.name, self.size)
        else:
            name = self.name
        if self.length:
            name += '(len=%s)' % (self.length,)
        if self.ndim:
            name += '(ndim=%s)' % (self.ndim,)
            
        return '%s' % (name)
    
    def copy(self, **args):
        ty = FortranType()
        ty.__dict__ = self.__dict__.copy()
        ty.__dict__.update(args)
        return ty
    
    @property
    def name(self):
        return self._name
    @name.setter
    def name(self, value):
        if value:
            self._name = value.upper()
        else:
            self._name = None
            
    @property
    def ndim(self):
        return self._ndim
    
    @ndim.setter
    def ndim(self, value):
        self._ndim = value
        

def get_type(type_spec_list):
    assert type_spec_list
    
    ty = FortranType()
    specs = split_on_type(type_spec_list, ttype=',')
    namespec = next(specs)
    type_name = namespec.pop(0)
    assert type_name.type == 'TYPE', type_name
    ty.name = type_name.value
    
    if namespec:
        item = namespec.pop(0)
        if item.type == 'TIMES':
            type_size = namespec.pop(0)
            assert type_size.type == 'NUMBER'
            ty.size = int(type_size.value)
        elif item.type == 'DIMLEN':
            ty.length = item.length 
        else:
            assert False, item

    for spec in specs:
        item = spec.pop(0)
        if item.type == 'TYPESPEC':
            if item.value in ['parameter']:
                return
            if item.value in ['allocatable']:
                continue
            elif item.value == 'dimension':
                dims = spec.pop(0)
                assert dims.type == 'DIMSHAPE', dims
                ty.ndim = len(dims.value.split(','))
            else:
                assert False
        
    return ty

def one_line(token_iter):
    for tok in token_iter:
        if tok.type == 'NEWLINE':
            break
        yield tok

def make_namelist(ty, tokens):
    variables = {}
    for variable in split_on_type(tokens, ttype=','):
        tok = variable.pop(0)
        assert tok.type == 'NAME', tok
        
        var_name = tok.value
        variables[var_name.lower()] = ty.copy() 
        ty.var_name = var_name
        if not variable:
            continue
        
        next_tok = variable.pop(0)
        
        if next_tok.type == 'EQUALS':
            continue
        elif next_tok.type == 'DIMSHAPE':
            ty.ndim = len(next_tok.value.split(','))
        else:
            assert False, next_tok
    
    return variables
        
def contains_type(tokens, ttype):
    for token in tokens:
        if token.type == ttype:
            return True
    return False

def split_on_type(tokens, ttype):
    tokens = list(tokens)
    first = []
    while tokens:
        token = tokens.pop(0)
        if token.type == ttype:
            yield first
            first = []
        else:
            first.append(token)
    yield first
        
        
def type_consumer(tokens):
    
    if not contains_type(tokens, "DCOLON"):
        return 
    
    typedec, name_list = split_on_type(tokens, "DCOLON")
    ty = get_type(typedec)
    
    if ty:
        names = make_namelist(ty, name_list)
        return names

def single_block(token_iter, module_name, block_type):
    END = 'END%s' % (block_type)
    for tok in token_iter:
        if tok.type == 'END':
            blocktok = next(token_iter)
            if blocktok.type != block_type:
                yield tok
                yield blocktok
            else:
                nametok = next(token_iter)
                assert nametok.type in ['NAME', 'NEWLINE'], (tok, blocktok, nametok)
                if nametok.type == 'NEWLINE' or nametok.value == module_name:
                    break
                else:
                    yield tok
                    yield blocktok
                    yield nametok
                    
        elif tok.type == END:
            nametok = next(token_iter)
            assert nametok.type in ['NAME', 'NEWLINE'], (tok, blocktok, nametok)
            if nametok.type == 'NEWLINE' or nametok.value == module_name:
                break
            else:
                yield tok
                yield nametok
        else:
            yield tok
    return 
        
def split_lines(token_iterator):
    tokens = []
    for tok in token_iterator:
        if tok.type == 'NEWLINE':
            yield tokens
            tokens = []
        else:
            tokens.append(tok)
        
    if tokens:
        yield tokens
        
    
def module_consumer(token_iter):
    module_name = next(token_iter)
    
    
    module_variables = {}
    
    subroutines = []
    new_iter = single_block(token_iter, module_name.value, 'MODULE')
    
    for line in split_lines(new_iter):
        if contains_type(line, 'CONTAINS'):
            for tok in new_iter:
                if tok.type == 'SUBROUTINE':
                    name_args = subroutine_consumer(new_iter)
                    subroutines.append(name_args)
        
        vars = type_consumer(line)
        if vars:
            module_variables.update(vars)
                 
    return module_name.value, module_variables, subroutines
        
def get_line(lexer):
    line = []
    while True:
        tok = lexer.token()
        if tok.type == 'NEWLINE':
            break
        line.append(tok)
    return line

class PreProcessor():
    def __init__(self, lexer, defines):
        self.lexer = lexer
        self.defines = {}
        for define in defines:
            if '=' in define:
                key, value = define.split('=') 
                self.defines[key] = value
            else:
                self.defines[define] = True
                
        self.ifdef_stack = [True]
        

    def pre(self, line):
        value = True
        while line:
            tok = line.pop(0)
            if tok.type == 'MACRO_DIRECTIVE':
                next_symbol = line.pop(0)
                assert next_symbol.type == 'NAME', next_symbol
                if tok.value == 'not_defined':
                    value = (tok.value not in self.defines)
                elif tok.value == 'defined':
                    value = (tok.value in self.defines)
                else :  
                    assert False, tok
            elif tok.type == 'NAME':
                value = tok.value in self.defines
            elif tok.type == 'OR':
                value = value or self.pre(line)
            elif tok.type == 'AND':
                value = value and self.pre(line)
            elif tok.type == 'NOT':
                mac = line.pop(0)
                sym = line.pop(0)
                assert mac.type == 'MACRO_DIRECTIVE'
                assert sym.type == 'NAME'
                value = (tok.value not in self.defines)
            else:
                assert  False, tok
                
        return value
            
            
            
    
    
    def tokens(self):
        
        tok = True
        while tok:
            tok = self.lexer.token()
            if tok is None:
                break
            
            if tok.type == '&':
                tok = self.lexer.token()
                assert tok.type == 'NEWLINE', tok
                tok = self.lexer.token()
                if tok.type == '&':
                    tok = self.lexer.token()
                
            if tok.type == 'DIRECTIVE':
                line = get_line(self.lexer)
                
                if tok.value == '#ifdef':
                    tok.value = '#if'
                    new_tok = lex.LexToken()
                    new_tok.type = 'MACRO_DIRECTIVE'
                    new_tok.value = 'defined'
                    new_tok.lineno = 0
                    new_tok.lexpos = 0
                    line.insert(0, new_tok)
                elif tok.value == '#ifndef':
                    new_tok = lex.LexToken()
                    new_tok.type = 'MACRO_DIRECTIVE'
                    new_tok.value = 'not_defined'
                    new_tok.lineno = 0
                    new_tok.lexpos = 0
                    line.insert(0, new_tok)
                    tok.value = '#if'
                    
#                 
                if tok.value == '#if':
                    self.ifdef_stack.append(self.pre(line))
                elif tok.value == '#elif':
                    self.ifdef_stack.pop()
                    self.ifdef_stack.append(self.pre(line))
                elif tok.value == '#endif':
                    self.ifdef_stack.pop()
                elif tok.value == '#else':
                    value = self.ifdef_stack.pop()
                    self.ifdef_stack.append(not value)
                else:
                    raise NotImplementedError(tok)
                continue
                
            if all(self.ifdef_stack):
                if tok.type == 'NAME' and tok.value in self.defines:
                    print "waring define substitution ignored", tok 
                yield tok
            
    
def subroutine_consumer(token_iter):
    scons = list(one_line(token_iter))
    if len(scons) == 1:
        name = scons[0]
        subroutine_args = []
    else:
        name, args = scons    
        subroutine_args = [arg.strip() for arg in args.value[1:-1].split(',') if arg.strip()]
    subroutine_name = name.value
    
    module_variables = {}
    new_iter = single_block(token_iter, subroutine_name, 'SUBROUTINE')
    for line in split_lines(new_iter):
        vars = type_consumer(line)
        if vars: module_variables.update(vars)
            
    args = []
    for name in subroutine_args:
        if name not in module_variables:
            print "warning %s is declared (subroutine %s)" % (name, subroutine_name) 
        args.append((name, module_variables.get(name, None)))
        
    return subroutine_name, args

def function_consumer(token_iter):
    scons = list(one_line(token_iter))
    if len(scons) == 1:
        name = scons[0]
        subroutine_args = []
    else:
        name, args = scons    
        subroutine_args = [arg.strip() for arg in args.value[1:-1].split(',') if arg.strip()]
    subroutine_name = name.value
    
    module_variables = {}
    new_iter = single_block(token_iter, subroutine_name, 'FUNCTION')
    for line in split_lines(new_iter):
        vars = type_consumer(line)
        if vars: module_variables.update(vars)
            
    args = []
    for name in subroutine_args:
        args.append((name, module_variables[name.lower()]))
        
    return subroutine_name, args

def consume(preprocessor):
    modules = []
    subroutines = []
    
    for tok in preprocessor:
        if tok.type == 'MODULE':
            modname_vars_subroutines = module_consumer(preprocessor)
            modules.append(modname_vars_subroutines)
        elif tok.type == 'SUBROUTINE':
            name_args = subroutine_consumer(preprocessor)
            subroutines.append(name_args)
        elif tok.type == 'FUNCTION':
            name_args = function_consumer(preprocessor)
            subroutines.append(name_args)
        elif tok.type == 'NEWLINE':
            continue
        else:
            assert False, tok
    return modules, subroutines

import ply.lex as lex

def write_mod_header_ty(header, mod, var, ty):
    header.write('\n\n // variable %s \n' % var)
    header.write('#define fw_get_%(mod)s_%(var)s_loc FORTRAN_MANGLE(get_%(mod)s_%(var)s_loc)\n' % dict(mod=mod[0], var=var))
    header.write('void fw_get_%(mod)s_%(var)s_loc(size_t *location);\n' % dict(mod=mod[0], var=var))

    if ty.ndim:
        header.write('#define fw_get_%(mod)s_%(var)s_shape FORTRAN_MANGLE(get_%(mod)s_%(var)s_shape)\n' % dict(mod=mod[0], var=var))
        header.write('void fw_get_%(mod)s_%(var)s_shape(int *shape);\n' % dict(mod=mod[0], var=var))
    
def write_mod_pxd_ty(header, mod, var, ty):
    header.write('    void fw_get_%(mod)s_%(var)s_loc(size_t *location)\n' % dict(mod=mod[0], var=var))
    if ty.ndim:
        header.write('    void fw_get_%(mod)s_%(var)s_shape(int *shape)\n' % dict(mod=mod[0], var=var))
    
def write_mod_pyx_ty(pyx, mod, var, ty):
    ctx = dict(mod=mod[0], var=var, ctype=TY_LOOKUP[ty.name, ty.size])
    if ty.name == 'LOGICAL':
        return
    if ty.ndim:
        ctx['ndim'] = ty.ndim
        pyx.write('    def _get_%(var)s(self):\n' % ctx)
        pyx.write('        cdef %(ctype)s *loc\n' % ctx)
        pyx.write('        helper.fw_get_%(mod)s_%(var)s_loc(<size_t*>&loc)\n' % ctx)

        pyx.write('        if loc == NULL: return None\n' % ctx)
        pyx.write('        cdef int _shape[%(ndim)i]\n' % ctx)
        pyx.write('        cdef numpy.npy_intp dims[%(ndim)i]\n' % ctx)
        pyx.write('        helper.fw_get_%(mod)s_%(var)s_shape(_shape)\n' % ctx)
        for i in range(ty.ndim):
            ctx['i'] = i
            pyx.write('        dims[%(i)i] = _shape[%(i)i]\n' % ctx)
            pyx.write('        if _shape[%(i)i] == 0: return None\n' % ctx)
            
        npy_type_enum = {('INTEGER', None):'numpy.NPY_INT', 
                         ('REAL', None):'numpy.NPY_FLOAT',
                         ('REAL', 4):'numpy.NPY_FLOAT',
                         ('REAL', 8):'numpy.NPY_DOUBLE',
                         }
        ctx['npy_type_enum'] = npy_type_enum[(ty.name, ty.size)]
        
        pyx.write('        return helper.PyArray_New(&helper.PyArray_Type, %(ndim)i, dims, %(npy_type_enum)s, NULL, <void*>loc, 0, numpy.NPY_FARRAY, None)\n' % ctx)

        pyx.write('    %(var)s = property(_get_%(var)s)\n\n' % ctx)
    elif ty.length:
        ctx['length'] = int(ty.length)
        pyx.write('    def _get_%(var)s(self):\n' % ctx)
        pyx.write('        cdef %(ctype)s *loc\n' % ctx)
        pyx.write('        helper.fw_get_%(mod)s_%(var)s_loc(<size_t*>&loc)\n' % ctx)
        
        pyx.write('        return loc[:helper.strnlen(loc, %(length)i)].decode()\n' % ctx)
            
        pyx.write('    def _set_%(var)s(self, value):\n' % ctx)
        pyx.write('        cdef %(ctype)s *loc\n' % ctx)
        pyx.write('        helper.fw_get_%(mod)s_%(var)s_loc(<size_t*>&loc)\n' % ctx)
        #pyx.write('        loc[:%(length)i] = value[:%(length)i]\n' % ctx)
        pyx.write('        val = value[:%(length)i].encode()\n' % ctx)
        pyx.write('        for i,c in enumerate(val):\n' % ctx)
        pyx.write('            loc[i] = ord(c)\n' % ctx)
        
        pyx.write('    %(var)s = property(_get_%(var)s, _set_%(var)s)\n\n' % ctx)
    else:
        ctx['ctype'] = TY_LOOKUP[ty.name, ty.size]
        pyx.write('    def _get_%(var)s(self):\n' % ctx)
        pyx.write('        cdef %(ctype)s *loc\n' % ctx)
        pyx.write('        helper.fw_get_%(mod)s_%(var)s_loc(<size_t*>&loc)\n' % ctx)
        pyx.write('        return loc[0]\n' % ctx)
        
            
        pyx.write('    def _set_%(var)s(self, value):\n' % ctx)
        pyx.write('        cdef %(ctype)s *loc\n' % ctx)
        pyx.write('        helper.fw_get_%(mod)s_%(var)s_loc(<size_t*>&loc)\n' % ctx)
        pyx.write('        loc[0] = value\n' % ctx)
        pyx.write('    %(var)s = property(_get_%(var)s, _set_%(var)s)\n\n' % ctx)
    
TY_LOOKUP = {('REAL', None):'float',
             ('REAL', 4):'float',
             ('REAL', 8):'double',
             ('INTEGER', None): 'int',
             ('INTEGER', 8): 'long long',
             ('CHARACTER', None): 'char',
             ('LOGICAL', None):'int'}

def get_ctype(argname, argty):
    if argty is None:
        raise NotImplementedError(argname, argty)
    if argty.ndim:
        raise NotImplementedError(argname, argty)
    yield '%s *%s' % (TY_LOOKUP[argty.name, argty.size], argname)
    
def write_pxd_sub(header, mod, sub):
    args = []
    for argname, argty in sub[1]:
        for argstr in get_ctype(argname, argty):
            args.append(argstr)
    ctx = dict(sub=sub[0], args=', '.join(args))
    if mod:
        ctx['mod'] = mod[0]
        header.write('    void fw_%(mod)s_%(sub)s(%(args)s) nogil\n' % ctx)
    else:
        header.write('    void fw_%(sub)s(%(args)s) nogil\n' % ctx)

def write_pyx_sub(pyx, mod, sub):
    ctx = dict(sub=sub[0], indent='')
    if mod:
        ctx['mod'] = mod[0]
        ctx['indent'] = '    '
    
    py_arg_names = [argname for argname, argty in sub[1]]
    if mod:
        py_arg_names.insert(0, 'self')
    ctx['py_argnames'] = ', '.join(py_arg_names)
    
    pyx.write('%(indent)sdef %(sub)s(%(py_argnames)s):\n' % ctx)
    
    call_args = []
    args = []
    for argname, argty in sub[1]:
        call_argname = '_c_' + argname
        ctype = TY_LOOKUP[argty.name, argty.size]
        ctx['ctype'] = ctype
        ctx['call_argname'] = call_argname
        ctx['argname'] = argname
        
        if argty.length or argty.ndim:
            raise NotImplementedError()
        else:
            pyx.write('%(indent)s    cdef %(ctype)s %(call_argname)s = %(argname)s\n' % ctx)
            call_args.append('&(%(call_argname)s)' % ctx)
    
    ctx['call_args'] = ', '.join(call_args)
    if mod:
        pyx.write('%(indent)s    helper.fw_%(mod)s_%(sub)s(%(call_args)s)\n' % ctx)
    else:
        pyx.write('%(indent)s    helper.fw_%(sub)s(%(call_args)s)\n' % ctx)


def write_mod_header_sub(header, mod, sub):
    header.write('\n\n // subroutine %s \n' % sub[0])
    args = []
    for argname, argty in sub[1]:
        for argstr in get_ctype(argname, argty):
            args.append(argstr)
    if not args:
        args.append('void')
    header.write('#define fw_%(mod)s_%(sub)s FORTRAN_MANGLE_MOD(%(mod)s, %(sub_lower)s)\n' % dict(mod=mod[0], sub=sub[0], sub_lower=sub[0].lower()))
    header.write('void fw_%(mod)s_%(sub)s(%(args)s);\n' % dict(mod=mod[0], sub=sub[0], args=', '.join(args)))
    
def write_header_sub(header, sub):
    header.write('\n\n // subroutine %s \n' % sub[0])
    args = []
    ctx = dict(sub=sub[0])
    for argname, argty in sub[1]:
        for argstr in get_ctype(argname, argty):
            args.append(argstr)
    if not args:
        args.append('void')
    header.write('#define fw_%(sub)s FORTRAN_MANGLE(%(sub)s)\n' % ctx)
    ctx['args'] = ', '.join(args)
    header.write('void fw_%(sub)s(%(args)s);\n' % ctx)
    

def write_helper(helper, mod, var, ty, pointer_size):
    helper.write('\n\n ! variable %s \n' % var)
    helper.write('SUBROUTINE get_%s_%s_loc(location)\n' % (mod[0], var))
    helper.write('    USE %s\n' % mod[0])
    helper.write('    INTEGER*%i, INTENT(OUT) :: location\n' % pointer_size)
    helper.write('    location = LOC(%s)\n' % var)
    helper.write('END SUBROUTINE get_%s_%s_loc\n' % (mod[0], var))
    if ty.ndim:
        helper.write('SUBROUTINE get_%s_%s_shape(var_shape)\n' % (mod[0], var))
        helper.write('    USE %s\n' % mod[0])
        helper.write('    INTEGER, INTENT(OUT) :: var_shape(%i)\n' % ty.ndim)
        helper.write('    var_shape = SHAPE(%s)\n' % var)
        helper.write('END SUBROUTINE get_%s_%s_shape\n\n' % (mod[0], var))
        

    
def main():
    lexer = lex.lex()
    parser = ArgumentParser()
    parser.add_argument('inputs', nargs='+',)
    parser.add_argument('-D', '--define', action='append')
    parser.add_argument('-f', '--fortran-helper', type=FileType('w'), required=True)
    parser.add_argument('-c', '--c-header', type=FileType('w'), required=True)
    parser.add_argument('--pxd', type=FileType('w'), required=True)
    parser.add_argument('--pyx', type=FileType('w'), required=True)
    parser.add_argument('--pyx-tail', type=FileType('r'))
    parser.add_argument('--ignore-module', action='append', default=[])
    parser.add_argument('--ignore-mod-subroutine', nargs=2, action='append', default=[])
    parser.add_argument('--ignore-mod-var', nargs=2, action='append', default=[])
    parser.add_argument('--ignore-subroutine', action='append', default=[])
    parser.add_argument('--pointer-size', type=int, default=8)
    
    args = parser.parse_args()
    
    all_modules = []
    all_subroutines = []
    for inpt in args.inputs:
        lexer.lineno = 1
        lexer.input(open(inpt).read())
        preprocessor = PreProcessor(lexer, args.define or [])
        print "inpt", inpt
        modules, subroutines = consume(preprocessor.tokens())
        
        all_modules.extend(modules)
        all_subroutines.extend(subroutines)
        
    helper = args.fortran_helper
    header = args.c_header
    pxd = args.pxd
    pyx = args.pyx
    
    pxd.write('cimport numpy\n')
    pxd.write('cdef extern from "string.h":\n')
    pxd.write('    size_t strnlen(char *, size_t)\n\n')
    pxd.write('cdef extern from "Python.h":\n')
    pxd.write('    cdef struct PyTypeObject:\n')
    pxd.write('        pass\n')
    pxd.write('cdef extern from "numpy/arrayobject.h":\n')
    pxd.write('    cdef PyTypeObject PyArray_Type\n')
    pxd.write('    cdef object PyArray_New(PyTypeObject* subtype, int nd, numpy.npy_intp *dims, int type_num, numpy.npy_intp *strides, void *data, int itemsize, int flags, object obj)\n\n')
    
    pxd.write('cdef extern from "%s":\n' % basename(header.name))
    pyx.write('cimport numpy\n')
    pyx.write('import numpy\n')
    pyx.write('cimport %s as helper\n\n' % basename(splitext(pxd.name)[0]))
    pyx.write('modules = []\n\n' )
    
    header.write('#include "fortran_defines.h"\n\n')

    for mod in all_modules:
        if mod[0] in args.ignore_module:
            print "Ignoring module", mod[0]
            continue
            
        helper.write('! Wrapper helper for module %s \n' % mod[0])
        
        pyx.write('class _%s_(object):\n\n' % (mod[0].upper()))
#        pyx.write('    def __setattr__(self, attr, value):\n        raise AttributeError("fortran module %s has no attribute %%r" %% (attr,))\n\n' % (mod[0].lower(),))
        pyx.write('    modname = "%s"\n\n' %(mod[0].lower(),))
        
        pyx.write('    __slots__ = ()\n\n')
        
        for var, ty in mod[1].items():
            write_helper(helper, mod, var, ty, args.pointer_size)
            write_mod_header_ty(header, mod, var, ty)
            write_mod_pxd_ty(pxd, mod, var, ty)
            write_mod_pyx_ty(pyx, mod, var, ty)
            
                
        for sub in mod[2]:
            try:
                write_mod_header_sub(header, mod, sub)
                write_pxd_sub(pxd, mod, sub)
                write_pyx_sub(pyx, mod, sub)
            except NotImplementedError as err:
                print "not writing module subroutine", mod[0], sub[0]
                

        if not mod[1] or mod[2]:
            pyx.write('    pass\n\n')
        pyx.write('\n')
        pyx.write('%s = _%s_()\n\n' % (mod[0].lower(), mod[0].upper()))
        pyx.write('modules.append(%s)\n\n' % (mod[0].lower(),))
        
    for sub in all_subroutines:
        try:
            write_header_sub(header, sub)
            write_pxd_sub(pxd, None, sub)
            write_pyx_sub(pyx, None, sub)
        except NotImplementedError as err:
            print "not writing subroutine", sub[0]
    
    if args.pyx_tail:
        pyx.write('#Tail\n')
        pyx.write(args.pyx_tail.read())
    
    pyx.write('numpy.import_array()\n')
    
if __name__ == '__main__':
    main()
