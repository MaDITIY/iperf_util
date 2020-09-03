"""Main module of iperf util"""
from iperf_hosts.iperf_client import IperfClient
from iperf_hosts.iperf_server import IperfServer
from shell_interface import ShellParser
from output_parser import parser
from pprint import pprint


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
    output_parser = parser.Parser()
    errors = []
    start_return_code = server.start()
    if start_return_code is not None:
        raise Exception("Server can't be started")
    measure_output, measure_return_code = client.measure()
    if measure_return_code != 0:
        errors.append(measure_output[0])
    stop_output, stop_return_code = server.stop()
    if stop_return_code and stop_return_code != 0:
        errors.append(stop_output[0])
    result = output_parser.build_result(measure_output[0], errors, measure_return_code)
    pprint(result, width=100)


if __name__ == '__main__':
    main()
