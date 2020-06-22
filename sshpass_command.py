from subprocess import Popen, PIPE


class SSHExecutor:
    """Class for ssh + sshpass command execution"""

    def __init__(self, host, password, command,
                 protocol='ssh', pass_file=None):
        """
        :param command: string command to execute
        :param host: 'user@192.168.xx.xx'
        :param password: '*******', ( can be left empty in case of pass_file exist)
        :param protocol: ssh/scp (ssh for default)
        :param pass_file: way to password file. None by default
        """
        self.command = command
        self.host = host
        self.password = password
        self.protocol = protocol
        self.pass_file = pass_file
        self.pass_flag = None
        self.expression = None

    def execute(self):
        """method to execute command"""
        self.build_expression()
        print(self.expression)
        expression = Popen(self.expression, shell=True, stdout=PIPE, stderr=PIPE, encoding='utf-8')
        return expression.communicate()


    def build_expression(self):
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
            "'" + self.command + "'",
        ]
        self.expression = " ".join(args)
