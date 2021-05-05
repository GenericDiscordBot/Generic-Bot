class LRUDict(dict):
    def __init__(self, max_size: int = 1024, *args, **kwargs):
        if max_size <= 0:
            raise ValueError('Maximum cache size must be greater than 0.')
        self.max_size = max_size
        super().__init__(*args, **kwargs)
        self.__cleanup()

    def __cleanup(self):
        while len(self) > self.max_size:
            del self[next(iter(self))]

    def __getitem__(self, key):
        value = super().__getitem__(key)
        self.__cleanup()
        return value

    def __setitem__(self, key, value):
        super().__setitem__(key, value)
        self.__cleanup()
