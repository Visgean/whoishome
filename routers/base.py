import re

MAC_PATTERN = re.compile('^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$')


class IncorrectMAC(Exception):
    """
    Did not your mother teach you how to spell your MAC?!
    """

class IncorrectPassword(Exception):
    """
    Raised on incorrectly typed password.
    """

class DHCPRecord(object):
    """
    Class that describes record from the DHCP server
    """
    ethernet = 'ETH'
    wifi = 'WIFI'

    conn_types = (ethernet, wifi)

    def __init__(self, hostname, mac, ip, conn=None, rssi=None, expires=None):
        """
        :param hostname: hostname of the device
        :param mac: MAC address of the device
        :param ip: assigned IP
        :param conn: ethernet or wifi
        :param rssi: strength of the signal or something like that
        :param expires: when is the record going to expire
        :return:
        """
        if MAC_PATTERN.match(mac):
            raise IncorrectMAC('Yo, clean your shite, man!')

        self.mac = mac
        self.expires = expires
        self.rssi = rssi
        self.conn = conn
        self.hostname = hostname

    def __repr__(self):
        return self.hostname


class BaseRouter(object):
    """
    Abstract class for router, this object downloads data from server
    and returns them in understandable fashion.
    """

    def __init__(self, router_ip, router_port, user, password):
        self.base_url = 'http://{0}:{1}'.format(router_ip, router_port)
        self.router_port = router_port
        self.router_ip = router_ip
        self.user = user
        self.password = password

    def get_records(self):
        """
        :return: [DHCPRecord]
        """
        raise NotImplementedError
