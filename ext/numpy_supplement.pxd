cdef extern from "Python.h":
    cdef struct PyTypeObject:
        pass

from numpy cimport *
cdef extern from "numpy/arrayobject.h":
    cdef PyTypeObject PyArray_Type
    cdef enum flags:
        NPY_CONTIGUOUS
        NPY_FORTRAN
        NPY_C_CONTIGUOUS
        NPY_F_CONTIGUOUS
        NPY_OWNDATA
        NPY_FORCECAST
        NPY_ENSURECOPY
        NPY_ENSUREARRAY
        NPY_ELEMENTSTRIDES
        NPY_ALIGNED
        NPY_NOTSWAPPED
        NPY_WRITEABLE
        NPY_UPDATEIFCOPY
        NPY_ARR_HAS_DESCR
        NPY_BEHAVED
        NPY_BEHAVED_NS
        NPY_CARRAY
        NPY_CARRAY_RO
        NPY_FARRAY
        NPY_FARRAY_RO
        NPY_DEFAULT
        NPY_IN_ARRAY
        NPY_OUT_ARRAY
        NPY_INOUT_ARRAY
        NPY_IN_FARRAY
        NPY_OUT_FARRAY
        NPY_INOUT_FARRAY
        NPY_UPDATE_ALL
    cdef void import_array() 
    cdef object PyArray_New(PyTypeObject* subtype, int nd, npy_intp *dims, int type_num, npy_intp *strides, void *data, int itemsize, int flags, object obj)
    
