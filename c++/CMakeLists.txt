cmake_minimum_required(VERSION 3.14)

set(PROJECT MiuBot)

project(${PROJECT})

set(CMAKE_CXX_STANDARD 14)

set(BUILD_CPR_TESTS OFF)
find_package(CURL)
if(CURL_FOUND)
    set(USE_SYSTEM_CURL ON)
endif()

add_subdirectory(cpr)
include_directories(${CPR_INCLUDE_DIRS})

add_executable(${PROJECT} main.cpp)
target_link_libraries(${PROJECT} ${CPR_LIBRARIES})
