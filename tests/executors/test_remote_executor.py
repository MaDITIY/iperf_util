import unittest
from unittest import mock
from subprocess import PIPE


from executors.remote_executor import SSHExecutor


class TestSSHExecutor(unittest.TestCase):
    def setUp(self):
        self.host = 'somehost@1.1.1.1'
        self.password = 'secret'
        self.executor = SSHExecutor(self.host, self.password)

    @mock.patch.object(SSHExecutor, '_build_process')
    def test_execute_check_output(self, build_method_mock):
        popen_mock = mock.Mock()
        popen_mock.communicate = mock.Mock()
        expected_result = ('test_result', 0)
        popen_mock.communicate.return_value = expected_result[0]
        popen_mock.returncode = expected_result[1]
        build_method_mock.return_value = popen_mock

        result = self.executor.execute('some_command', True)

        self.assertEqual(result, expected_result)
        popen_mock.communicate.assert_called_once()

    @mock.patch.object(SSHExecutor, '_build_process')
    def test_execute(self, build_method_mock):
        popen_mock = mock.Mock()
        popen_mock.poll = mock.Mock()
        expected_result = 'test_result'
        popen_mock.poll.return_value = expected_result
        build_method_mock.return_value = popen_mock

        result = self.executor.execute('some_command')

        self.assertEqual(result, expected_result)
        popen_mock.poll.assert_called_once()

    @mock.patch('executors.remote_executor.Popen')
    def test_build_process(self, popen_mock):
        command = 'test_command'
        expected_expression = f"sshpass -p '{self.password}' ssh -o StrictHostKeyChecking=no " \
                              f"{self.host} '{command}'"
        self.executor._build_process(command)
        popen_mock.assert_called_with(
            expected_expression, shell=True, stdout=PIPE, stderr=PIPE,
            encoding='utf-8', universal_newlines=True
        )

    @mock.patch('executors.remote_executor.Popen')
    def test_build_process_pass_file(self, popen_mock):
        self.executor = SSHExecutor(self.host, None, pass_file='some_file.txt')
        command = 'test_command'
        expected_expression = f"sshpass -f some_file.txt ssh -o StrictHostKeyChecking=no " \
                              f"{self.host} '{command}'"
        self.executor._build_process(command)
        popen_mock.assert_called_with(
            expected_expression, shell=True, stdout=PIPE, stderr=PIPE,
            encoding='utf-8', universal_newlines=True
        )


if __name__ == '__main__':
    unittest.main()
