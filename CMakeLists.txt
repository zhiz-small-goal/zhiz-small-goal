cmake_minimum_required(VERSION 3.24)
project(zhiz-small-goal LANGUAGES CXX)

include(FetchContent)

FetchContent_Declare(nlohmann_json
  URL      https://github.com/nlohmann/json/releases/download/v3.12.0/json.tar.xz
  URL_HASH SHA256=42f6e95cad6ec532fd372391373363b62a14af6d771056dbfc86160e6dfff7aa
)
FetchContent_MakeAvailable(nlohmann_json)

add_executable(zhiz_tool app/main.cpp)
target_compile_features(zhiz_tool PRIVATE cxx_std_17)
set_property(TARGET zhiz_tool PROPERTY CXX_EXTENSIONS OFF)

add_library(core_zhiz_log STATIC core/zhiz_log/logger.cpp)
target_compile_features(core_zhiz_log PUBLIC cxx_std_17)
set_property(TARGET core_zhiz_log PROPERTY CXX_EXTENSIONS OFF)

target_include_directories(core_zhiz_log PUBLIC ${CMAKE_CURRENT_SOURCE_DIR})

target_link_libraries(zhiz_tool PRIVATE core_zhiz_log nlohmann_json::nlohmann_json)


target_link_libraries(zhiz_tool PRIVATE nlohmann_json::nlohmann_json)

option(ZHIZ_WARN_AS_ERROR "Treat warnings as errors" OFF)

if(MSVC)
    target_compile_options(zhiz_tool PRIVATE /W4)
    if(ZHIZ_WARN_AS_ERROR)
        target_compile_options(zhiz_tool PRIVATE /WX)
    endif()
endif()