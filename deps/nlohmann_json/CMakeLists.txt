cmake_minimum_required(VERSION 3.10)

add_library(NlohmannJson include/NlohmannJson/json.hpp)

target_include_directories(NlohmannJson PUBLIC include/)
