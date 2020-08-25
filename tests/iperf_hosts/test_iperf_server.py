import unittest
from unittest import mock

from iperf_hosts.iperf_server import IperfServer
from executors.local_executor import LocalExecutor


class TestIperfServer(unittest.TestCase):
    def setUp(self):
        self.server = IperfServer(
            'somehost@1.1.1.1',
            'secret',
            None
        )

    def test_start(self):
        with mock.patch.object(IperfServer, 'is_local', return_value=True):
            executor = LocalExecutor()
            executor.execute = mock.MagicMock()
            self.assertFalse(self.server.is_running())
            self.server.start()
            self.assertTrue(self.server.is_running())
