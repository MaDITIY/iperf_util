import unittest
from unittest import mock

from output_parser.parser import Parser


TEST_IPERF_OUTPUT = """
Connecting to host 1.1.1.1, port 5201
[  4] local 2.2.2.2 port 35138 connected to 1.1.1.1 port 5201
[ ID] Interval           Transfer     Bandwidth       Retr  Cwnd
[  4]   0.00-1.00   sec   703 MBytes  5.89 Gbits/sec    0   3.12 MBytes       
[  4]   1.00-2.00   sec   732 MBytes  6.14 Gbits/sec    0   3.12 MBytes       
[  4]   2.00-3.00   sec   685 MBytes  5.75 Gbits/sec    0   3.12 MBytes       
[  4]   3.00-4.00   sec   728 MBytes  6.10 Gbits/sec    0   3.12 MBytes       
[  4]   4.00-5.00   sec   701 MBytes  5.89 Gbits/sec    0   3.12 MBytes       
[  4]   5.00-6.00   sec   746 MBytes  6.25 Gbits/sec    0   3.12 MBytes       
[  4]   6.00-7.00   sec   692 MBytes  5.81 Gbits/sec    0   3.12 MBytes       
[  4]   7.00-8.00   sec   696 MBytes  5.84 Gbits/sec    0   3.12 MBytes       
[  4]   8.00-9.00   sec   706 MBytes  5.92 Gbits/sec    0   3.12 MBytes       
[  4]   9.00-10.00  sec   614 MBytes  5.15 Gbits/sec    0   3.12 MBytes       
- - - - - - - - - - - - - - - - - - - - - - - - -
[ ID] Interval           Transfer     Bandwidth       Retr
[  4]   0.00-10.00  sec  6.84 GBytes  5.87 Gbits/sec    0             sender
[  4]   0.00-10.00  sec  6.84 GBytes  5.87 Gbits/sec    0             receiver

iperf Done.

"""

TEST_PARSED_OUTPUT = [
    {'Bandwidth': [
            '5.89 Gbits/sec',
            '6.14 Gbits/sec',
            '5.75 Gbits/sec',
            '6.10 Gbits/sec',
            '5.89 Gbits/sec',
            '6.25 Gbits/sec',
            '5.81 Gbits/sec',
            '5.84 Gbits/sec',
            '5.92 Gbits/sec',
            '5.15 Gbits/sec'],
     'Cwnd': [
            '3.12 MBytes',
            '3.12 MBytes',
            '3.12 MBytes',
            '3.12 MBytes',
            '3.12 MBytes',
            '3.12 MBytes',
            '3.12 MBytes',
            '3.12 MBytes',
            '3.12 MBytes',
            '3.12 MBytes'],
     'Interval': [
            '0.00-1.00 sec',
            '1.00-2.00 sec',
            '2.00-3.00 sec',
            '3.00-4.00 sec',
            '4.00-5.00 sec',
            '5.00-6.00 sec',
            '6.00-7.00 sec',
            '7.00-8.00 sec',
            '8.00-9.00 sec',
            '9.00-10.00 sec'],
     'Retr': ['0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
     'Transfer': [
            '703 MBytes',
            '732 MBytes',
            '685 MBytes',
            '728 MBytes',
            '701 MBytes',
            '746 MBytes',
            '692 MBytes',
            '696 MBytes',
            '706 MBytes',
            '614 MBytes']},
    {'Bandwidth': ['5.87 Gbits/sec', '5.87 Gbits/sec'],
     'Interval': ['0.00-10.00 sec', '0.00-10.00 sec'],
     'Retr': ['0', '0'],
     'Transfer': ['6.84 GBytes', '6.84 GBytes']}
]


class TestParser(unittest.TestCase):

    def test_parse_output(self):
        result = Parser().parse_output(TEST_IPERF_OUTPUT)
        self.assertEqual(result, TEST_PARSED_OUTPUT)

    @mock.patch.object(Parser, 'parse_errors')
    @mock.patch.object(Parser, 'parse_output')
    def test_build_result(self, output_mock, errors_mock):
        output_param = 'output'
        errors_param = 'errors'
        status_code = 0
        output_mock.return_value = output_param
        errors_mock.return_value = errors_param
        expected_result = {
            'error': errors_param,
            'result': output_param,
            'status': status_code,
        }

        result = Parser().build_result(output_param, errors_param, status_code)

        output_mock.assert_called_once_with(output_param)
        errors_mock.assert_called_once_with(errors_param)
        self.assertEqual(result, expected_result)

    def test_save_result(self):
        empty_table = {}
        not_empty_table = {'key': 'value'}
        result = []

        Parser().save_result(result, empty_table)
        self.assertEqual(result, [])

        Parser().save_result(result, not_empty_table)
        self.assertEqual(result, [not_empty_table])

    def test_parse_errors(self):
        errors = 'errors'
        self.assertEqual(Parser().parse_errors(errors), errors)


if __name__ == '__main__':
    unittest.main()
