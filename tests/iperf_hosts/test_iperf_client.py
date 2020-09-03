import unittest
from unittest import mock

from iperf_hosts.iperf_client import IperfClient
from executors.local_executor import LocalExecutor
from executors.remote_executor import SSHExecutor


class TestIperfClient(unittest.TestCase):
    def setUp(self):
        server_ip = '2.2.2.2'
        self.command = f'iperf3 -c {server_ip}'
        self.server = IperfClient(
            'somehost@1.1.1.1',
            'secret',
            None,
            server_ip
        )

    @mock.patch.object(SSHExecutor, 'execute')
    def test_remote_measure(self, execute):
        execute.return_value = 'test result'
        with mock.patch.object(IperfClient, 'is_local', return_value=False):
            result = self.server.measure()
        execute.assert_called_once_with(self.command, check_output=True)
        self.assertEqual(result, 'test result')

    @mock.patch.object(LocalExecutor, 'execute')
    def test_local_measure(self, execute):
        execute.return_value = 'test result'
        with mock.patch.object(IperfClient, 'is_local', return_value=True):
            result = self.server.measure()
        execute.assert_called_once_with(self.command, check_output=True)
        self.assertEqual(result, 'test result')


if __name__ == '__main__':
    unittest.main()
