import datetime as dt
import time
import logging
import numpy as np
import math
import csv
# Import libraries
from optibook.synchronous_client import Exchange
# Use vega value
from math import floor, ceil
from black_scholes import call_value, put_value, call_delta, put_delta, call_vega
from libs import calculate_current_time_to_date

exchange = Exchange()
exchange.connect()
# Login
logging.getLogger('client').setLevel('ERROR')

# Variable setting
# Stock id list
STOCK_ID = ['BAYER','SANTANDER','ING']
# Option id list (call and put included)
OPTIONS_ID=['BAYER50','BAYER75','BAYER100','SAN40','SAN50','SAN60','ING15','ING20','ING25']
# Option id list (call and put separated)
options_ID=['BAY-2022_03_18-050C', 'BAY-2022_03_18-050P', 'BAY-2022_03_18-075C', 'BAY-2022_03_18-075P', 'BAY-2022_03_18-100C', 'BAY-2022_03_18-100P',
'SAN-2022_03_18-040C','SAN-2022_03_18-040P','SAN-2022_03_18-050C','SAN-2022_03_18-050P','SAN-2022_03_18-060C','SAN-2022_03_18-060P',
 'ING-2022_03_18-015C','ING-2022_03_18-015P','ING-2022_03_18-020C','ING-2022_03_18-020P','ING-2022_03_18-025C','ING-2022_03_18-025P']
# Specific option dictionaries 
OPTIONS = [
    {'id': 'BAY-2022_03_18-050C', 'expiry_date': dt.datetime(2022, 3, 18, 12, 0, 0), 'strike': 50, 'callput': 'call'},
    {'id': 'BAY-2022_03_18-050P', 'expiry_date': dt.datetime(2022, 3, 18, 12, 0, 0), 'strike': 50, 'callput': 'put'},
    {'id': 'BAY-2022_03_18-075C', 'expiry_date': dt.datetime(2022, 3, 18, 12, 0, 0), 'strike': 75, 'callput': 'call'},
    {'id': 'BAY-2022_03_18-075P', 'expiry_date': dt.datetime(2022, 3, 18, 12, 0, 0), 'strike': 75, 'callput': 'put'},
    {'id': 'BAY-2022_03_18-100C', 'expiry_date': dt.datetime(2022, 3, 18, 12, 0, 0), 'strike': 100, 'callput': 'call'},
    {'id': 'BAY-2022_03_18-100P', 'expiry_date': dt.datetime(2022, 3, 18, 12, 0, 0), 'strike': 100, 'callput': 'put'},
    {'id': 'SAN-2022_03_18-040C', 'expiry_date': dt.datetime(2022, 3, 18, 12, 0, 0), 'strike': 40, 'callput': 'call'},
    {'id': 'SAN-2022_03_18-040P', 'expiry_date': dt.datetime(2022, 3, 18, 12, 0, 0), 'strike': 40, 'callput': 'put'},
    {'id': 'SAN-2022_03_18-050C', 'expiry_date': dt.datetime(2022, 3, 18, 12, 0, 0), 'strike': 50, 'callput': 'call'},
    {'id': 'SAN-2022_03_18-050P', 'expiry_date': dt.datetime(2022, 3, 18, 12, 0, 0), 'strike': 50, 'callput': 'put'},
    {'id': 'SAN-2022_03_18-060C', 'expiry_date': dt.datetime(2022, 3, 18, 12, 0, 0), 'strike': 60, 'callput': 'call'},
    {'id': 'SAN-2022_03_18-060P', 'expiry_date': dt.datetime(2022, 3, 18, 12, 0, 0), 'strike': 60, 'callput': 'put'},
    {'id': 'ING-2022_03_18-015C', 'expiry_date': dt.datetime(2022, 3, 18, 12, 0, 0), 'strike': 15, 'callput': 'call'},
    {'id': 'ING-2022_03_18-015P', 'expiry_date': dt.datetime(2022, 3, 18, 12, 0, 0), 'strike': 15, 'callput': 'put'},
    {'id': 'ING-2022_03_18-020C', 'expiry_date': dt.datetime(2022, 3, 18, 12, 0, 0), 'strike': 20, 'callput': 'call'},
    {'id': 'ING-2022_03_18-020P', 'expiry_date': dt.datetime(2022, 3, 18, 12, 0, 0), 'strike': 20, 'callput': 'put'},
    {'id': 'ING-2022_03_18-025C', 'expiry_date': dt.datetime(2022, 3, 18, 12, 0, 0), 'strike': 25, 'callput': 'call'},
    {'id': 'ING-2022_03_18-025P', 'expiry_date': dt.datetime(2022, 3, 18, 12, 0, 0), 'strike': 25, 'callput': 'put'},
]

# Set the variables before loop
# To save stock bid price
saved_bid={ 'BAYER': 0, 'SANTANDER': 0, 'ING': 0 }
# To save option bid price
saved_bid_opt={ 'BAY-2022_03_18-050C' : 0, 'BAY-2022_03_18-050P' : 0, 'BAY-2022_03_18-075C' : 0, 'BAY-2022_03_18-075P' : 0, 
    'BAY-2022_03_18-100C' : 0, 'BAY-2022_03_18-100P' : 0, 'SAN-2022_03_18-040C' : 0, 'SAN-2022_03_18-040P' : 0, 
    'SAN-2022_03_18-050C' : 0, 'SAN-2022_03_18-050P' : 0, 'SAN-2022_03_18-060C' : 0, 'SAN-2022_03_18-060P' : 0,
    'ING-2022_03_18-015C' : 0, 'ING-2022_03_18-015P' : 0, 'ING-2022_03_18-020C' : 0, 'ING-2022_03_18-020P' : 0,
    'ING-2022_03_18-025C' : 0, 'ING-2022_03_18-025P' : 0 }
