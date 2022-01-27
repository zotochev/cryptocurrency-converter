import requests
from config import API_RATE


class APIHandler:
    def __init__(self):
        self.api_rate = API_RATE

    def output(self, address_1, address_2=None):
        if address_2 is None:
            return self.handle_one_address(address_1)
        else:
            return self.handle_pair_addresses(address_1, address_2)

    def handle_one_address(self, address):
        r = requests.get(f'{self.api_rate}/{address}')

        if 200 == r.status_code:
            return [r.json()['data']]
        else:
            raise UserWarning(f'API bad response. Http response code is {r.status_code}')

    def handle_pair_addresses(self, address_1, address_2):
        r1 = requests.get(f'{self.api_rate}/{address_1}')
        r2 = requests.get(f'{self.api_rate}/{address_2}')

        if 200 == r1.status_code and 200 == r2.status_code:
            return [r1.json()['data'], r2.json()['data']]
        else:
            raise UserWarning(f'API bad response. Http response code is {r1.status_code} and {r2.status_code} ')


api_handler = APIHandler()

