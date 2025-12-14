cmake_minimum_required(VERSION 3.20)
project(zhiz-small-goal LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
# set(CMAKE_CXX_EXTENSIONS ON)

add_executable(zhiz_tool app/main.cpp)
target_compile_features(zhiz_tool PRIVATE cxx_std_17)

option(ZHIZ_WARN_AS_ERROR "Tread warnings as errors" OFF)

if (MSVC)
    target_compile_options(zhiz_tool PRIVATE /W4)
    if (ZHIZ_WARN_AS_ERROR)
    target_compile_options(zhiz_tool PRIVATE /WX)
    
    endif()
endif()