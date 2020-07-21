from subprocess import Popen, PIPE


class SSHExecutor:
    """Class for ssh + sshpass command execution"""

    def __init__(self, host, password, protocol='ssh', pass_file=None):
        """
        :param host: 'user@192.168.xx.xx'
        :param password: '*******', ( can be left empty in case of pass_file exist)
        :param protocol: ssh/scp (ssh for default)
        :param pass_file: way to password file. None by default
        """
        self.host = host
        self.password = password
        self.protocol = protocol
        self.pass_file = pass_file
        self.pass_flag = None
        self.expression = None

    def execute(self, command, check_output=False):
        process = self._build_process(command)
        if check_output:
            result = process.communicate(), process.returncode
        else:
            result = process.poll()
        return result

    def _build_process(self, command):
        """method to build expression"""
        if self.pass_file is not None:
            self.pass_flag = f'-f {self.pass_file}'
        else:
            self.pass_flag = f"-p '{self.password}'"

        additional_flags = '-o StrictHostKeyChecking=no'
        args = [
            'sshpass',
            self.pass_flag,
            self.protocol,
            additional_flags,
            self.host,
            "'" + command + "'",
        ]
        expression = " ".join(args)
        print(expression)
        process = Popen(expression, shell=True, stdout=PIPE, stderr=PIPE,
                        encoding='utf-8', text=True)
        return process
