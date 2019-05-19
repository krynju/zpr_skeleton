cmake_minimum_required(VERSION 3.13.0)
project(python_cpp_example)

find_package(Python3 3.7 REQUIRED COMPONENTS Interpreter Development)
add_subdirectory(lib/pybind11)


SET(SOURCE_DIR "src/python_cpp_example")
# Tell cmake that headers are in else in source_dir
include_directories(${SOURCE_DIR})
SET(SOURCES "${SOURCE_DIR}/math.cpp")

SET(TEST_DIR "tests")
SET(TESTS ${SOURCES}
    "${TEST_DIR}/test_main.cpp"
    "${TEST_DIR}/test_math.cpp")



# Generate a test executable
include_directories(lib/catch/include)

include_directories(${Boost_INCLUDE_DIRS} ${PYTHON_INCLUDE_DIRS})
add_executable("${PROJECT_NAME}_test" ${TESTS})

target_link_libraries("${PROJECT_NAME}_test" Python3::Python pybind11::module)


# Generate python module
pybind11_add_module(python_cpp_example ${SOURCES} "${SOURCE_DIR}/bindings.cpp" )
target_link_libraries(python_cpp_example PRIVATE Python3::Python)