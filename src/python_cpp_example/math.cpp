#include "math.hpp"
#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>

namespace py = pybind11;

int add(int i, int j)
{
    return i + j;
}

int subtract(int i, int j)
{
    return i - j;
}

int getint(py::array_t<int> input){
    py::buffer_info buf1 = input.request();
    int *ptr = (int *) buf1.ptr;
    return ptr[1];
}

int getint_direct(const py::array_t<int>& input) {
    auto r = input.unchecked<1>();
    return r(1);
}
