"""Module with host classes"""

class Host():
    """Base class for hosts"""

    def __init__(self, host, password):
        self.host = host
        self.password = password
        self.address = self.host.split('@')[1]


class Singleton(type):
    """Singleton pattern meta class"""
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Server(Host, metaclass=Singleton):
    """Server class"""


class Client(Host):
    """Client class"""
