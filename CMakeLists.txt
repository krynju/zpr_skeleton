cmake_minimum_required(VERSION 2.8.12)
project(python_cpp_example)


find_package(Boost REQUIRED)
find_package(Python REQUIRED)

SET(SOURCE_DIR "src/python_cpp_example")
# Tell cmake that headers are in alse in source_dir
include_directories(${SOURCE_DIR})
SET(SOURCES "${SOURCE_DIR}/math.cpp")

SET(TEST_DIR "tests")
SET(TESTS ${SOURCES}
    "${TEST_DIR}/test_main.cpp"
    "${TEST_DIR}/test_math.cpp")

message(STATUS "PYTHON_LIBRARIES = ${PYTHON_LIBRARIES}")
message(STATUS "PYTHON_EXECUTABLE = ${PYTHON_EXECUTABLE}")
message(STATUS "PYTHON_INCLUDE_DIRS = ${PYTHON_INCLUDE_DIRS}")
message(STATUS "Boost_LIBRARIES = ${Boost_LIBRARIES}")

# Generate a test executable
include_directories(lib/catch/include)
add_executable("${PROJECT_NAME}_test" ${TESTS})
include_directories(${Boost_INCLUDE_DIRS} ${PYTHON_INCLUDE_DIRS})
link_libraries(${Boost_LIBRARIES} ${PYTHON_LIBRARIES})

# Generate python module
add_subdirectory(lib/pybind11)
pybind11_add_module(python_cpp_example ${SOURCES} "${SOURCE_DIR}/bindings.cpp")
