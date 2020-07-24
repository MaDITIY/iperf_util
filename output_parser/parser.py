import re
import json


class Parser:

    def build_result(serf, output, errors, return_code):
        result = {
            'error': serf.parse_errors(errors),
            'result': serf.parse_output(output),
            'status': return_code,
        }
        return result

    @staticmethod
    def parse_output(iperf_output):
        diff_lines = re.split(r'\[.{3}\]', iperf_output)
        deleted_linebrakers = ''.join(diff_lines).split('\n')
        result = [line.strip() for line in deleted_linebrakers if line]
        return result

    @staticmethod
    def parse_errors(errors):
        return errors