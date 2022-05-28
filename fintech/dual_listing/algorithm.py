import datetime as dt
import time
import random
import logging

from optibook.synchronous_client import Exchange

exchange = Exchange()
exchange.connect()

logging.getLogger('client').setLevel('ERROR')


def trade_would_breach_position_limit(instrument_id, volume, side, position_limit):
    positions = exchange.get_positions()
    position_instrument = positions[instrument_id]

    if side == 'bid':
        return position_instrument + volume > position_limit
    elif side == 'ask':
        return position_instrument - volume < -position_limit
    else:
        raise Exception(f'''Invalid side provided: {side}, expecting 'bid' or 'ask'.''')


def print_positions_and_pnl():
    positions = exchange.get_positions()
    pnl = exchange.get_pnl()

    print('Positions:')
    for instrument_id in positions:
        print(f'  {instrument_id:10s}: {positions[instrument_id]:4.0f}')

    print(f'\nPnL: {pnl:.2f}')


STOCK_A_ID = 'PHILIPS_A'
STOCK_B_ID = 'PHILIPS_B'

bida=0#exchange.get_last_price_book(STOCK_A_ID).asks[0].price
bidb=0#exchange.get_last_price_book(STOCK_B_ID).asks[0].price
aska=0#exchange.get_last_price_book(STOCK_A_ID).bids[0].price
askb=0#exchange.get_last_price_book(STOCK_B_ID).bids[0].price

i=0
j=0
while True:
    print(f'')
    print(f'-----------------------------------------------------------------')
    print(f'TRADE LOOP ITERATION ENTERED AT {str(dt.datetime.now()):18s} UTC.')
    print(f'-----------------------------------------------------------------')

    print_positions_and_pnl()
    print(f'')
    
    print(1)
    key=True
    while key:
        i+=1
        print(i,'times')
        value_a=exchange.get_positions()[STOCK_A_ID]*exchange.get_last_price_book(STOCK_A_ID).bids[0].price
        value_b=exchange.get_positions()[STOCK_B_ID]*exchange.get_last_price_book(STOCK_B_ID).bids[0].price
        value=value_a+value_b
        
        time.sleep(3)
        if not (exchange.get_last_price_book(STOCK_A_ID) and exchange.get_last_price_book(STOCK_A_ID).bids and exchange.get_last_price_book(STOCK_A_ID).asks):
            time.sleep(2)
        elif not (exchange.get_last_price_book(STOCK_B_ID) and exchange.get_last_price_book(STOCK_B_ID).bids and exchange.get_last_price_book(STOCK_B_ID).asks):
            time.sleep(2)
        print(2)
        
        #if j == 0:
            #print(3)

        if value_a < exchange.get_positions()[STOCK_A_ID]*exchange.get_last_price_book(STOCK_A_ID).bids[0].price and (exchange.get_positions()[STOCK_A_ID] + exchange.get_positions()[STOCK_B_ID]) < 10:
            side = 'bid'
            stock_id = STOCK_A_ID
            bid=bida
            ask=aska
            print(4)
            key=False
        elif value_a > exchange.get_positions()[STOCK_A_ID]*exchange.get_last_price_book(STOCK_A_ID).bids[0].price and (exchange.get_positions()[STOCK_A_ID] + exchange.get_positions()[STOCK_B_ID]) > -1:
            side = 'ask'
            stock_id = STOCK_A_ID
            bid=bida
            ask=aska
            print(5)
            key=False
        elif value_b < exchange.get_positions()[STOCK_B_ID]*exchange.get_last_price_book(STOCK_B_ID).bids[0].price and (exchange.get_positions()[STOCK_A_ID] + exchange.get_positions()[STOCK_B_ID]) < 10:
            side = 'bid'
            stock_id = STOCK_B_ID
            bid=bidb
            ask=askb
            print(6)
            key=False
        elif value_b > exchange.get_positions()[STOCK_B_ID]*exchange.get_last_price_book(STOCK_B_ID).bids[0].price and (exchange.get_positions()[STOCK_A_ID] + exchange.get_positions()[STOCK_B_ID]) > -1 :
            side = 'ask'
            stock_id = STOCK_B_ID
            bid=bidb
            ask=askb
            print(7)
            key=False
                
        elif value_a==0 and value_b==0:
            if exchange.get_positions()[STOCK_A_ID]*exchange.get_last_price_book(STOCK_A_ID).bids[0].price > exchange.get_positions()[STOCK_B_ID]*exchange.get_last_price_book(STOCK_B_ID).bids[0].price:
                side = 'bid'
                stock_id = STOCK_B_ID
                bid=bidb
                ask=askb
                print(8)
                key=False
            else:
                side = 'bid'
                stock_id = STOCK_A_ID
                bid=bida
                ask=aska
                print(9)
                key=False
            
    print(f'Selected stock {stock_id} to trade.')

    # Obtain order book and only trade if there are both bids and offers available on that stock
    stock_order_book = exchange.get_last_price_book(stock_id)
    if not (stock_order_book and stock_order_book.bids and stock_order_book.asks):
        print(f'Order book for {stock_id} does not have bids or offers. Skipping iteration.')
        continue

    # Obtain best bid and ask prices from order book
    best_bid_price = stock_order_book.bids[0].price
    best_ask_price = stock_order_book.asks[0].price
    print(f'Top level prices for {stock_id}: {best_bid_price:.2f} :: {best_ask_price:.2f}')

    if stock_id == STOCK_A_ID:
        print(13)
        if side == 'bid':
            price = best_ask_price
            bida = price
            print(14)
        else:
            price = best_bid_price
            aska = price
            print(15)
    if stock_id == STOCK_B_ID:
        print(16)
        if side == 'bid':
            price = best_ask_price
            bidb = price
            print(17)
        else:
            price = best_bid_price
            askb = price
            print(18)

    # Insert an IOC order to trade the opposing top-level, ensure to always keep instrument position below 5 so
    # aggregate position stays below 10.
    volume = 1
    if not trade_would_breach_position_limit(stock_id, volume, side, 5):
        print(f'''Inserting {side} for {stock_id}: {volume:.0f} lot(s) at price {price:.2f}.''')
        exchange.insert_order(
            instrument_id=stock_id,
            price=price,
            volume=volume,
            side=side,
            order_type='ioc')
        j+=1
        print(j,'times IOC')
        if side == "bid":
            spend=price*volume
        else:
            earn=price*volume
    else:
        print(f'''Not inserting {volume:.0f} lot {side} for {stock_id} to avoid position-limit breach.''')
    print(1)
    print(f'\nSleeping for 3 seconds.')
    time.sleep(3)