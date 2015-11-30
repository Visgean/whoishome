import re

MAC_PATTERN = re.compile('^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$')


class IncorrectMAC(Exception):
    """
    Did not your mother teach you how to spell your MAC?!
    """


class DHCPRecord(object):
    """
    Class that describes record from the DHCP server
    """
    ethernet = 'ETH'
    wifi = 'WIFI'

    conn_types = (ethernet, wifi)

    def __init__(self, hostname, mac, conn_type=None, rssi=None, expires=None):
        """

        :param hostname: hostname of the device
        :param mac: MAC address of the device
        :param conn_type: ethernet or
        :param rssi: strength of the signal or something like that
        :param expires: when is the record going to expire
        :return:
        """
        if MAC_PATTERN.match(mac):
            raise IncorrectMAC('Yo, clean your shite, man!')

        self.mac = mac
        self.expires = expires
        self.rssi = rssi
        self.conn_type = conn_type
        self.hostname = hostname


class BaseRouter(object):
    """
    Abstract class for router, this object downloads data from server
    and returns them in understandable fashion.
    """

    def __init__(self, router_ip, router_port):
        self.router_port = router_port
        self.router_ip = router_ip

    def get_records(self):
        """
        :return: [DHCPRecord]
        """
        raise NotImplementedError
