import ddt

import unittest
from unittest import mock

from iperf_hosts.iperf_server import IperfServer
from executors.local_executor import LocalExecutor
from executors.remote_executor import SSHExecutor


class TestIperfServer(unittest.TestCase):
    def setUp(self):
        self.server = IperfServer(
            'somehost@1.1.1.1',
            'secret',
            None
        )

    @mock.patch.object(LocalExecutor, 'execute')
    @mock.patch.object(IperfServer, 'is_local', return_value=True)
    def test_start(self, _, __):
        self.assertFalse(self.server.is_running())
        self.server.start()
        self.assertTrue(self.server.is_running())

    @mock.patch.object(SSHExecutor, 'execute')
    @mock.patch.object(IperfServer, 'is_local', return_value=False)
    def test_remote_start(self, method, execute):
        self.server.start()
        method.assert_called_once()
        execute.assert_called_once()


if __name__ == '__main__':
    unittest.main()