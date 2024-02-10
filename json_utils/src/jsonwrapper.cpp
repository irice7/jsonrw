#include "JsonUtils/jsonwrapper.h"

#define getRoot(T) std::get<T>(root)
#define isRootADict() std::holds_alternative<DictObj>(root)

void JsonWrapper::add_root_methods() {
	if (isRootADict()) {
		putKV = [this](const std::string key, const std::any value) {
			return getRoot(DictObj).put<decltype(value.type())>(key, std::any_cast<decltype(value.type())>(value));
		};
	 } else {
		 putI = [this](std::any value, int index) {
			 return getRoot(ListObj).put<decltype(value)>(std::any_cast<decltype(value)>(value), index);
		 };
	 }
}

std::variant<DictObj, ListObj> JsonWrapper::put(std::variant<std::string, std::any> a, std::variant<std::optional<int>, std::any> b) {
	if (isRootADict()) {
		return putKV(std::get<std::string>(a), std::get<std::any>(b));
	}

	return putI(std::get<std::any>(a), std::get<std::optional<int>>(b).value_or(-1));
}
