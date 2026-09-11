#include "parts.h"


static PyObject *
get_debug_metadata(PyObject *module, PyObject *name_obj)
{
    const char *name;
    if (!PyArg_Parse(name_obj, "s", &name)) {
        return NULL;
    }

    size_t size;
    const void *data;
    Py_BEGIN_ALLOW_THREADS
    data = PyUnstable_Debug_GetMetadata(name, &size);
    Py_END_ALLOW_THREADS
    if (data == NULL) {
        Py_RETURN_NONE;
    }

    PyObject *address_obj = PyLong_FromVoidPtr((void *)data);
    if (address_obj == NULL) {
        return NULL;
    }
    PyObject *size_obj = PyLong_FromSize_t(size);
    if (size_obj == NULL) {
        Py_DECREF(address_obj);
        return NULL;
    }
    Py_ssize_t prefix_size = size < 8 ? (Py_ssize_t)size : 8;
    PyObject *prefix = PyBytes_FromStringAndSize(data, prefix_size);
    if (prefix == NULL) {
        Py_DECREF(address_obj);
        Py_DECREF(size_obj);
        return NULL;
    }
    PyObject *result = PyTuple_Pack(3, address_obj, size_obj, prefix);
    Py_DECREF(address_obj);
    Py_DECREF(size_obj);
    Py_DECREF(prefix);
    return result;
}


static PyMethodDef test_methods[] = {
    {"get_debug_metadata", get_debug_metadata, METH_O},
    {NULL},
};


int
_PyTestCapi_Init_Debug(PyObject *module)
{
    return PyModule_AddFunctions(module, test_methods);
}
