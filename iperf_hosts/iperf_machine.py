import socket


class IperfMachine:
    """Base class for hosts"""

    def __init__(self, host, password, password_file):
        self.host = host
        self.password = password
        self.address = self.host.split('@')[1]
        self.password_file = password_file

    def is_local(self, port=None):
        """returns True if the hostname points to the localhost, otherwise False."""
        if port is None:
            port = 22  # no port specified, lets just use the ssh port
        hostname = socket.getfqdn(self.address)
        if hostname in ("localhost", "0.0.0.0"):
            return True
        localhost = socket.gethostname()
        localaddrs = socket.getaddrinfo(localhost, port)
        targetaddrs = socket.getaddrinfo(hostname, port)
        for (family, socktype, proto, canonname, sockaddr) in localaddrs:
            for (rfamily, rsocktype, rproto, rcanonname, rsockaddr) in targetaddrs:
                if rsockaddr[0] == sockaddr[0]:
                    return True
        return False
