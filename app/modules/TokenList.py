import requests
from nltk.metrics.distance import edit_distance

from .config import API_ALL_TOKENS, SIM_IND


class TokenList:
    def __init__(self):
        self.tokens = None

        self.update()

    def update(self):
        r = requests.get(API_ALL_TOKENS)

        if 200 == r.status_code:
            self.tokens = {address: {key: self.clean_name(value) for key, value in name_symbol.items()} for address, name_symbol in r.json()['data'].items()}

            self.symbols = list() 
            self.names = list()

            for address, name_symbol in self.tokens.items():
                # remove 'token' from names

                self.symbols.append(name_symbol['symbol'].lower())
                self.names.append(name_symbol['name'].lower())
        else:
            raise Exception(f'API bad response. Http response code is {r.status_code}')

    def output(self, user_input):
        result = self.get_address(user_input)

        if len(result) == 0:
            return self.get_similar(self.clean_name(user_input))
        else:
            return result

    def get_address(self, text):
        """Returns address of token if it is known or None otherwise
        """

        if text in self.tokens:
            return [(text, self.tokens[text]['symbol'], self.tokens[text]['name'])]
        elif text[:2] == '0x':
            return [(text, 'unknown', 'unknown')]
        else:
            text = self.clean_name(text)

            for address, name_symbol in self.tokens.items():
                if name_symbol['symbol'] == text or name_symbol['name'] == text:
                    return [(address, name_symbol['symbol'], name_symbol['name'])]
            return []

    def get_similar(self, text):
        """Returns list of similar tokens names or symbols
        """

        def is_similar(line1, line2):
            return SIM_IND >= edit_distance(line1, line2)

        result = list()

        #for symbol, name in zip(self.symbols, self.names):
        for address, name_symbol in self.tokens.items():
            if is_similar(name_symbol['symbol'], text) or is_similar(name_symbol['name'], text):
                result.append((address, name_symbol['symbol'], name_symbol['name']))

        return result

    @staticmethod
    def clean_name(name):
        name = name.lower().strip()

        ind_coin = name.rfind('coin')
        ind_token = name.rfind('token')

        if ind_coin != -1 and ind_token != -1 and min(ind_coin, ind_token) != 0:
            return name[:min(ind_coin, ind_token)].strip()
        elif ind_coin != -1 or ind_token != -1:
            return name[:max(ind_coin, ind_token)].strip()
        else:
            return name


def main():
    test = TokenList()
    t = ['et', 'eth', 'ethr', '0xferwgergerg']

    for c in t:
        print(test.output(c))



if __name__ == "__main__":
    main()
