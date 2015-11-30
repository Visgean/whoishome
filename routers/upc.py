import requests
from pyquery import PyQuery as PQ

from .base import DHCPRecord, BaseRouter, IncorrectPassword


class Router(BaseRouter):
    """
    UPC default shit router that they gave me
    """
    login_url = '/goform/login'
    logout_url = '/logout.asp'
    dhcp_url = '/basic/dhcp.asp'
    incorrect_password = 'Given username'

    def __init__(self, router_ip, router_port, user, password):
        super().__init__(router_ip, router_port, user, password)
        self.auth_request = requests.Session()

    def login(self):
        login_page = PQ(self.auth_request.get(self.base_url).content)
        csrf_token = login_page('input[name=CSRFValue]')[0].value

        data = {
            'CSRFValue': csrf_token,
            'loginUsername': self.user,
            'loginPassword': self.password,
            'logoffUser': '0'
        }

        status = self.auth_request.post(self.base_url + self.login_url, data)
        if self.incorrect_password in status:
            raise IncorrectPassword

    def get_records(self):
        self.login()
        dhcp_page = PQ(self.auth_request.get(self.base_url + self.dhcp_url))
        dhcp_table = dhcp_page('table')[0]
        lines = dhcp_table.findall('tr')
        results = []

        for line in lines:
            parts = line.findall('td')
            results.append(
                DHCPRecord(
                    hostname=parts[0].text,
                    mac=parts[1].text,
                    ip=parts[2].text,
                    conn=parts[3].text,
                    rssi=parts[4].text,
                    expires=parts[5].text))

        self.auth_request.get(self.base_url + self.logout_url)
        return results
