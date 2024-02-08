#pragma once

#include <any>
#include <unordered_map>
class JsonWrapper;

class DictObj {
	private:
		std::unordered_map<std::string, std::any> data;
		JsonWrapper* root;
};
