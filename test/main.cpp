#include <JsonUtils/jsonwrapper.h>

int main() {
	JsonWrapper jw = JsonWrapper("test");
	printf("%s", jw.to_string().c_str());
}
