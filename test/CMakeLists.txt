cmake_minimum_required(VERSION 3.10)
project("JsonRW-Test")

add_executable(JsonRW_Test main.cpp)
target_link_libraries(JsonRW_Test PUBLIC JsonUtils)
