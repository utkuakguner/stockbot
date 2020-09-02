import yfinance as yf
from datetime import datetime, timedelta
import pandas as pd
import progressbar
from time import sleep
import math

classes = {
    "BANK": ["ISCTR.IS", "GARAN.IS", "AKBNK.IS", "ICBCT.IS", "YKBNK.IS", "VAKBN.IS", "HALKB.IS", "QNBFB.IS", "TSKB.IS"],
    "FUND": ["ISFIN.IS", "ISGSY.IS", "ISMEN.IS"],
    "AIRLINE": ["THYAO.IS", "PGSUS.IS"],
    "HOLDING": ["DEVA.IS", "DOHOL.IS", "TKFEN.IS", "KCHOL.IS"],
    "INDUSTRY": ["EKIZ.IS", "BTCIM.IS", "SODA.IS", "SISE.IS", "ASUZU.IS", "DOGUB.IS", "TRKCM.IS", "ANACM.IS", "ENJSA.IS"],
    "REALESTATE": ["ISGYO.IS", "TSGYO.IS"],
    "SERVICE": ["CCOLA.IS", "MGROS.IS", "VAKKO.IS", "YATAS.IS", "MAVI.IS", "AYGAZ.IS", "AEFES.IS", "PNSUT.IS"],
    "TECH": ["VESTL.IS", "ARCLK.IS", "ASELS.IS", "VESBE.IS"]
}

options = {
    "year_range": 1,
    "ticker_classes": ["BANK", "FUND", "AIRLINE", "HOLDING", "INDUSTRY", "REALESTATE", "SERVICE", "TECH"],
    "result_length": 20
}

date = datetime.today() - timedelta(days = 365 * options["year_range"])
date.strftime("%Y/%m/%d") 

ratios = []
my_list = []

for cls in options["ticker_classes"]:
    my_list += classes[cls]

print("Fetching results...")

bar = progressbar.ProgressBar(maxval=100, \
    widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
bar.start()
prog = 0

for ticker in my_list:
    obj = yf.Ticker(ticker)
    hist = obj.history(start=date, period="max").values.tolist()
    close_prices = []
    for x in hist:
        close_prices.append(x[3])
    max_price = max(close_prices)
    current_price = hist[-1][3]
    ratios.append((ticker, max_price / current_price))
    prog += 100 / len(my_list)
    bar.update(prog)

ratios.sort(key=lambda x: x[1], reverse=True)
ratios = sorted(ratios, key=lambda x: x[1], reverse=True)
bar.finish()

print("\nListing first " + str(options["result_length"]) + " results:\n-------------------------")
print(pd.DataFrame(ratios[:options["result_length"]], columns=["SYMBOL", "RATIO(m/c)"], index=range(1, options["result_length"] + 1)))


