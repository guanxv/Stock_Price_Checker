from get_stock_data import *
from writexls import *
import time



fund_list = [
    "180012",
    "162605",
    "570001",
    "110011",
    "160213",
    "003095",
    "164906",
    "161121",
    "486002",
    "163406",
    "006328"
]

for fund in fund_list:
    get_networth(fund)
    print(fund)
    time.sleep(10)

wrtxls(fund_list)






    

