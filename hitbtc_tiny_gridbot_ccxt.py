'''
This is a sample of a small GridBot written in Python, using 
the CCXT library, with which it connects to the HitBTC exchange. 
The bot operates only within the range specified in the 
settings and for a limited time.
Disclaimer: This code is for educational and demonstration purposes. 
It should not be considered an investment tool at all and its use 
does not make the author responsible for the results.
'''
__version__ = '1.0'
__author__ = 'Santiago A. Orellana Perez'
__created__ = '16/junio/2022'
__tested__ = 'Python 3.10'

import ccxt, threading, time, json
from decimal import *

CREDENTIALS = json.loads(open('./credential_hitbtc.json').readline())

CONF = {
    'base':'ETH',	
    'quote':'BTC',
    'amount':0.00001,		# Amount of BTC that you want to trade in each trade.
    'fee_percent':0.25,		# Fee charged by HitBTC for each market taker trade.
    'limit_down':0, 		# Lower limit below which it does not operate.
    'limit_up':21000 		# Upper limit above which there is no operation.
    }

exchange = (getattr(ccxt, 'hitbtc'))({
    "apiKey": CREDENTIALS['key'],
    "secret": CREDENTIALS['secret']
    })

# Calculate the activation threshold of the operations. 
# This value was established from the parameter 2.75 that has been obtained 
# experimentally as the limit from which profits can be obtained when the fee is 0.25%. 
# To learn how to get this parameter on other exchanges, see the repository titled FeeThresoldDetect.
thresold = Decimal(CONF['fee_percent']) * Decimal(2.75) * Decimal(100)

marketBegin, market = exchange.fetch_ticker(CONF['base']+'/'+CONF['quote']), None
lastOpp = {'side':'buy', 'price':marketBegin['last']}
minutes = 0        
while time.sleep(1) == None:
    try: 
        CONF['limit_minutes'] -= 1
        ticker = exchange.fetch_ticker(CONF['base']+'/'+CONF['quote'])

        # Calculate the profit potential of the new price with respect to the last trade.
        delta = (Decimal(float(ticker['last'])) - Decimal(float(lastOpp['price']))) 
		profit = (delta / Decimal(float(lastOpp['price']))) * 100

        # It shows the market and power data in each iteration.
        print('{} {:0.10f} {} potential: {:0.2f} %'.format(ticker['datetime'], ticker['last'], CONF['quote'], profit))

        # If the potential profit is above the trade fee, execute the trade.
        if (profit > thresold or profit < -thresold) and
            float(market['last']) < CONF['limit_up'] and
            float(market['last']) > CONF['limit_down']:

            # Execute the order at the specified price and wait for immediate.
            side = 'sell' if profit > 0 else 'buy'
            lastOpp = exchange.createOrder(
                CONF['base']+'/'+CONF['quote'],
                'limit',
                side,
                CONF['amount'],
                market['last'],
                {'time_in_force':'IOC'}
            )

            # Shows the result of the executed operation.
            print('{}  {:0.10f} {} {} {:0.10f} {}'.format(
                lastOpp['datetime'],
                lastOpp['average'],
                CONF['quote'],
                side.upper(),
                lastOpp['filled'],
                CONF['quote']
            )) 
    except: 
		print('Retry...')



