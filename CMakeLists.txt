cmake_minimum_required(VERSION 3.10)
project("JsonRW")

set(CMAKE_EXPORT_COMPILE_COMMANDS ON)
set_property(GLOBAL PROPERTY POSITION_INDEPENDENT_CODE ON)

add_subdirectory(deps/nlohmann_json)
add_subdirectory(json_utils)
add_subdirectory(jsonrw)
