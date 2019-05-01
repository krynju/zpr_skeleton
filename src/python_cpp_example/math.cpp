#include "math.hpp"

#define BOOST_PYTHON_STATIC_LINK
#include <boost/python.hpp>

namespace p = boost::python;
//namespace np = boost::python::numpy;

int add(int i, int j)
{
    return i + j;
}

int subtract(int i, int j)
{
    return i - j;
}

int numpy_check()
{
    return 0;
}
