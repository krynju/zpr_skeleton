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
