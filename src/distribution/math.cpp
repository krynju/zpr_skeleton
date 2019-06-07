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

std::pair<py::array_t<double>, py::array_t<double>> generateQQ(py::array_t<double> data1, py::array_t<double> data2, int size){
    double* begin1 = static_cast<double*>(data1.request().ptr);
    double* begin2 = static_cast<double*>(data2.request().ptr);

    std::sort(begin1 , begin1+data1.shape(0));
    std::sort(begin2 , begin2+data2.shape(0));

    std::vector<double> v1(begin1, begin1+data1.shape(0));
    std::vector<double> v2(begin2, begin2+data2.shape(0));

    std::sort(v1.begin(), v1.end());
    std::sort(v2.begin(), v2.end());

    auto x = py::array_t<double>(size);
    double *ptr_x = (double *)x.request().ptr;

    auto y = py::array_t<double>(size);
    double *ptr_y = (double *)y.request().ptr;

    for (int i=0; i<size; i++){
        ptr_x[i] = v1[v1.size()*i/size];
        ptr_y[i] = v2[v2.size()*i/size];
    }
    return std::pair<py::array_t<double>, py::array_t<double>>(x, y);
}

py::array_t<double> quantiles(py::array_t<double> input, int count) {
    auto q = py::array_t<double>(count);

    long int N = input.size() - 1;
    double p, h;

    auto array = static_cast<double *>(input.request().ptr);
    auto q_ptr = static_cast<double *>(q.request().ptr);

    int f_h = 0;
    for (int i = 0; i < count; ++i) {
        p = 1.0 * i / count;
        h = (N - 1) * p + 1;

        f_h = static_cast<int>(std::floor(h));
        q_ptr[i] = array[f_h] + (h - f_h) * (array[f_h + 1] - array[f_h]);
    }

    return q;
}

// remove this
std::vector<double> quantiles_vec(std::vector<double> &input, int count) {
    auto q = std::vector<double>(count);

    int N = input.size() - 1;
    double p, h;


    int f_h = 0;
    for (int i = 0; i < count; ++i) {
        p = 1.0 * i / count;
        h = (N - 1) * p + 1;
        f_h = static_cast<int>(std::floor(h));
        q[i] = input[f_h] + (h - f_h) * (input[f_h + 1] - input[f_h]);
    }

    return q;
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


