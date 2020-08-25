from iperf_hosts.iperf_machine import IperfMachine
from executors.remote_executor import SSHExecutor
from executors.local_executor import LocalExecutor
from utils import Singleton


class IperfServer(IperfMachine, metaclass=Singleton):
    """Server class"""

    def __init__(self, host, password, password_file):
        self._running = False
        super(IperfServer, self).__init__(host, password, password_file)

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
        self._running = True
        return result

    def stop(self):
        if self.is_running():
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
            self._running = False
            return result

    def is_running(self):
        return self._running
