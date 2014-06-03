#include <Python.h>
#include <numpy/arrayobject.h>


#define ScrPrt(_str) {\
	PyObject *_sys = PyImport_ImportModule("sys");\
	PyObject *_s_out = PyObject_GetAttrString(_sys, "stdout"); \
	PyObject *_result = PyObject_CallMethod(_s_out, "write", "s", _str); \
	Py_DECREF(_result);\
	Py_DECREF(_s_out);\
	Py_DECREF(_sys);}

#define ScrPrtRefCount(pObj) {\
	char buffer[50];\
	sprintf(buffer,"\nref count: %d\n",(*pObj).ob_refcnt);\
	ScrPrt(buffer);}

int cpivoting(double *A, int nrow_A, int ncol_A, double *B, int nrow_B, int ncol_B, int csz);

static PyObject *
pivoting(PyObject *self, PyObject *args)
{
	int csz;
	PyObject *a0 = NULL, *b0 = NULL, *a = NULL, *b = NULL;
	if (!PyArg_ParseTuple(args, "OOi", &a0, &b0, &csz))
		return NULL;
	
	a = PyArray_FROM_OTF(a0,NPY_DOUBLE,NPY_INOUT_ARRAY);	
	b = PyArray_FROM_OTF(b0,NPY_DOUBLE,NPY_INOUT_ARRAY);	
	
	// Check the validity of input values:
	int ndim_a = PyArray_NDIM(a), ndim_b = PyArray_NDIM(b);
	npy_intp *dims_a = PyArray_DIMS(a), *dims_b = PyArray_DIMS(b);
	int nrow_a = dims_a[0], ncol_a = dims_a[1], nrow_b = dims_b[0], ncol_b = 1;
	
#ifdef CHK_INPUTS
	if (a == NULL || b == NULL) return NULL;	
	if (ndim_a != 2){
		PyErr_SetString(PyExc_ValueError,"The dimension of a should be 2.");
		return NULL;
	}	
	if (ndim_b != 1){
		PyErr_SetString(PyExc_ValueError,"The dimension of b should be 1.");
		return NULL;
	}	
	if (nrow_a != nrow_b){
		PyErr_SetString(PyExc_ValueError,"a and b should have the same rows");
		return NULL;
	}
#endif

	double *A = (double *)PyArray_DATA(a);
	double *B = (double *)PyArray_DATA(b);
	
	cpivoting(A, nrow_a, ncol_a, B, nrow_b, ncol_b, csz);	

	Py_DECREF(a);
	Py_DECREF(b);
	Py_INCREF(Py_None);
	return Py_None;
}

static PyMethodDef Methods[] = {
     {"pivoting", pivoting, METH_VARARGS,
     	"changes matrix A by pivoting"}
};

PyMODINIT_FUNC
initcgauss(void)
{
    (void) Py_InitModule("cgauss", Methods);
    import_array();
}
