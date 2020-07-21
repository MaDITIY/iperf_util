from iperf_hosts.iperf_machine import IperfMachine
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


class IperfServer(IperfMachine, metaclass=Singleton):
    """Server class"""

    def start(self):
        if self.is_local():
            print('iperf3 -s')
            process = Popen(
                'iperf3 -s',
                shell=True,
                stdout=PIPE,
                stderr=PIPE,
            )
            result = process.poll()
        else:
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
            if self.is_local():
                print('pkill iperf3')
                process = Popen(
                    'pkill iperf3',
                    shell=True,
                    stdout=PIPE,
                    stderr=PIPE
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
