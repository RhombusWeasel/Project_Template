import json

class Blackboard:
    def __init__(self):
        self.data = {}

    def set(self, key, value, namespace='common'):
        if namespace not in self.data:
            self.data[namespace] = {}
        self.data[namespace][key] = value

    def get(self, key, default=None, namespace='common'):
        return self.data[namespace].get(key, default)
    
    def get_namespace(self, namespace):
        return self.data.get(namespace, {})
    
    def set_namespace(self, namespace, data):
        self.data[namespace] = data
    
    def get_namespaces(self):
        return list(self.data.keys())
    
    def delete(self, key, namespace='common'):
        if namespace in self.data:
            del self.data[namespace][key]

    def delete_namespace(self, namespace):
        if namespace in self.data:
            del self.data[namespace]
    
    def print(self):
        return json.dumps(self.data, indent=2)