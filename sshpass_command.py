from subprocess import Popen, PIPE


class SSHExecutor:
    """Class for ssh + sshpass command execution"""

    def __init__(self, host_credentials, command,
                 protocol='ssh', pass_file=None):
        """
        :param command: string command to execute
        :param host_credentials: dict of host/ip and password()
            {
                'host': 'user@192.168.xx.xx',
                'password': '*******', ( can be left empty in case of pass_file exist)
            }
        :param protocol: ssh/scp (ssh for default)
        :param pass_file: way to password file. None by default
        """
        self.command = command
        self.host_credentials = host_credentials
        self.protocol = protocol
        self.pass_file = pass_file
        self.pass_flag = None
        self.expression = None

    def execute(self):
        """method to execute command"""
        self.build_password_arg()
        self.build_expression()
        additional_flags = '-o StrictHostKeyChecking=no'
        args = [
            'sshpass',
            self.pass_flag,
            self.protocol,
            additional_flags,
            self.host_credentials['host'],
            "'" + self.command + "'",
        ]
        # command = " ".join(args)
        # print(command)
        expression = Popen(args, stdout=PIPE, stderr=PIPE, encoding='utf-8')
        return expression.communicate()

    def build_password_arg(self, ):
        """method to build password flag(from file or as arg)"""
        if self.pass_file is not None:
            self.pass_flag = f'-f {self.pass_file}'
        else:
            password = self.host_credentials['password']
            self.pass_flag = f"-p'{password}'"

    def build_expression(self):
        """method to build expression"""
        self.expression = " ".join([
            'sshpass', self.pass_flag, self.protocol, self.command
        ])
