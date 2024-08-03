from collections import OrderedDict


class FileCache:
    def __init__(self, max_size=10):
        self.max_size = max_size
        self.cache = OrderedDict()

    def get(self, file_path):
        if file_path in self.cache:
            # Move the accessed item to the end (most recently used)
            self.cache.move_to_end(file_path)
            return self.cache[file_path]
        return None

    def set(self, file_path, content):
        if file_path in self.cache:
            # Update existing entry and move to end
            self.cache.move_to_end(file_path)
        elif len(self.cache) >= self.max_size:
            # Remove least recently used item
            self.cache.popitem(last=False)
        self.cache[file_path] = content

    def remove(self, file_path):
        if file_path in self.cache:
            del self.cache[file_path]

    def clear(self):
        self.cache.clear()
