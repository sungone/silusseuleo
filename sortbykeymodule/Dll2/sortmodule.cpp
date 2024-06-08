#include "python.h" 
#include <map>
#include <string>



static PyObject* sort_key(PyObject* self, PyObject* args) {
	PyObject* pyDefaultDict = NULL;
	if (!PyArg_ParseTuple(args, "O", &pyDefaultDict)) {
		return NULL;
	}

	std::map<std::string, PyObject*> sorted_map;
	PyObject* key, * value;
	Py_ssize_t pos = 0;

	while (PyDict_Next(pyDefaultDict, &pos, &key, &value)) {
		PyObject* pyStr = PyObject_Str(key);
		const char* cStr = PyUnicode_AsUTF8(pyStr);
		std::string result(cStr);
		Py_DECREF(pyStr);

		std::string keyStr = result;
		Py_INCREF(value);
		sorted_map[keyStr] = value;
	}

	PyObject* sortedDict = PyDict_New();
	for (const auto& item : sorted_map) {
		PyObject* key = PyUnicode_FromString(item.first.c_str());
		PyObject* value = item.second;
		PyDict_SetItem(sortedDict, key, value);
		Py_DECREF(key);
		Py_DECREF(value);
	}
	return sortedDict;
}

static PyMethodDef SortMethods[] = {
	{ "sort_key", sort_key, METH_VARARGS,
	"count a string length." },
	{ NULL, NULL, 0, NULL } // �迭�� ���� ��Ÿ���ϴ�.
};

static struct PyModuleDef sortmodule = {
	PyModuleDef_HEAD_INIT,
	"sortbykey",            // ��� �̸�
	"It is test module.", // ��� ������ ���� �κ�, ����� __doc__�� ����˴ϴ�.
	-1,SortMethods
};

PyMODINIT_FUNC
PyInit_sortbykey(void)
{
	return PyModule_Create(&sortmodule);
}
