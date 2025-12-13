cmake_minimum_required(VERSION 3.20)
project(zhiz_tool LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

add_executable(zhiz_tool app/main.cpp)