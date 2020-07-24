import re


class Parser:

    def build_result(self, output, errors, return_code):
        result = {
            'error': self.parse_errors(errors),
            'result': self.parse_output(output),
            'status': return_code,
        }
        return result

    @staticmethod
    def parse_output(iperf_output):
        diff_lines = re.split(r'\[.{3}\]', iperf_output)
        deleted_linebrakers = ''.join(diff_lines).split('\n')
        lines = [line.strip() for line in deleted_linebrakers if line]
        needed_lines = lines[2:13]
        keys = needed_lines[0].split()
        default_value = []
        result = {key: list(default_value) for key in keys}
        for index, key in enumerate(keys):
            for line in needed_lines[1:]:
                values = re.split(r' {2,}', line)
                values = [' '.join(values[:2])] + values[2:]
                result[key].append(values[index])
        return result

    @staticmethod
    def parse_errors(errors):
        return errors