# To save call option value save
bs_val_save={ 'BAYER50' : 0, 'BAYER75' : 0, 'BAYER100' : 0, 'SAN40' : 0, 'SAN50' : 0, 'SAN60' : 0, 'ING15' : 0, 'ING20' : 0, 'ING25' : 0 }
# To save put option value save
bs_val_save2={ 'BAYER50' : 0, 'BAYER75' : 0, 'BAYER100' : 0, 'SAN40' : 0, 'SAN50' : 0, 'SAN60' : 0, 'ING15' : 0, 'ING20' : 0, 'ING25' : 0 }
# To find
bs_val_checker={ 'BAYER50' : 0, 'BAYER75' : 0, 'BAYER100' : 0, 'SAN40' : 0, 'SAN50' : 0, 'SAN60' : 0, 'ING15' : 0, 'ING20' : 0, 'ING25' : 0 }
bs_val_checker2={ 'BAYER50' : 0, 'BAYER75' : 0, 'BAYER100' : 0, 'SAN40' : 0, 'SAN50' : 0, 'SAN60' : 0, 'ING15' : 0, 'ING20' : 0, 'ING25' : 0 }

# Save datas in local
def save(dic1,dic2,dic3):
    # Save option prices to csv
    with open('optionprice.csv', 'a', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames = options_ID)
        writer.writeheader()
        writer.writerow(dic1)
    # Save calculated option prices to csv
    with open('blackscholes.csv', 'a', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames = OPTIONS_ID)
        writer.writeheader()
        writer.writerow(dic2)
    # save delta value to csv
    with open('delta.csv', 'a', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames = OPTIONS_ID)
        writer.writeheader()
        writer.writerow(dic3)

        return print('saved')

# Stock market value save
def stock_prices():
    # Stock prices dictionary setting
    stock_price_bid={ 'BAYER': 0, 'SANTANDER': 0, 'ING': 0 }
    stock_price_ask={ 'BAYER': 0, 'SANTANDER': 0, 'ING': 0 }
    # Get the best price of stocks
    stock_price_bid['BAYER']=round(exchange.get_last_price_book('BAYER').bids[0].price,4)
    stock_price_ask['BAYER']=round(exchange.get_last_price_book('BAYER').asks[0].price,4)
    stock_price_bid['SANTANDER']=round(exchange.get_last_price_book('SANTANDER').bids[0].price,4)
    stock_price_ask['SANTANDER']=round(exchange.get_last_price_book('SANTANDER').asks[0].price,4)
    stock_price_bid['ING']=round(exchange.get_last_price_book('ING').bids[0].price,4)
    stock_price_ask['ING']=round(exchange.get_last_price_book('ING').asks[0].price,4)
        

    return (stock_price_bid, stock_price_ask)

