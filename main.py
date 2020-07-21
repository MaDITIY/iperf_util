"""Main module of iperf util"""
from host import IperfServer, IperfClient
from shell_interface import ShellParser


def main():
    """main function of project"""
    args = ShellParser().parse_arguments()
    server = IperfServer(
        args.server_host,
        args.server_password,
        args.server_file,
    )
    client = IperfClient(
        args.client_host,
        args.client_password,
        args.client_file,
        server.address
    )
    server.start()
    data = client.measure()
    server.stop()
    print(data)


if __name__ == '__main__':
    main()
