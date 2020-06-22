"""Main module of iperf util"""
from host import Server, Client
from shell_interface import ShellParser
from sshpass_command import SSHExecutor


def main():
    """main function of project"""
    args = ShellParser().parse_arguments()
    validate_args(args)
    server_password, client_password = exclude_passwords(args)
    server = Server(args.server_host, server_password)
    client = Client(args.client_host, client_password)
    data = measure_capacity(server, client)
    print(data)


def validate_args(args):
    if not any([args.client_password, args.client_file]):
        raise ValueError('No client password. Client password is required')
    if not any([args.server_password, args.server_file]):
        raise ValueError('No server password. Client server is required')


def exclude_passwords(args):
    server_password = args.server_password if args.server_password else read_password_file(args.server_file)
    client_password = args.client_password if args.client_password else read_password_file(args.client_file)
    return server_password, client_password


def read_password_file(filename):
    raise Exception('Reading from file is not implemented yet')


def measure_capacity(server, client):
    server_command = SSHExecutor(server.host, server.password, 'iperf -s -t 10')
    client_command = SSHExecutor(client.host, client.password, f'iperf -c {server.address} -t 10')
    server_command.execute()
    return client_command.execute()


if __name__ == '__main__':
    main()