# Option market value save
def option_prices():
    # Option price dictionary setting
    option_price_bid={ 'BAY-2022_03_18-050C' : 0, 'BAY-2022_03_18-050P' : 0, 'BAY-2022_03_18-075C' : 0, 'BAY-2022_03_18-075P' : 0, 
    'BAY-2022_03_18-100C' : 0, 'BAY-2022_03_18-100P' : 0, 'SAN-2022_03_18-040C' : 0, 'SAN-2022_03_18-040P' : 0, 
    'SAN-2022_03_18-050C' : 0, 'SAN-2022_03_18-050P' : 0, 'SAN-2022_03_18-060C' : 0, 'SAN-2022_03_18-060P' : 0,
    'ING-2022_03_18-015C' : 0, 'ING-2022_03_18-015P' : 0, 'ING-2022_03_18-020C' : 0, 'ING-2022_03_18-020P' : 0,
    'ING-2022_03_18-025C' : 0, 'ING-2022_03_18-025P' : 0 }
    option_price_ask={ 'BAY-2022_03_18-050C' : 0, 'BAY-2022_03_18-050P' : 0, 'BAY-2022_03_18-075C' : 0, 'BAY-2022_03_18-075P' : 0, 
    'BAY-2022_03_18-100C' : 0, 'BAY-2022_03_18-100P' : 0, 'SAN-2022_03_18-040C' : 0, 'SAN-2022_03_18-040P' : 0, 
    'SAN-2022_03_18-050C' : 0, 'SAN-2022_03_18-050P' : 0, 'SAN-2022_03_18-060C' : 0, 'SAN-2022_03_18-060P' : 0,
    'ING-2022_03_18-015C' : 0, 'ING-2022_03_18-015P' : 0, 'ING-2022_03_18-020C' : 0, 'ING-2022_03_18-020P' : 0,
    'ING-2022_03_18-025C' : 0, 'ING-2022_03_18-025P' : 0 }
    # Get the best value of options (in the simulation, getting price process sometimes occurs error with bid and ask refresh speed so store values manually not usinf for loop)
    option_price_bid['BAY-2022_03_18-050C']=round(exchange.get_last_price_book('BAY-2022_03_18-050C').bids[0].price,4)
    option_price_ask['BAY-2022_03_18-050C']=round(exchange.get_last_price_book('BAY-2022_03_18-050C').asks[0].price,4)
    option_price_bid['BAY-2022_03_18-050P']=round(exchange.get_last_price_book('BAY-2022_03_18-050P').bids[0].price,4)
    option_price_ask['BAY-2022_03_18-050P']=round(exchange.get_last_price_book('BAY-2022_03_18-050P').asks[0].price,4)
    option_price_bid['BAY-2022_03_18-075C']=round(exchange.get_last_price_book('BAY-2022_03_18-075C').bids[0].price,4)
    option_price_ask['BAY-2022_03_18-075C']=round(exchange.get_last_price_book('BAY-2022_03_18-075C').asks[0].price,4)
    option_price_bid['BAY-2022_03_18-075P']=round(exchange.get_last_price_book('BAY-2022_03_18-075P').bids[0].price,4)
    option_price_ask['BAY-2022_03_18-075P']=round(exchange.get_last_price_book('BAY-2022_03_18-075P').asks[0].price,4)
    option_price_bid['BAY-2022_03_18-100C']=round(exchange.get_last_price_book('BAY-2022_03_18-100C').bids[0].price,4)
    option_price_ask['BAY-2022_03_18-100C']=round(exchange.get_last_price_book('BAY-2022_03_18-100C').asks[0].price,4)
    option_price_bid['BAY-2022_03_18-100P']=round(exchange.get_last_price_book('BAY-2022_03_18-100P').bids[0].price,4)
    option_price_ask['BAY-2022_03_18-100P']=round(exchange.get_last_price_book('BAY-2022_03_18-100P').asks[0].price,4)
    # Get the best value of options     
    option_price_bid['SAN-2022_03_18-040C']=round(exchange.get_last_price_book('SAN-2022_03_18-040C').bids[0].price,4)
    option_price_ask['SAN-2022_03_18-040C']=round(exchange.get_last_price_book('SAN-2022_03_18-040C').asks[0].price,4)
    option_price_bid['SAN-2022_03_18-040P']=round(exchange.get_last_price_book('SAN-2022_03_18-040P').bids[0].price,4)
    option_price_ask['SAN-2022_03_18-040P']=round(exchange.get_last_price_book('SAN-2022_03_18-040P').asks[0].price,4)
    option_price_bid['SAN-2022_03_18-050C']=round(exchange.get_last_price_book('SAN-2022_03_18-050C').bids[0].price,4)
    option_price_ask['SAN-2022_03_18-050C']=round(exchange.get_last_price_book('SAN-2022_03_18-050C').asks[0].price,4)
    option_price_bid['SAN-2022_03_18-050P']=round(exchange.get_last_price_book('SAN-2022_03_18-050P').bids[0].price,4)
    option_price_ask['SAN-2022_03_18-050P']=round(exchange.get_last_price_book('SAN-2022_03_18-050P').asks[0].price,4)
    option_price_bid['SAN-2022_03_18-060C']=round(exchange.get_last_price_book('SAN-2022_03_18-060C').bids[0].price,4)
    option_price_ask['SAN-2022_03_18-060C']=round(exchange.get_last_price_book('SAN-2022_03_18-060C').asks[0].price,4)
    option_price_bid['SAN-2022_03_18-060P']=round(exchange.get_last_price_book('SAN-2022_03_18-060P').bids[0].price,4)
    option_price_ask['SAN-2022_03_18-060P']=round(exchange.get_last_price_book('SAN-2022_03_18-060P').asks[0].price,4)
    # Get the best value of options
    option_price_bid['ING-2022_03_18-015C']=round(exchange.get_last_price_book('ING-2022_03_18-015C').bids[0].price,4)
    option_price_ask['ING-2022_03_18-015C']=round(exchange.get_last_price_book('ING-2022_03_18-015C').asks[0].price,4)
    option_price_bid['ING-2022_03_18-015P']=round(exchange.get_last_price_book('ING-2022_03_18-015P').bids[0].price,4)
    option_price_ask['ING-2022_03_18-015P']=round(exchange.get_last_price_book('ING-2022_03_18-015P').asks[0].price,4)
    option_price_bid['ING-2022_03_18-020C']=round(exchange.get_last_price_book('ING-2022_03_18-020C').bids[0].price,4)
    option_price_ask['ING-2022_03_18-020C']=round(exchange.get_last_price_book('ING-2022_03_18-020C').asks[0].price,4)
    option_price_bid['ING-2022_03_18-020P']=round(exchange.get_last_price_book('ING-2022_03_18-020P').bids[0].price,4)
    option_price_ask['ING-2022_03_18-020P']=round(exchange.get_last_price_book('ING-2022_03_18-020P').asks[0].price,4)
    option_price_bid['ING-2022_03_18-025C']=round(exchange.get_last_price_book('ING-2022_03_18-025C').bids[0].price,4)
    option_price_ask['ING-2022_03_18-025C']=round(exchange.get_last_price_book('ING-2022_03_18-025C').asks[0].price,4)
    option_price_bid['ING-2022_03_18-025P']=round(exchange.get_last_price_book('ING-2022_03_18-025P').bids[0].price,4)
    option_price_ask['ING-2022_03_18-025P']=round(exchange.get_last_price_book('ING-2022_03_18-025P').asks[0].price,4)

    return (option_price_bid, option_price_ask)
    
# Average stock value save
def stock_values():
    # Average stock value saving dictionary (for calculating Black-scholes equation)
    stock_value={ 'BAYER': 0, 'SANTANDER': 0, 'ING': 0 }
    # Get the value of bid and ask and divide by 2
    stock_value['BAYER']=(exchange.get_last_price_book('BAYER').bids[0].price + exchange.get_last_price_book('BAYER').asks[0].price)/2
    stock_value['SANTANDER']=(exchange.get_last_price_book('SANTANDER').bids[0].price + exchange.get_last_price_book('SANTANDER').asks[0].price)/2
    stock_value['ING']=(exchange.get_last_price_book('ING').bids[0].price + exchange.get_last_price_book('ING').asks[0].price)/2
    
    return stock_value

# Average call option value save
def option_values():
    # Set the option value dictionary
    option_call_value={ 'BAYER50' : 0, 'BAYER75' : 0, 'BAYER100' : 0, 'SAN40' : 0, 'SAN50' : 0, 'SAN60' : 0, 'ING15' : 0, 'ING20' : 0, 'ING25' : 0 }
    # Set the call and put option keys list
    opt=[]
    for i in OPTIONS:
        # Append key list of options
        opt.append(i['id'])
    # calculate averaged call option value (to claclulate implied volatility)
    for i in range(0,9):
        option_call_value[OPTIONS_ID[i]]=(option_prices()[0][opt[2*i]] + option_prices()[1][opt[2*i]])/2

    return option_call_value

