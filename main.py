"""Main module of iperf util"""
from host import Server, Client
from shell_interface import ShellParser


def main():
    """main function of project"""
    args = ShellParser().parse_arguments()
    server = Server(
        args.server_host,
        args.server_password,
        args.server_file,
    )
    client = Client(
        args.client_host,
        args.client_password,
        args.client_file,
        server.address
    )
    print(server.start())
    data = client.measure()
    print(server.stop())
    print(data)


if __name__ == '__main__':
    main()
