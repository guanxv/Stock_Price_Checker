import pandas as pd

columns = [
    "Type",
    "Name",
    "DateStr",
    "Amount",
    "Unit",
    "NetWorth",
    "Fees",
    "OrderNumber",
]
data = [
    ["已有份额", "银华富裕主题混合", "2021-04-20 11:04:15", 136.63, 20.99, 0, 0, "NA"],
    ["已有份额", "景顺长城鼎益混合（LOF）", "2021-04-20 11:04:15", 137.65, 42.59, 0, 0, "NA"],
    ["已有份额", "诺德价值优势混合", "2021-04-20 11:04:15", 200, 60.6, 0, 0.3, "NA"],
    ["已有份额", "易方达中小盘混合", "2021-04-20 11:04:15", 238.64, 29.69, 0, 0, "NA"],
    ["已有份额", "交银海外中国互联网指数", "2021-04-20 11:04:15", 2401.52, 1238.32, 0, 0, "NA"],
    ["已有份额", "国泰纳斯达克100指数（QDII）", "2021-04-20 11:04:15", 1718.12, 316.18, 0, 0, "NA"],
]

df_before2020apr = pd.DataFrame(data, columns=columns)


df_before2020apr['NetWorth'] = (df_before2020apr['Amount'] - df_before2020apr['Fees'])/df_before2020apr['Unit']

# print(df_before2020apr[['Name','NetWorth']] )