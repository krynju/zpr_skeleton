#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include <vector>

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

int getint_direct(const py::array_t<int> &input);

py::array_t<int> increment_array(const py::array_t<int> &input);

std::pair<int, int> create_tuple(int x, int y);

std::pair<py::array_t<double>, py::array_t<double>>
generateQQ(py::array_t<double> data1, py::array_t<double> data2, int size);

template<typename T>
py::array_t<double> quantiles(py::array_t<T> input, int count) {
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

std::vector<double> quantiles_vec(std::vector<double> &input, int count);
