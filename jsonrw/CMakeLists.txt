file(GLOB jsonrw_src "src/*" "include/*")
add_library(JsonRW SHARED jsonrw_src)

target_include_directories(JsonRW PUBLIC include/)

target_link_libraries(JsonRW
	log
)