# Calculated call option value
def black_scholes_value():
    # Set the option value dictionary
    bs_cal={ 'BAYER50' : 0, 'BAYER75' : 0, 'BAYER100' : 0, 'SAN40' : 0, 'SAN50' : 0, 'SAN60' : 0, 'ING15' : 0, 'ING20' : 0, 'ING25' : 0 }
    # Strike price of BAYER stock option
    Strike1=[50,75,100]
    # Strike price of SANTANDER stock option
    Strike2=[40,50,60]
    # Strike price of ING stock option
    Strike3=[15,20,25]
    # Set variables for smallest different with stock price and strike
    implied_strike=[]
    # Calculate BAYER strike
    temp1=[]
    for i in Strike1:
        temp1.append(abs(stock_values()['BAYER']-i))
    implied_strike.append(Strike1[temp1.index(min(temp1))])
    # Calculate SANTANDER strike
    temp2=[]
    for i in Strike2:
        temp2.append(abs(stock_values()['SANTANDER']-i))
    implied_strike.append(Strike2[temp2.index(min(temp2))])
    # calculate ING strike
    temp3=[]
    for i in Strike3:
        temp3.append(abs(stock_values()['ING']-i))
    implied_strike.append(Strike3[temp3.index(min(temp3))])
    # Divide 3 part to calculate stock value in Black-Scholes equation easily
    for j in range(0,3):
        # Calculate Black-Scholes equation for BAYER options with implied volatility of strike price 75(most closest value to stock price)
        bs_cal[OPTIONS_ID[j]]=call_value(stock_values()[STOCK_ID[int(j/3)]], Strike1[j], calculate_current_time_to_date(dt.datetime(2022, 3, 18, 12, 0, 0)), 0
        ,implied_vol(stock_values()[STOCK_ID[int(j/3)]], implied_strike[0], calculate_current_time_to_date(dt.datetime(2022, 3, 18, 12, 0, 0)), 0, option_values()[OPTIONS_ID[j]]))
    for j in range(3,6):
        # Calculate Black-Scholes equation for SANTANDER options with implied volatility of strike price 50(most closest value to stock price)
        bs_cal[OPTIONS_ID[j]]=call_value(stock_values()[STOCK_ID[int(j/3)]], Strike2[j-3], calculate_current_time_to_date(dt.datetime(2022, 3, 18, 12, 0, 0)), 0
        ,implied_vol(stock_values()[STOCK_ID[int(j/3)]], implied_strike[1], calculate_current_time_to_date(dt.datetime(2022, 3, 18, 12, 0, 0)), 0, option_values()[OPTIONS_ID[j]]))
    for j in range(6,9):
        # Calculate Black-Scholes equation for ING options with implied volatility of strike price 15(most closest value to stock price)
        bs_cal[OPTIONS_ID[j]]=call_value(stock_values()[STOCK_ID[int(j/3)]], Strike3[j-6], calculate_current_time_to_date(dt.datetime(2022, 3, 18, 12, 0, 0)), 0
        ,implied_vol(stock_values()[STOCK_ID[int(j/3)]], implied_strike[2], calculate_current_time_to_date(dt.datetime(2022, 3, 18, 12, 0, 0)), 0, option_values()[OPTIONS_ID[j]]))
        
    return bs_cal

# Calculate call delta value    
def delta():
    # Set the call delta dictionary
    delta={ 'BAYER50' : 0, 'BAYER75' : 0, 'BAYER100' : 0, 'SAN40' : 0, 'SAN50' : 0, 'SAN60' : 0, 'ING15' : 0, 'ING20' : 0, 'ING25' : 0 }
    # Divide 3 part to calculate stock value in Delta easily
    for j in range(0,3):
        # Strike price of BAYER stock option
        Strike=[50,75,100]
        # Calculate call delta for BAYER options with implied volatility of strike price 75(most closest value to stock price)
        delta[OPTIONS_ID[j]]=call_delta(stock_values()[STOCK_ID[int(j/3)]], Strike[j], calculate_current_time_to_date(dt.datetime(2022, 3, 18, 12, 0, 0)), 0
        ,implied_vol(stock_values()[STOCK_ID[int(j/3)]], 75, calculate_current_time_to_date(dt.datetime(2022, 3, 18, 12, 0, 0)), 0, option_values()[OPTIONS_ID[j]]))
    for j in range(3,6):
        # Strike price of SANTANDER stock option
        Strike=[40,50,60]
        # Calculate call delta for SANTANDER options with implied volatility of strike price 50(most closest value to stock price)
        delta[OPTIONS_ID[j]]=call_delta(stock_values()[STOCK_ID[int(j/3)]], Strike[j-3], calculate_current_time_to_date(dt.datetime(2022, 3, 18, 12, 0, 0)), 0
        ,implied_vol(stock_values()[STOCK_ID[int(j/3)]], 50, calculate_current_time_to_date(dt.datetime(2022, 3, 18, 12, 0, 0)), 0, option_values()[OPTIONS_ID[j]]))
    for j in range(6,9):
        # Strike price of ING stock option
        Strike=[15,20,25]
        # Calculate call delta for ING options with implied volatility of strike price 15(most closest value to stock price)
        delta[OPTIONS_ID[j]]=call_delta(stock_values()[STOCK_ID[int(j/3)]], Strike[j-6], calculate_current_time_to_date(dt.datetime(2022, 3, 18, 12, 0, 0)), 0
        ,implied_vol(stock_values()[STOCK_ID[int(j/3)]], 15, calculate_current_time_to_date(dt.datetime(2022, 3, 18, 12, 0, 0)), 0, option_values()[OPTIONS_ID[j]]))

    return delta
    
# Calculate put option with put-call parity
def pc_parity_put():
    # Set the put option dictionary
    put_cal = { 'BAYER50' : 0, 'BAYER75' : 0, 'BAYER100' : 0, 'SAN40' : 0, 'SAN50' : 0, 'SAN60' : 0, 'ING15' : 0, 'ING20' : 0, 'ING25' : 0 }
    # Strike values
    strike=[50,75,100,40,50,60,15,20,25]
    # call premium + strike price = put premium + stock value
    for i in range(len(strike)):
        # Find the Put value with Put-Call parity (r=0)
        put_cal[OPTIONS_ID[i]] = black_scholes_value()[OPTIONS_ID[i]] + strike[i] - stock_values()[STOCK_ID[int(i/3)]]
    
    return put_cal

# Calculate Implied volatility
def implied_vol(S, K, T, r, market_value):
    # Iteration number for Newton raphson method
    MAX_ITERATIONS = 100
    # Set the minimum convergence value
    PRECISION = 2.0e-7
    # Initial sigma(volatility)(set more than 0.5)
    sigma = 0.8
    # Run Newton raphson method to find new sigma
    for i in range(0, MAX_ITERATIONS):
        # Call option value
        price = call_value(S, K, T, r, sigma)
        # Vega call value
        vega = call_vega(S, K, T, r, sigma)
        # Difference between market value and calculated value
        diff = market_value - price
        # Set range of convergence
        if (abs(diff) < PRECISION):
            return sigma
        # New sigma
        sigma = sigma + diff/vega
    return sigma

