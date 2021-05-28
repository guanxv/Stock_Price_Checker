import requests
import json
from datetime import datetime
from datetime import timedelta
import csv


def get_networth(fund_code):
    
    source = requests.get(
        "http://fund.eastmoney.com/pingzhongdata/" + fund_code + ".js"
    ).text

    # read the data from local drive instead of online, for code development only.
    # with open(fund_code+".data", "r") as stock_file:
    #     source = stock_file.read()
        

    # generate local data for code development purpurse. 
    # with open(fund_code+".data", "w") as stock_file:
    #     stock_file.write(source)

    source = source.split(";")
    netWorth = ""

    for item in source:
        if "Data_netWorthTrend" in item:
            netWorth = item

    netWorth = netWorth.split("[")[1]
    netWorth = netWorth.strip("]")
    netWorth = netWorth.replace("},{", "};{")
    netWorth = netWorth.split(";")

    netWorthDict = {}

    delta = timedelta(hours=12)

    for item in netWorth:
        python_dict = json.loads(item)
        ts = python_dict["x"] / 1000

        timestamp = (datetime.utcfromtimestamp(ts) + delta).strftime("%Y-%m-%d")
        netWorthDict[timestamp] = python_dict["y"]

    # print(netWorthDict)

    with open(fund_code + ".csv", "w") as f:
        for key in netWorthDict.keys():
            # print(key, netWorthDict[key])
            f.write("%s,%s\n" % (key, netWorthDict[key]))


