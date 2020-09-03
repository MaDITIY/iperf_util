import re
from collections import namedtuple


Column = namedtuple('Column', ['name', 'is_measurement_unit'], defaults=(True, ))
EXPECTED_COLUMS = {
    'Interval': Column('Interval'),
    'Transfer': Column('Transfer'),
    'Bandwidth': Column('Bandwidth'),
    'Retr': Column('Retr', False),
    'Cwnd': Column('Cwnd'),
}
LINE_REGEX = r'\[.{3}\]'  # 3 is the number of chars in bracers
HEADER_LINE_REGEX = r'([a-zA-Z]+)( *)'


class Parser:
    def build_result(self, output, errors, return_code):
        result = {
            'error': self.parse_errors(errors),
            'result': self.parse_output(output),
            'status': return_code,
        }
        return result

    def parse_output(self, iperf_output):
        result = []
        default_value = []
        current_table = None
        # get informative lines by regex and strip first 5 chars (unused part line e.g. [ ID])
        info_line = [r[5:].strip() for r in iperf_output.split('\n') if re.match(LINE_REGEX, r)]
        for line in info_line:
            if re.match(HEADER_LINE_REGEX, line):
                self.save_result(result, current_table)
                keys = line.split()
                current_table = {key: list(default_value) for key in keys}
                continue
            items = line.split()
            items.reverse()
            for column_name in current_table.keys():
                column = EXPECTED_COLUMS.get(column_name, Column(column_name))
                current_table[column_name].append(
                    " ".join([items.pop(), items.pop()]) if column.is_measurement_unit else items.pop()
                )
        self.save_result(result, current_table)
        return result

    @staticmethod
    def save_result(result, current_table):
        if current_table and any(current_table.values()):
            result.append(current_table.copy())

    @staticmethod
    def parse_errors(errors):
        return errors
