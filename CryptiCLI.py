import time

def Welcome():
    print("""
        Hi I'm Crypti (V1.0 ALPHA), I will be making you rich today...      
    """)
    time.sleep(1)

# 15 Supported tokens in V1.0 ALPHA, more tokens will be added later
def chooseToken():
    Tokens = ['BTC','ETH','ICP','BCH','UNI','ADA','ETC','LINK','MATIC','XLM','LTC','EOS','FIL','DAI','1INCH']
    print("""
        Please choose a crypto currency from the list below:
        # BTC
        # ETH
        # ICP
        # BCH
        # UNI
        # ADA
        # ETC
        # LINK
        # MATIC
        # XLM
        # LTC
        # EOS
        # FIL
        # DAI
        # 1INCH
    """)

    try:
        Token = input('       -> ').upper()
    except TypeError as e:
        print(f"""
            Error parsing input
            {e}
        """)
        quit()

    if Token in Tokens:
        return Token
    else:
        print("""
            Please choose a token from the list of supported tokens.
        """)
        chooseToken()

# Granularities supported by Coinbase API
def chooseGranularity():
    print("""
        Choose a dataframe for the prediction proccess:
        1. One minute
        2. Five minutes
        3. Fifteen minutes
        4. One hour
        5. Six hours
        6. One day
    """)

    try:
        Granularity = int(input('       -> '))
    except TypeError as e:
        print(f"""
            Error parsing input
            {e}
        """)
        quit()

    switcher = {
        1: 60,
        2: 300,
        3: 900,
        4: 3600,
        5: 21600,
        6: 86400
    }

    if switcher.get(Granularity, 0) == 0:
        print("""
            Please choose a timeframe from the list.
        """)
        chooseGranularity()
    else:
        return switcher.get(Granularity)

def num_of_candles():
    num_of_candles = int(input('Enter the number of candles you want to predict (Recommended [10 to 30]): '))
    return num_of_candles

def testSize():
    testSize = float(input('Enter the testing size you want to use (From 0 to 1, ex. 0.15): '))
    return testSize