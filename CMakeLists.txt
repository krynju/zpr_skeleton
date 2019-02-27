cmake_minimum_required(VERSION 3.10.2)
project(zpr_placeholder)

find_package(Boost REQUIRED)

set(CMAKE_CXX_STANDARD 11)

include_directories(${Boost_INCLUDE_DIRS})
link_libraries(${Boost_LIBRARIES})
add_executable(zpr_placeholder main.cpp)
