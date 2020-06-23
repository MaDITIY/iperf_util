"""Module to parse console args"""
import argparse


class ShellParser:
    def parse_arguments(self):
        """Parse args from console and returns it"""
        parser = argparse.ArgumentParser(description='Util to measure capacity of line between two hosts')
        required = parser.add_argument_group('required arguments')
        required.add_argument('-s', '--server_host', required=True, help='server side host')
        required.add_argument('-c', '--client_host', required=True, help='client side host')
        parser.add_argument('-sp', '--server_password', help='server side password by arg')
        parser.add_argument('-cp', '--client_password', help='client side password by arg')
        parser.add_argument('-sf', '--server_file', help='server side password by file')
        parser.add_argument('-cf', '--client_file', help='client side password by file')
        self.args = parser.parse_args()
        self.validate_args()
        return self.args

    def validate_args(self):
        if not any([self.args.client_password, self.args.client_file]):
            raise ValueError('No client password. Client password is required')
        if not any([self.args.server_password, self.args.server_file]):
            raise ValueError('No server password. Client server is required')
