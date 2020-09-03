import unittest
from unittest import mock

from iperf_hosts.iperf_server import IperfServer
from executors.local_executor import LocalExecutor
from executors.remote_executor import SSHExecutor
from utils import Singleton


class TestIperfServer(unittest.TestCase):
    def setUp(self):
        with mock.patch.dict(Singleton._instances, {}, clear=True):
            self.start_command = 'iperf3 -s'
            self.stop_command = 'pkill iperf3'
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
    def test_remote_start(self, execute):
        execute.return_value = 'test result'
        with mock.patch.object(IperfServer, 'is_local', return_value=False):
            result = self.server.start()
        execute.assert_called_once_with(self.start_command)
        self.assertEqual(result, 'test result')

    @mock.patch.object(LocalExecutor, 'execute')
    def test_local_start(self, execute):
        execute.return_value = 'test result'
        with mock.patch.object(IperfServer, 'is_local', return_value=True):
            result = self.server.start()
        execute.assert_called_once_with(self.start_command)
        self.assertEqual(result, 'test result')

    @mock.patch.object(IperfServer, 'is_running', return_value=False)
    def test_stop(self, _):
        self.assertEqual(self.server.stop(), (None, None))

    @mock.patch.object(IperfServer, 'is_running', return_value=True)
    @mock.patch.object(SSHExecutor, 'execute')
    def test_remote_stop(self, execute_mock, _):
        execute_mock.return_value = 'test result'
        with mock.patch.object(IperfServer, 'is_local', return_value=False):
            result = self.server.stop()
        execute_mock.assert_called_once_with(self.stop_command, check_output=True)
        self.assertEqual(result, 'test result')

    @mock.patch.object(IperfServer, 'is_running', return_value=True)
    @mock.patch.object(LocalExecutor, 'execute')
    def test_local_stop(self, execute_mock, _):
        execute_mock.return_value = 'test result'
        with mock.patch.object(IperfServer, 'is_local', return_value=True):
            result = self.server.stop()
        execute_mock.assert_called_once_with(self.stop_command, check_output=True)
        self.assertEqual(result, 'test result')


if __name__ == '__main__':
    unittest.main()
