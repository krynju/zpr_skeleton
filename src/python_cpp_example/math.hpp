#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>

namespace py = pybind11;


/*! Add two integers
    \param i an integer
    \param j another integer
*/
int add(int i, int j);

/*! Subtract one integer from another
    \param i an integer
    \param j an integer to subtract from \p i
*/
int subtract(int i, int j);

int getint(py::array_t<int> input);

int getint_direct(const py::array_t<int>& input);
