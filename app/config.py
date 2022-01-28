# API url to send price request
# usage requests.get(f'{API_RATE}/{address}')
API_RATE: str = 'https://api.pancakeswap.info/api/v2/tokens'

# API url to collect tokens symbols and name to validate mistapes
# info from this url collected in instance of TokenList
# usage requests.get(f'{API_ALL_TOKENS}')
API_ALL_TOKENS: str = 'https://api.pancakeswap.info/api/v2/tokens'

# Similarity index
# integer number that used for mistapes suggestions
# then lower number then more strict comperision
# Example:
# SIM_IND=1 is_similar("ethereum", "ethireume") -> False
# SIM_IND=2 is_similar("ethereum", "ethireume") -> True 
SIM_IND: int = 2


# update Token list
# Token list use is to collect token address by name of token
UP_TOKEN_LIST: bool = True
# number of UP_PERIOD before update
UP_EVERY: int = 10
# possible UP_PERIOD variants union('seconds' | 'minutes' | 'hours' | 'days' | 'weeks')
UP_PERIOD: str = 'seconds'


reactions = {
        "start": "👋 Hello! I'm Cryptocurrency converter bot. 💰\n"
                 "You can use a command /single and send me one token "
                 "to receive its price vs. USDT, or u\nse a command /pair "
                 "and send me a pair of coins to get their price vs. each other. "
                 "To learn more, send /help.\n"
                 "I use [PancakeSwap API](github.com/pancakeswap/pancake-info-api)",
        "help":  "💹If you want to get price of one token, send me the command "
                 "/single and in next message send a token - its address, name "
                 "or short name.\n🔄If you want to get price of two tokens vs. "
                 "each other, send me the command /pair and send the tokens in "
                 "two messages.",

        "single": "💹Send me a token to get its price.",
        "single_result": "⬇️Here it is:",

        "pair": "🔄Send me the first token.",
        "pair_next": "✅Ok, send me the next one",
        "pair_result": "⬇️Here is the price:",

        "unknown": "❌Sorry, I don't know such token.",

        "several": "❓I've found several tokens according to your request. Please select an appropriate one.",
        "unknown_command": "❌Sorry, I don't understand.",
        "api_bad_response": "Something went wrong.\nEither address you sent is not valid, or API doesn't work.",
}

if __name__ == "__main__":
    for key, value in reactions.items():
        print(key)
        print(value)
