#pragma once

#include <cmath>
#include <fstream>
#include <ios>
#include <iostream>
#include <nlohmann/json.hpp>
#include <ostream>
#include <string>

using json = nlohmann::json;

namespace JsonUtils {
	static json load_json(std::string path) {
		json j;

		std::ifstream file(path);
		if (!file.is_open()) {
			std::cerr << "Failed to open file!" << std::endl;
			file.close();

			return nullptr;
		}

		try {
			j = json::parse(file);
		} catch (const std::exception& e) {
			std::cerr << "Failed to parse JSON: " << e.what() << std::endl;
			file.close();

			return nullptr;
		}

		file.close();

		return j;
	}

	static void save_json(std::string path, json data) {
		std::ofstream file(path, std::ios::out | std::ios::trunc);
		if (!file.is_open()) {
			std::cerr << "Failed to open file! Creating it" << std::endl;
			file.close();

			return;
		}

		file << data.dump(4).c_str() << std::endl;
		file.close();
	}
}
