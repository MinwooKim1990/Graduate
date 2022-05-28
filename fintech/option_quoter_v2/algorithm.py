import datetime as dt
import time
import logging

from optibook.synchronous_client import Exchange

from math import floor, ceil
from black_scholes import call_value, put_value, call_delta, put_delta
from libs import calculate_current_time_to_date

exchange = Exchange()
exchange.connect()

logging.getLogger('client').setLevel('ERROR')


STOCK_ID = 'BMW'
OPTIONS = [
    {'id': 'BMW-2022_03_18-050C', 'expiry_date': dt.datetime(2022, 3, 18, 12, 0, 0), 'strike': 50, 'callput': 'call'},
    {'id': 'BMW-2022_03_18-050P', 'expiry_date': dt.datetime(2022, 3, 18, 12, 0, 0), 'strike': 50, 'callput': 'put'},
    {'id': 'BMW-2022_03_18-075C', 'expiry_date': dt.datetime(2022, 3, 18, 12, 0, 0), 'strike': 75, 'callput': 'call'},
    {'id': 'BMW-2022_03_18-075P', 'expiry_date': dt.datetime(2022, 3, 18, 12, 0, 0), 'strike': 75, 'callput': 'put'},
    {'id': 'BMW-2022_03_18-100C', 'expiry_date': dt.datetime(2022, 3, 18, 12, 0, 0), 'strike': 100, 'callput': 'call'},
    {'id': 'BMW-2022_03_18-100P', 'expiry_date': dt.datetime(2022, 3, 18, 12, 0, 0), 'strike': 100, 'callput': 'put'},
    {'id': 'BMW-2022_03_18-125C', 'expiry_date': dt.datetime(2022, 3, 18, 12, 0, 0), 'strike': 125, 'callput': 'call'},
    {'id': 'BMW-2022_03_18-125P', 'expiry_date': dt.datetime(2022, 3, 18, 12, 0, 0), 'strike': 125, 'callput': 'put'},
    {'id': 'BMW-2022_03_18-150C', 'expiry_date': dt.datetime(2022, 3, 18, 12, 0, 0), 'strike': 150, 'callput': 'call'},
    {'id': 'BMW-2022_03_18-150P', 'expiry_date': dt.datetime(2022, 3, 18, 12, 0, 0), 'strike': 150, 'callput': 'put'},
]


while True:
    print(f'')
    print(f'-----------------------------------------------------------------')
    print(f'TRADE LOOP ITERATION ENTERED AT {str(dt.datetime.now()):18s} UTC.')
    print(f'-----------------------------------------------------------------')

    # TODO: Determine stock value
    stock_value=(exchange.get_last_price_book(STOCK_ID).bids[0].price + exchange.get_last_price_book(STOCK_ID).asks[0].price)/2
    # For each option
    for option in OPTIONS:
        # Print which option we are updating
        print(f'''Updating option {option['id']} with expiry date {option['expiry_date']}, strike {option['strike']} '''
              f'''and type {option['callput']}.''')

        # TODO: Delete existing orders
        exchange.delete_orders(option['id'])
        time.sleep(1)
        # TODO: Calculate option value
    print(stock_value)
    option_value={}
    for option in OPTIONS:
        if option['callput'] == 'call' :
            option_value[option['id']] = call_value(stock_value, option['strike'], calculate_current_time_to_date(option['expiry_date']),0,3)
        else :
            option_value[option['id']] = put_value(stock_value, option['strike'], calculate_current_time_to_date(option['expiry_date']),0,3)
    print(option_value)

        # TODO: Calculate desired bid and ask prices
    stock_id=[]
    price=[]
    side=[]
    if stock_value < 50 :
        bid1=option_value['BMW-2022_03_18-050P']
        ask1=option_value['BMW-2022_03_18-050C']
        stock_id=['BMW-2022_03_18-050P', 'BMW-2022_03_18-050C']
        price=[bid1,ask1]
        side=['bid','ask']
    elif stock_value >=50 and stock_value < 75 :
        bid1=option_value['BMW-2022_03_18-050C']
        ask1=option_value['BMW-2022_03_18-050P']
        bid2=option_value['BMW-2022_03_18-075P']
        ask2=option_value['BMW-2022_03_18-075C']
        stock_id=['BMW-2022_03_18-050C', 'BMW-2022_03_18-050P','BMW-2022_03_18-075P', 'BMW-2022_03_18-075C']
        price=[bid1,ask1,bid2,ask2]
        side=['bid','ask','bid','ask']
    elif stock_value >= 75 and stock_value < 100 :
        bid1=option_value['BMW-2022_03_18-075C']
        ask1=option_value['BMW-2022_03_18-075P']
        bid2=option_value['BMW-2022_03_18-100P']
        ask2=option_value['BMW-2022_03_18-100C']
        stock_id=['BMW-2022_03_18-075C', 'BMW-2022_03_18-075P','BMW-2022_03_18-100P', 'BMW-2022_03_18-100C']
        price=[bid1,ask1,bid2,ask2]
        side=['bid','ask','bid','ask']
    elif stock_value >= 100 and stock_value < 125 :
        bid1=option_value['BMW-2022_03_18-100C']
        ask1=option_value['BMW-2022_03_18-100P']
        bid2=option_value['BMW-2022_03_18-125P']
        ask2=option_value['BMW-2022_03_18-125C']
        stock_id=['BMW-2022_03_18-100C', 'BMW-2022_03_18-100P','BMW-2022_03_18-125P', 'BMW-2022_03_18-125C']
        price=[bid1,ask1,bid2,ask2]
        side=['bid','ask','bid','ask']
    elif stock_value > 125 and stock_value < 150 :
        bid1=option_value['BMW-2022_03_18-125C']
        ask1=option_value['BMW-2022_03_18-125P']
        bid2=option_value['BMW-2022_03_18-150P']
        ask2=option_value['BMW-2022_03_18-150C']
        stock_id=['BMW-2022_03_18-125C', 'BMW-2022_03_18-125P','BMW-2022_03_18-150P', 'BMW-2022_03_18-150C']
        price=[bid1,ask1,bid2,ask2]
        side=['bid','ask','bid','ask']
    else :
        bid1=option_value['BMW-2022_03_18-150C']
        ask1=option_value['BMW-2022_03_18-150P']
        stock_id=['BMW-2022_03_18-150C', 'BMW-2022_03_18-150P']
        price=[bid1,ask1]
        side=['bid','ask']
        # TODO: Insert limit orders on those prices for a desired volume
    volume = 10
    #if not trade_would_breach_position_limit(stock_id, volume, side, 5):
    for i in range(len(stock_id)):
        print(f'''Inserting {side[i]} for {stock_id[i]}: {volume:.0f} lot(s) at price {price[i]:.2f}.''')
        exchange.insert_order(
            instrument_id=stock_id[i],
            price=round(float(price[i]),2),
            volume=volume,
            side=side[i],
            order_type='limit')
    else:
        print(f'''Not inserting {volume:.0f} lot {side} for {stock_id} to avoid position-limit breach.''')
        # Wait 1/10th of a second to avoid breaching the exchange frequency limit
        time.sleep(0.10)

    # TODO: Calculate current delta position across all instruments
    # TODO: Calculate stocks to buy/sell to become close to delta-neutral
    # TODO: Perform the hedging stock trade by inserting an IOC order on the stock against the current top-of-book

    # Sleep until next iteration
    print(f'\nSleeping for 4 seconds.')
    time.sleep(4)
