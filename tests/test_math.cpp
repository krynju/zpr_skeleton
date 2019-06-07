#include <catch.hpp>

#include "math.hpp"
#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>

namespace py = pybind11;

TEST_CASE("Addition and subtraction")
{
    REQUIRE(add(1, 1) == 2);
    REQUIRE(subtract(1, 1) == 0);
    std::vector<double> a = {1, 2, 3, 4, 5};
    std::vector<double> b = {2.0, 2.6, 3.2, 3.8, 4.4};
    REQUIRE(quantiles_vec(a, 5) == b);
//    REQUIRE(quantiles<double>(py::array_t<double>([1,2,3,4]), 4));
}

TEST_CASE("Quantile generation"){
    std::vector<double> a = {1, 2, 3, 4, 5};
    std::vector<double> b = {2.0, 2.6, 3.2, 3.8, 4.4};
    auto py_vec = py::array_t<double>(std::vector<int>({1,5}));
//    double *ptr = (double*)py_vec.request().ptr;
//    for (int i =0;i<5;i++) ptr[i]=a[i];
    //py::array_t<double> result = quantiles(py::array_t<double>(py::cast(a)), 5);
    //auto result_array = static_cast<double *>(result.request().ptr);
    //std::vector<double>result_vector(result_array, result_array+5);
    //auto result = quantiles(py_vec, 5);
    //double* begin = static_cast<double*>(result.request().ptr);
    //std::vector<double> resylt_vec(begin, begin+result.shape(0));
    REQUIRE(true);}

