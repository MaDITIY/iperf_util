from iperf_hosts.iperf_machine import IperfMachine
from executors.remote_executor import SSHExecutor
from executors.local_executor import LocalExecutor


class IperfClient(IperfMachine):
    """Client class"""

    def __init__(self, host, password, password_file, server_ip):
        self.server_ip = server_ip
        super(IperfClient, self).__init__(host, password, password_file)

    def measure(self):
        command = f'iperf3 -c {self.server_ip}'
        if self.is_local():
            executor = LocalExecutor()
        else:
            executor = SSHExecutor(
                host=self.host,
                password=self.password,
                pass_file=self.password_file
            )
        return executor.execute(command, check_output=True)
