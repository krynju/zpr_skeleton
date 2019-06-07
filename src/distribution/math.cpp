#include "math.hpp"
#include <pybind11/pybind11.h>
#include <cmath>
#include <pybind11/numpy.h>
#include <iostream>
#include <vector>
#include <algorithm>
#include <array>
#include <map>

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
    ptr[0] = 7;
    return ptr[1];
}

int getint_direct(const py::array_t<int>& input) {
    auto r = input.unchecked<1>();
    return r(1);
}

py::array_t<int> increment_array(const py::array_t<int>& input){
    auto r = input.unchecked<1>();
    auto result = py::array_t<int>(r.shape(0));
    py::buffer_info buf_result = result.request();
    int *ptr = (int *)buf_result.ptr;
    for (int i=0; i<input.shape(0); i++){
        ptr[i] = r(i)+1;
    }
    return result;
}

std::pair<int, int> create_tuple(int x, int y){
    return std::pair<int, int>(x, y);
}


std::map<std::string, int> histogram(const py::array &input) {
    std::map<std::string, int> histogram;
    for (int i = 0; i < input.size(); ++i) {
        auto ptr = static_cast<const unsigned int *>(input.data(i));
        std::string temp(ptr, ptr + (input.itemsize() / sizeof(unsigned int)));
        ++histogram[temp];
    }
    return histogram;
}


