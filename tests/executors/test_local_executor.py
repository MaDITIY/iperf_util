import unittest
from unittest import mock
from subprocess import PIPE, Popen


from executors.local_executor import LocalExecutor


class TestLocalExecutor(unittest.TestCase):
    def setUp(self):
        self.executor = LocalExecutor()

    @mock.patch.object(Popen, 'poll')
    def test_execute(self, popen_mock):
        expected_result = 'test_result'
        popen_mock.return_value = expected_result

        result = self.executor.execute(expected_result)

        self.assertEqual(result, expected_result)
        popen_mock.assert_called_once()

    @mock.patch('executors.local_executor.Popen')
    def test_execute_check_output(self, popen_mock):
        func_mock = mock.Mock()
        func_mock.communicate.return_value = 'test_result'
        func_mock.returncode = 0
        popen_mock.return_value = func_mock

        result = self.executor.execute('command', True)

        self.assertEqual(result, ('test_result', 0))
        popen_mock.assert_called()


if __name__ == '__main__':
    unittest.main()
