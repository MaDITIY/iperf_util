import unittest
from unittest import mock
from subprocess import PIPE


from iperf_hosts.iperf_server import IperfServer
from main import main


class TestMain(unittest.TestCase):

    @mock.patch('main.ShellParser.parse_arguments')
    @mock.patch.object(IperfServer, 'start', return_value=1)
    def test_server_star_error(self, server_start_mock, _):
        with self.assertRaises(Exception):
            main()


if __name__ == '__main__':
    unittest.main()