# Call option trading with delta hedging
def call_option_trading():
    # Call option trading
    volume=10
    # NaN value eliminator if there are NaN values (with different strike value it is possible)
    #for i in OPTIONS_ID:
    #    if np.isnan(black_scholes_value()[i]):
    #        bs_val_checker[i]=0
    #    else:
    #        bs_val_checker[i]=black_scholes_value()[i]
        #print('i in nan eli')
        #print(i)
    # Call bidding
    for i in range(len(OPTIONS_ID)):
        # If the calculated option price is higher than market price buy call option positions before 300 position
        if black_scholes_value()[OPTIONS_ID[i]] > option_prices()[0][options_ID[i*2]] and exchange.get_positions()[options_ID[i*2]] < 300:
            # Print status
            print(f'''Inserting {'bid'} for {options_ID[i*2]}: {volume:.0f} lot(s) at price {option_prices()[0][options_ID[i*2]]:.2f}.''')
            # Bidding with limited order
            exchange.insert_order(instrument_id=options_ID[i*2], price=round(float(option_prices()[0][options_ID[i*2]]),2),volume=volume, side='bid', order_type='limit')
            # Save the bidding price to new dictionary
            bs_val_save[OPTIONS_ID[i]]=option_prices()[0][options_ID[i*2]]
            # print status of delta neutralize asking status
            print(f'''Inserting {'ask'} for {STOCK_ID[int(i/3)]}: {math.ceil(delta()[OPTIONS_ID[i]]*10):.0f} lot(s) at price {stock_prices()[0][STOCK_ID[int(i/3)]]:.2f}.''')
            # Asking the position with amount of delta in limited order
            exchange.insert_order(instrument_id=STOCK_ID[int(i/3)], price=round(float(stock_prices()[0][STOCK_ID[int(i/3)]]),2),volume=round(delta()[OPTIONS_ID[i]]*10), side='ask', order_type='limit')
        else:
            print('not order')
    
    # Call asking
    for i in range(len(OPTIONS_ID)):
        # If the existing value is too big change position volume
        if exchange.get_positions()[options_ID[i]] >= 200:
            volume=100
        # If the market value is bigger than saved call option value which bidded before and if there have saved value and position it insert
        if bs_val_save2[OPTIONS_ID[i]] < option_prices()[1][options_ID[i*2]] and bs_val_save[OPTIONS_ID[i]] > 0 and exchange.get_positions()[options_ID[i*2]] > 0:
            # Print status
            print(f'''Inserting {'ask'} for {options_ID[i*2]}: {volume:.0f} lot(s) at price {option_prices()[1][options_ID[i*2]]:.2f}.''')
            # Insert asking order with limitied type
            exchange.insert_order(instrument_id=options_ID[i], price=round(float(option_prices()[1][options_ID[i*2]]),2),volume=volume, side='ask', order_type='limit')
            # print delta neutralize bidding status
            print(f'''Inserting {'bid'} for {STOCK_ID[int(i/3)]}: {math.ceil(delta()[OPTIONS_ID[i]]*10):.0f} lot(s) at price {stock_prices()[0][STOCK_ID[int(i/3)]]:.2f}.''')
            # Bidding the position with amount of delta in limited order
            exchange.insert_order(instrument_id=STOCK_ID[int(i/3)], price=round(float(stock_prices()[0][STOCK_ID[int(i/3)]]),2),volume=round(delta()[OPTIONS_ID[i]]*10), side='bid', order_type='limit')
        else:
            print('not order')
            

    return print('run')

# Put option trading with delta hedging
def put_option_trading():
    # Put option trading
    volume=10
    # NaN value eliminator if strike value is different
    #for i in OPTIONS_ID:
    #    if np.isnan(pc_parity_put()[i]):
    #        bs_val_checker2[i]=0
    #    else:
    #        bs_val_checker2[i]=pc_parity_put()[i]
    # Put bidding
    for i in range(len(OPTIONS_ID)):
        # If the calculated put value is bigger than market value, bidding position before position 300
        if pc_parity_put()[OPTIONS_ID[i]] > option_prices()[0][options_ID[i*2+1]] and exchange.get_positions()[options_ID[i*2+1]] < 300:
            # Print status
            print(f'''Inserting {'bid'} for {options_ID[i*2+1]}: {volume:.0f} lot(s) at price {option_prices()[0][options_ID[i*2+1]]:.2f}.''')
            # Insert bidding of put option with limitied order
            exchange.insert_order(instrument_id=options_ID[i*2+1], price=round(float(option_prices()[0][options_ID[i*2+1]]),2),volume=volume, side='bid', order_type='limit')
            # Print delta neutralize status
            print(f'''Inserting {'bid'} for {STOCK_ID[int(i/3)]}: {math.ceil(delta()[OPTIONS_ID[i]]*10):.0f} lot(s) at price {stock_prices()[0][STOCK_ID[int(i/3)]]:.2f}.''')
            # Bidding stock with delta amount position
            exchange.insert_order(instrument_id=STOCK_ID[int(i/3)], price=round(float(stock_prices()[0][STOCK_ID[int(i/3)]]),2),volume=round(delta()[OPTIONS_ID[i]]*10), side='bid', order_type='limit')
            # Save the bidding value
            bs_val_save2[OPTIONS_ID[i]]=option_prices()[0][options_ID[i*2+1]]
        else:
            print('not order')
    
    # Put asking
    for i in range(len(OPTIONS_ID)):
        # If the position stored over 200, increase the asking volume
        if exchange.get_positions()[options_ID[i]] >= 200:
            volume=100
        # If saved bidding value is cheaper than market prices insert asking and the bidding value is saved and there are positions
        if bs_val_save2[OPTIONS_ID[i]] < option_prices()[1][options_ID[i*2+1]] and bs_val_save2[OPTIONS_ID[i]] > 0 and exchange.get_positions()[options_ID[i*2+1]] > 0:
            # Print status
            print(f'''Inserting {'ask'} for {options_ID[i*2+1]}: {volume:.0f} lot(s) at price {option_prices()[1][options_ID[i*2+1]]:.2f}.''')
            # Asking the put options with limited order
            exchange.insert_order(instrument_id=options_ID[i*2+1], price=round(float(option_prices()[1][options_ID[i*2+1]]),2),volume=volume, side='ask', order_type='limit')
            # Print delta neutralize status
            print(f'''Inserting {'ask'} for {STOCK_ID[int(i/3)]}: {math.ceil(delta()[OPTIONS_ID[i]]*10):.0f} lot(s) at price {stock_prices()[0][STOCK_ID[int(i/3)]]:.2f}.''')
            # Askint the stock position as much as delta value 
            exchange.insert_order(instrument_id=STOCK_ID[int(i/3)], price=round(float(stock_prices()[0][STOCK_ID[int(i/3)]]),2),volume=round(delta()[OPTIONS_ID[i]]*10), side='ask', order_type='limit')
        else:
            print('not order')
            
    return print('run')
    
