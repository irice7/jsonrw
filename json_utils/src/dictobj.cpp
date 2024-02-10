#include "JsonUtils/jsonwrapper.h"

DictObj DictObj::new_dict(std::string key) {
	data[key] = json();
	auto_save();
	return DictObj(data[key], root);
}

ListObj DictObj::new_list(std::string key) {
	data[key] = json::array();
	auto_save();
	return ListObj(data[key], root);
}

template<typename T>
DictObj DictObj::put(std::string key, T value) {
	data[key] = value;
	auto_save();
	return *this;
}

void DictObj::auto_save() {
	if (root->auto_commit) {
		root->save();
	}
}
