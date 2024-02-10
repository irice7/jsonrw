#pragma once

#include <nlohmann/json.hpp>
#include "utils.h"

using json = nlohmann::json;

typedef std::unordered_map<std::string, std::any> Dict;
typedef std::vector<std::any> List;

class JsonWrapper;
class DictObj;
class ListObj;

class DictObj {
private:
    json data;
    JsonWrapper* root;

	void auto_save();

public:
    DictObj(json data, JsonWrapper* root) : data(data), root(root) { }

    DictObj new_dict(std::string key);
    ListObj new_list(std::string key);
	template<typename T>
    DictObj put(std::string key, T value);
    std::any get(std::string key) { return data[key]; }

    std::string to_string() { return data.dump(); }

    // Iterator methods
    size_t size() { return data.size(); }
	json::iterator begin() { return data.begin(); }
    json::iterator end() { return data.end(); }

    // Dictionary compatibility methods
    std::any operator[](std::string key);
	// void operator=(std::pair<std::string, std::any> pair);
    void erase(std::string key) { data.erase(key); }
    bool contains(std::string key) { return data.contains(key); }
};

class ListObj {
private:
    json data;
    JsonWrapper* root;
	
public:
    ListObj(json data, JsonWrapper* root) : data(data), root(root) { }

    DictObj new_dict(size_t index = -1);
    ListObj new_list(size_t index = -1);
	template<typename T>
    ListObj put(T value, size_t index = -1);
    std::any get(size_t index);

    std::string to_string() { return data.dump(); }

    // Iterator methods
    size_t size() { return data.size(); }
    json::iterator begin() { return data.begin(); }
    json::iterator end() { return data.end(); }
	
    // List compatibility methods
    std::any operator[](size_t index) { return data[index]; }
    // void operator=(std::any value);
    void erase(size_t index) { data.erase(index); }

	template<typename T>
    bool contains(T value) {
		for (const auto element : data) {
			if (element == value) {
				return true;
			}
		}
		return false;
	}
};

class JsonWrapper {
private:
	json base_json = json();
    std::variant<DictObj, ListObj> root;

	std::function<DictObj(std::string, std::any)> putKV;
	std::function<ListObj(std::any, int)> putI;

	void add_root_methods();

public:
	const std::string path;
    const bool auto_commit;
	
    JsonWrapper(std::string path = "", std::variant<Dict, List> data = { }, bool auto_commit = false): 
		path(path), auto_commit(auto_commit), root(DictObj(base_json, this)) {
		if (path.empty()) {
			if (std::holds_alternative<List>(data)) {
				base_json = json::array();
				root = ListObj(base_json, this);
			}
		} else {
			json tmp = JsonUtils::load_json(path);
			if (tmp != nullptr) {
				base_json = tmp;
			}

			if (base_json.is_object() || std::holds_alternative<Dict>(data)) {
				root = DictObj(base_json, this);
			} else {
				root = ListObj(base_json, this);
			}
		}

		add_root_methods();
	}

	std::variant<DictObj, ListObj> put(std::variant<std::string, std::any> a, std::variant<std::optional<int>, std::any> b);

    void save() { JsonUtils::save_json(path, base_json); }
    std::string to_string() { return base_json.dump(); }

    // Iterator methods
    size_t size();
    std::variant<Dict::iterator, List::iterator> begin();
    std::variant<Dict::iterator, List::iterator> end();

    // List/Dict compatibility methods
    std::variant<DictObj*, ListObj*> operator[](std::string key);
    void operator=(std::pair<std::string, std::any> pair);
    std::any erase(std::string key);
    bool contains(std::string key);
};

