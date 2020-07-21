from iperf_hosts.iperf_machine import IperfMachine
from executors.remote_executor import SSHExecutor
from executors.local_executor import LocalExecutor


class Singleton(type):
    """Singleton pattern meta class"""
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class IperfServer(IperfMachine, metaclass=Singleton):
    """Server class"""

    def start(self):
        command = 'iperf3 -s'
        if self.is_local():
            executor = LocalExecutor()
        else:
            executor = SSHExecutor(
                host=self.host,
                password=self.password,
                pass_file=self.password_file
            )
        result = executor.execute(command)
        self.running = True
        return result

    def stop(self):
        if self.running:
            command = 'pkill iperf3'
            if self.is_local():
                executor = LocalExecutor()
            else:
                executor = SSHExecutor(
                    host=self.host,
                    password=self.password,
                    pass_file=self.password_file
                )
            result = executor.execute(command, check_output=True)
            self.running = False
            return result
