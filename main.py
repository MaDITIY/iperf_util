from shell_interface import ShellParser


def measure_capacity():
    args = ShellParser().parse_arguments()
    validate_args(args)


def validate_args(args):
    if not any([args.client_password, args.client_file]):
        raise ValueError('No client password. Client password is required')
    if not any([args.server_password, args.server_file]):
        raise ValueError('No server password. Client server is required')


if __name__ == '__main__':
    measure_capacity()
