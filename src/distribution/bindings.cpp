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
        Add two numbers
        Some other information about the add function.
    )doc");

    m.def("subtract", &subtract, R"doc(
        Subtract two numbers

        Some other information about the subtract function.
    )doc");

    m.def("getint", &getint);

    m.def("getint_direct", &getint_direct);

    m.def("increment_array", &increment_array);

    m.def("create_tuple", &create_tuple);

    m.def("generateQQ", &generateQQ);

    m.def("quantiles", &quantiles<int>);

    m.def("quantiles", &quantiles<double>);

    m.def("histogram", &histogram);
}