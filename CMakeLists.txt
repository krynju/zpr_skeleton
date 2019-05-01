cmake_minimum_required(VERSION 3.14.0)
project(python_cpp_example)

# set( CMAKE_VERBOSE_MAKEFILE on )

find_package(Boost REQUIRED COMPONENTS python37 numpy37)
find_package(Python3 3.7 REQUIRED COMPONENTS Interpreter Development)

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

target_link_libraries("${PROJECT_NAME}_test" ${PYTHON_LIBRARIES} ${Boost_LIBRARIES})
link_libraries(Boost::python37 ${PYTHON_LIBRARIES})


# Generate python module
add_subdirectory(lib/pybind11)
pybind11_add_module(python_cpp_example ${SOURCES} "${SOURCE_DIR}/bindings.cpp")
