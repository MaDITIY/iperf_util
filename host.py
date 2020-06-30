"""Module with host classes"""
from sshpass_command import SSHExecutor
from subprocess import Popen, PIPE


class Singleton(type):
    """Singleton pattern meta class"""
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Host:
    """Base class for hosts"""

    def __init__(self, host, password, password_file):
        self.host = host
        self.password = password
        self.address = self.host.split('@')[1]
        self.password_file = password_file

    def is_local(self):
        if isinstance(self, Client):
            return True
        return False


class Server(Host, metaclass=Singleton):
    """Server class"""

    def start(self):
        executor = SSHExecutor(
            host=self.host,
            password=self.password,
            pass_file=self.password_file
        )
        result = executor.execute('iperf3 -s')
        self.running = True
        return result

    def stop(self):
        if self.running:
            executor = SSHExecutor(
                host=self.host,
                password=self.password,
                pass_file=self.password_file
            )
            result = executor.execute('pkill iperf3')
            self.running = False
            return result


class Client(Host):
    """Client class"""

    def __init__(self, host, password, password_file, server_ip):
        self.server_ip = server_ip
        super(Client, self).__init__(host, password, password_file)

    def measure(self):
        command = f'iperf3 -c {self.server_ip}'
        if self.is_local():
            print(command)
            process = Popen(
                command,
                shell=True,
                stdout=PIPE,
                stderr=PIPE,
                encoding='utf-8'
            )
            return process.communicate()
        else:
            executor = SSHExecutor(
                host=self.host,
                password=self.password,
                pass_file=self.password_file
            )
            return executor.execute(command)
