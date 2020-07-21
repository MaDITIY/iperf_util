"""Module with host classes"""
from sshpass_command import SSHExecutor
from subprocess import Popen, PIPE

import socket


class Singleton(type):
    """Singleton pattern meta class"""
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class IperfMachine:
    """Base class for hosts"""

    def __init__(self, host, password, password_file):
        self.host = host
        self.password = password
        self.address = self.host.split('@')[1]
        self.password_file = password_file

    def is_local(self, port=None):
        """returns True if the hostname points to the localhost, otherwise False."""
        if port is None:
            port = 22  # no port specified, lets just use the ssh port
        hostname = socket.getfqdn(self.address)
        if hostname in ("localhost", "0.0.0.0"):
            return True
        localhost = socket.gethostname()
        localaddrs = socket.getaddrinfo(localhost, port)
        targetaddrs = socket.getaddrinfo(hostname, port)
        for (family, socktype, proto, canonname, sockaddr) in localaddrs:
            for (rfamily, rsocktype, rproto, rcanonname, rsockaddr) in targetaddrs:
                if rsockaddr[0] == sockaddr[0]:
                    return True
        return False


class IperfServer(IperfMachine, metaclass=Singleton):
    """Server class"""

    def start(self):
        if self.is_local():
            print('iperf3 -s')
            process = Popen(
                'iperf3 -s',
                shell=True,
            )
            result = process.returncode
        else:
            executor = SSHExecutor(
                host=self.host,
                password=self.password,
                pass_file=self.password_file
            )
            result = executor.execute('iperf3 -s', check_output=False)
        self.running = True
        return result

    def stop(self):
        if self.running:
            if self.is_local():
                print('pkill iperf3')
                process = Popen(
                    'pkill iperf3',
                    shell=True,
                )
                result = process.returncode
            else:
                executor = SSHExecutor(
                    host=self.host,
                    password=self.password,
                    pass_file=self.password_file
                )
                result = executor.execute('pkill iperf3')
            self.running = False
            return result


class IperfClient(IperfMachine):
    """Client class"""

    def __init__(self, host, password, password_file, server_ip):
        self.server_ip = server_ip
        super(IperfClient, self).__init__(host, password, password_file)

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
