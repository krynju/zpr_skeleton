#include <pybind11/pybind11.h>
#include "math.hpp"

namespace py = pybind11;

py::module m("distribution", R"doc(
	Python module
	-----------------------
	.. currentmodule:: distribution
	.. autosummary::
	   :toctree: _generate
	   
	   add
	   subtract
)doc");

PYBIND11_MODULE(distribution, m) {
    m.def("add", &add, R"doc(
        Add two numbers. Function used for testing python/c++ integration.
    )doc");

    m.def("subtract", &subtract, R"doc(
        Subtract two numbers. Function used for testing python/c++ integration.
    )doc");

    m.def("getint", &getint);

    m.def("getint_direct", &getint_direct, R"doc(
        returns the 2nd element of an array. Function used for testing python/c++ integration.
    )doc");

    m.def("increment_array", &increment_array, R"doc(
        Adds 1 to every element of an array. Function used for testing python/c++ integration.
    )doc");

    m.def("create_tuple", &create_tuple);

    m.def("quantiles", &quantiles<int>, R"doc(
        Sorts the array of doubles given as arg0 and returns arg1 quantiles
    )doc");

    m.def("quantiles", &quantiles<double>, R"doc(
        Sorts the array of ints given as arg0 and returns arg1 quantiles
    )doc");

    m.def("histogram", &histogram, R"doc(
        Counts the number of unique elements given in array arg0 and returns the total number of occurence of each unique element
    )doc");
}