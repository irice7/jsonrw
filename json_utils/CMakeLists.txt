file(GLOB_RECURSE json_utils_src "include/*" "src/*")
add_library(JsonUtils STATIC json_utils_src)
target_include_directories(JsonUtils PUBLIC include/)

target_link_libraries(JsonUtils NlohmannJson)