# Variables for judging iteration
# Find how much iterated with simple trading algorithm
a=0
# Check arbitrage opportunity and order in BAYER 
b=0
c=0
# Check arbitrage opportunity and order in SNATANDER 
d=0
e=0
# Check arbitrage opportunity and order in ING
f=0
g=0

# Start iteration
while True:
    print(f'')
    print(f'-----------------------------------------------------------------')
    print(f'TRADE LOOP ITERATION ENTERED AT {str(dt.datetime.now()):18s} UTC.')
    print(f'-----------------------------------------------------------------')

    #########################################
    #  Implement your main trade loop here  #
    #########################################
    
    # Stock market price save
    stck_bid=stock_prices()[0]
    stck_ask=stock_prices()[1]
    # Cool_time
    time.sleep(5)
    # Delete existing orders
    for option in OPTIONS:
        exchange.delete_orders(option['id'])
    """
    # Arbitrage
    # Arbitrage ratio calculate
    Ba_San_ratio=round(stock_values()['BAYER']/stock_values()['SANTANDER'],3)
    Ba_In_ratio=round(stock_values()['BAYER']/stock_values()['ING'],3)
    San_In_ratio=round(stock_values()['SANTANDER']/stock_values()['ING'],3)
    time.sleep(3)
    # BAYER_SANTANDER Arbitrage
    # Set the limited volume
    volume=5
    # If the bigger stock is bigger than smaller stock with muliply the ratio and position limit until 150
    if stock_values()['BAYER']>stock_values()['SANTANDER']*Ba_San_ratio and b == 0 and exchange.get_positions()['BAYER'] < 50 and exchange.get_positions()['SANTANDER'] < 50:
        # Print status
        print(f'''Inserting {'bid'} for {'BAYER'}: {volume:.0f} lot(s) at price {stock_prices()[0]['BAYER']:.2f}.''')
        # Bidding bigger stock with unit position
        exchange.insert_order(instrument_id='BAYER', price=round(float(stock_prices()[0]['BAYER']),2),volume=volume, side='bid', order_type='limit')
        # Print status
        print(f'''Inserting {'ask'} for {'SANTANDER'}: {math.ceil(volume*Ba_San_ratio):.0f} lot(s) at price {stock_prices()[0]['SANTANDER']:.2f}.''')
        # Asking smaller stock with multiplied unit position and ratio
        exchange.insert_order(instrument_id='SANTANDER', price=round(float(stock_prices()[0]['SANTANDER']),2),volume=math.ceil(volume*Ba_San_ratio), side='ask', order_type='limit')
        # Skip next iteration
        c=1
    # Bidding condition with after iteration
    if stock_values()['BAYER']>stock_values()['SANTANDER']*Ba_San_ratio and b == 1 and exchange.get_positions()['BAYER'] < 50 and exchange.get_positions()['SANTANDER'] < 50:
        # To convert bidding and asking condtion, change unit volume as double
        volume=10
        # print status
        print(f'''Inserting {'bid'} for {'BAYER'}: {volume:.0f} lot(s) at price {stock_prices()[0]['BAYER']:.2f}.''')
        # Insert bidding
        exchange.insert_order(instrument_id='BAYER', price=round(float(stock_prices()[0]['BAYER']),2),volume=volume, side='bid', order_type='limit')
        # Print status
        print(f'''Inserting {'ask'} for {'SANTANDER'}: {math.ceil(volume*Ba_San_ratio):.0f} lot(s) at price {stock_prices()[0]['SANTANDER']:.2f}.''')
        # Insert asking
        exchange.insert_order(instrument_id='SANTANDER', price=round(float(stock_prices()[0]['SANTANDER']),2),volume=math.ceil(volume*Ba_San_ratio), side='ask', order_type='limit')
        # Check this process
        c=1
    # If the bigger stock is smaller than smaller stock with muliply the ratio and position limit until 150 
    if stock_values()['BAYER']<stock_values()['SANTANDER']*Ba_San_ratio and c == 0 and exchange.get_positions()['BAYER'] < 50 and exchange.get_positions()['SANTANDER'] < 50:
        # print status
        print(f'''Inserting {'ask'} for {'BAYER'}: {volume:.0f} lot(s) at price {stock_prices()[0]['BAYER']:.2f}.''')
        # Inset asking
        exchange.insert_order(instrument_id='BAYER', price=round(float(stock_prices()[0]['BAYER']),2),volume=volume, side='ask', order_type='limit')
        # Print status
        print(f'''Inserting {'bid'} for {'SANTANDER'}: {math.ceil(volume*Ba_San_ratio):.0f} lot(s) at price {stock_prices()[0]['SANTANDER']:.2f}.''')
        # Insert bidding
        exchange.insert_order(instrument_id='SANTANDER', price=round(float(stock_prices()[0]['SANTANDER']),2),volume=math.ceil(volume*Ba_San_ratio), side='bid', order_type='limit')
        # Check this iteration
        b=1
    # Asking condition after iteration
    if stock_values()['BAYER']<stock_values()['SANTANDER']*Ba_San_ratio and c == 1 and exchange.get_positions()['BAYER'] < 50 and exchange.get_positions()['SANTANDER'] < 50:
        # To convert bidding and asking condtion, change unit volume as double
        volume=10
        # print status
        print(f'''Inserting {'ask'} for {'BAYER'}: {volume:.0f} lot(s) at price {stock_prices()[0]['BAYER']:.2f}.''')
        # Insert asking
        exchange.insert_order(instrument_id='BAYER', price=round(float(stock_prices()[0]['BAYER']),2),volume=volume, side='ask', order_type='limit')
        # Print status
        print(f'''Inserting {'bid'} for {'SANTANDER'}: {math.ceil(volume*Ba_San_ratio):.0f} lot(s) at price {stock_prices()[0]['SANTANDER']:.2f}.''')
        # Insert bidding
        exchange.insert_order(instrument_id='SANTANDER', price=round(float(stock_prices()[0]['SANTANDER']),2),volume=math.ceil(volume*Ba_San_ratio), side='bid', order_type='limit')
        # Check the iteration
        b=1
            
    volume=10
    # Same conditions with BAYER-SANTANDER arbitrage
    # BAYER_ING Arbitrage
    volume=5
    if stock_values()['BAYER']>stock_values()['ING']*Ba_In_ratio and d == 0 and exchange.get_positions()['BAYER'] < 50 and exchange.get_positions()['ING'] < 50:
        print(f'''Inserting {'bid'} for {'BAYER'}: {volume:.0f} lot(s) at price {stock_prices()[0]['BAYER']:.2f}.''')
        exchange.insert_order(instrument_id='BAYER', price=round(float(stock_prices()[0]['BAYER']),2),volume=volume, side='bid', order_type='limit')
        print(f'''Inserting {'ask'} for {'ING'}: {math.ceil(volume*Ba_In_ratio):.0f} lot(s) at price {stock_prices()[0]['ING']:.2f}.''')
        exchange.insert_order(instrument_id='ING', price=round(float(stock_prices()[0]['ING']),2),volume=math.ceil(volume*Ba_In_ratio), side='ask', order_type='limit')
        e=1
    if stock_values()['BAYER']>stock_values()['ING']*Ba_In_ratio and d == 1 and exchange.get_positions()['BAYER'] < 50 and exchange.get_positions()['ING'] < 50:
        volume=10
        print(f'''Inserting {'bid'} for {'BAYER'}: {volume:.0f} lot(s) at price {stock_prices()[0]['BAYER']:.2f}.''')
        exchange.insert_order(instrument_id='BAYER', price=round(float(stock_prices()[0]['BAYER']),2),volume=volume, side='bid', order_type='limit')
        print(f'''Inserting {'ask'} for {'ING'}: {math.ceil(volume*Ba_San_ratio):.0f} lot(s) at price {stock_prices()[0]['ING']:.2f}.''')
        exchange.insert_order(instrument_id='ING', price=round(float(stock_prices()[0]['ING']),2),volume=math.ceil(volume*Ba_In_ratio), side='ask', order_type='limit')
        e=1
            
    if stock_values()['BAYER']<stock_values()['ING']*Ba_In_ratio and e == 0 and exchange.get_positions()['BAYER'] < 50 and exchange.get_positions()['ING'] < 50:
        print(f'''Inserting {'ask'} for {'BAYER'}: {volume:.0f} lot(s) at price {stock_prices()[0]['BAYER']:.2f}.''')
        exchange.insert_order(instrument_id='BAYER', price=round(float(stock_prices()[0]['BAYER']),2),volume=volume, side='ask', order_type='limit')
        print(f'''Inserting {'bid'} for {'ING'}: {math.ceil(volume*Ba_In_ratio):.0f} lot(s) at price {stock_prices()[0]['ING']:.2f}.''')
        exchange.insert_order(instrument_id='ING', price=round(float(stock_prices()[0]['ING']),2),volume=math.ceil(volume*Ba_In_ratio), side='bid', order_type='limit')
        d=1
    if stock_values()['BAYER']<stock_values()['ING']*Ba_In_ratio and e == 1 and exchange.get_positions()['BAYER'] < 50 and exchange.get_positions()['ING'] < 50:
        volume=10
        print(f'''Inserting {'ask'} for {'BAYER'}: {volume:.0f} lot(s) at price {stock_prices()[0]['BAYER']:.2f}.''')
        exchange.insert_order(instrument_id='BAYER', price=round(float(stock_prices()[0]['BAYER']),2),volume=volume, side='ask', order_type='limit')
        print(f'''Inserting {'bid'} for {'ING'}: {math.ceil(volume*Ba_In_ratio):.0f} lot(s) at price {stock_prices()[0]['ING']:.2f}.''')
        exchange.insert_order(instrument_id='ING', price=round(float(stock_prices()[0]['ING']),2),volume=math.ceil(volume*Ba_In_ratio), side='bid', order_type='limit')
        d=1
            
    volume=10
    
    # SANTANDER_ING Arbitrage
    # Same conditions with BAYER-SANTANDER arbitrage
    volume=5
    if stock_values()['SANTANDER']>stock_values()['ING']*San_In_ratio and f == 0 and exchange.get_positions()['SANTANDER'] < 50 and exchange.get_positions()['ING'] < 50:
        print(f'''Inserting {'bid'} for {'SANTANDER'}: {volume:.0f} lot(s) at price {stock_prices()[0]['SANTANDER']:.2f}.''')
        exchange.insert_order(instrument_id='SANTANDER', price=round(float(stock_prices()[0]['SANTANDER']),2),volume=volume, side='bid', order_type='limit')
        print(f'''Inserting {'ask'} for {'ING'}: {math.ceil(volume*Ba_In_ratio):.0f} lot(s) at price {stock_prices()[0]['ING']:.2f}.''')
        exchange.insert_order(instrument_id='ING', price=round(float(stock_prices()[0]['ING']),2),volume=math.ceil(volume*San_In_ratio), side='ask', order_type='limit')
        g=1
    if stock_values()['SANTANDER']>stock_values()['ING']*San_In_ratio and f == 1 and exchange.get_positions()['SANTANDER'] < 50 and exchange.get_positions()['ING'] < 50:
        volume=10
        print(f'''Inserting {'bid'} for {'SANTANDER'}: {volume:.0f} lot(s) at price {stock_prices()[0]['SANTANDER']:.2f}.''')
        exchange.insert_order(instrument_id='SANTANDER', price=round(float(stock_prices()[0]['SANTANDER']),2),volume=volume, side='bid', order_type='limit')
        print(f'''Inserting {'ask'} for {'ING'}: {math.ceil(volume*Ba_In_ratio):.0f} lot(s) at price {stock_prices()[0]['ING']:.2f}.''')
        exchange.insert_order(instrument_id='ING', price=round(float(stock_prices()[0]['ING']),2),volume=math.ceil(volume*San_In_ratio), side='ask', order_type='limit')
        g=1
            
    if stock_values()['SANTANDER']<stock_values()['ING']*Ba_San_ratio and g == 0 and exchange.get_positions()['SANTANDER'] < 50 and exchange.get_positions()['ING'] < 50:
        print(f'''Inserting {'ask'} for {'SANTANDER'}: {volume:.0f} lot(s) at price {stock_prices()[0]['SANTANDER']:.2f}.''')
        exchange.insert_order(instrument_id='SANTANDER', price=round(float(stock_prices()[0]['SANTANDER']),2),volume=volume, side='ask', order_type='limit')
        print(f'''Inserting {'bid'} for {'ING'}: {math.ceil(volume*Ba_In_ratio):.0f} lot(s) at price {stock_prices()[0]['ING']:.2f}.''')
        exchange.insert_order(instrument_id='ING', price=round(float(stock_prices()[0]['ING']),2),volume=math.ceil(volume*San_In_ratio), side='bid', order_type='limit')
        f=1
    if stock_values()['SANTANDER']<stock_values()['ING']*Ba_San_ratio and g == 1 and exchange.get_positions()['SANTANDER'] < 50 and exchange.get_positions()['ING'] < 50:
        volume=10
        print(f'''Inserting {'ask'} for {'SANTANDER'}: {volume:.0f} lot(s) at price {stock_prices()[0]['SANTANDER']:.2f}.''')
        exchange.insert_order(instrument_id='SANTANDER', price=round(float(stock_prices()[0]['SANTANDER']),2),volume=volume, side='ask', order_type='limit')
        print(f'''Inserting {'bid'} for {'ING'}: {math.ceil(volume*Ba_In_ratio):.0f} lot(s) at price {stock_prices()[0]['ING']:.2f}.''')
        exchange.insert_order(instrument_id='ING', price=round(float(stock_prices()[0]['ING']),2),volume=math.ceil(volume*San_In_ratio), side='bid', order_type='limit')
        f=1
            
    volume=10
    

    # Simple Stock trading
    # Bidding
    # Set volume
    volume=10
    # After 4 iteration condition
    if a > 3 :
        # If the stock getting cheaper more than 3 percent, buy more positions before 300 position
        for i in STOCK_ID:
            if saved_bid[i] > stock_prices()[0][i]*1.03 and exchange.get_positions()[i] < 300:
                # Print status
                print(f'''Inserting {'bid'} for {i}: {volume:.0f} lot(s) at price {stock_prices()[0][i]:.2f}.''')
                # Insert bidding with limited order
                exchange.insert_order(instrument_id=i, price=round(float(stock_prices()[0][i]),2),volume=volume, side='bid', order_type='limit')
                # save the bidding price
                saved_bid[i]=stock_prices()[0][i]
            else:
                print('not order')
    else:
        for i in STOCK_ID:
            # If the first value is expensive than now value bidding in first 4 iterations
            if stck_bid[i] > stock_prices()[0][i] and exchange.get_positions()[i] < 300:
                # Print status
                print(f'''Inserting {'bid'} for {i}: {volume:.0f} lot(s) at price {stock_prices()[0][i]:.2f}.''')
                # Insert bidding
                exchange.insert_order(instrument_id=i, price=round(float(stock_prices()[0][i]),2),volume=volume, side='bid', order_type='limit')
                # Save the bidding value
                saved_bid[i]=stock_prices()[0][i]
            else:
                print('not order')
    
    # Asking
    for i in STOCK_ID:
        # If position stored over 200, increase trading volume
        if exchange.get_positions()[i] >= 200:
            volume=100
        # If market price is higher more than 3 percent than saved bidding price, insert asking
        if saved_bid[i]*1.03 < stock_prices()[1][i] and saved_bid[i] > 0 and exchange.get_positions()[i] > 0:
            # Print status
            print(f'''Inserting {'ask'} for {i}: {volume:.0f} lot(s) at price {stock_prices()[1][i]:.2f}.''')
            # Insert asking
            exchange.insert_order(instrument_id=i, price=round(float(stock_prices()[1][i]),2),volume=volume, side='ask', order_type='limit')
        else:
            print('not order')
    print(a)
    """
    
    # Iteration number for Newton raphson method
    MAX_ITERATIONS = 1000
    # Set the minimum convergence value
    PRECISION = 2.0e-7
    # Initial sigma(volatility)(set more than 0.5)
    sigma = 0.8
    # Run Newton raphson method to find new sigma
    for i in range(0, MAX_ITERATIONS):
        # Call option value
        price = call_value(stock_values()['BAYER'], 75, calculate_current_time_to_date(dt.datetime(2022, 3, 18, 12, 0, 0)), 0, sigma)
        # Vega call value
        vega = call_vega(stock_values()['BAYER'], 75, calculate_current_time_to_date(dt.datetime(2022, 3, 18, 12, 0, 0)), 0, sigma)
        # Difference between market value and calculated value
        diff = option_values()['BAYER75'] - price
        # Set range of convergence
        if (abs(diff) < PRECISION):
            break
        # New sigma
        sigma = sigma + diff/vega
        #print(diff)
        print(sigma)
    
    
    
    
    
    # Calculate iteration number
    a=a+1   
    # Save the option trading results
    save(option_prices()[0],black_scholes_value(),delta())

    # Sleep until next iteration
    print(f'\nSleeping for 5 seconds.')
    time.sleep(5)
