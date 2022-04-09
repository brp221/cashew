library(fmpcloudr)
# Set API Token
# The default setting will buffer requests so that no more than 10 requests are made every second
fmpc_set_token('ce687b3fe0554890e65d6a5e48f601f9')


symbols = c('AAPL', 'SPY')

# Simple moving average
sma = fmpc_security_tech_indic(symbols, indicator = 'SMA', freq = 'daily', period = 10)

# Exponential moving average
ema = fmpc_security_tech_indic(symbols, indicator = 'EMA',  freq = '1min', period = 10)

# Weighted Moving Average
wma = fmpc_security_tech_indic(symbols, indicator = 'WMA', freq = '5min', period = 10)

# Double Exponential moving average
dema = fmpc_security_tech_indic(symbols, indicator = 'dema', freq = '30min', period = 10)

# Triple Exponential moving average
tema = fmpc_security_tech_indic(symbols, indicator = 'Tema', freq = '1hour', period = 10)

# Williams momentum
will = fmpc_security_tech_indic(symbols, indicator = 'Williams', freq = '4hour', period = 10)

# Average Directional Moving Index
adx = fmpc_security_tech_indic(symbols, indicator = 'adx', freq = 'daily', period = 10)

# Standard Deviation
sd = fmpc_security_tech_indic(symbols, indicator = 'StandardDeviation', freq = '1hour', period = 10)

# Relative Strength Indicator
rsi = fmpc_security_tech_indic(symbols, indicator = 'rsi', freq = 'daily', period = 14)