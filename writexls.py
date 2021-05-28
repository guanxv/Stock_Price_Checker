import pandas as pd
import openpyxl

def wrtxls(fund_list):

    df = pd.DataFrame(columns = ['Date', 'temp'])

    for fund in fund_list:
        df1 = pd.read_csv(fund + ".csv", names = ['Date', fund])
        df = pd.merge(df1, df, left_on = 'Date', right_on = 'Date', how = 'outer')

    df = df.drop(columns = 'temp').set_index('Date').fillna(0).sort_values(by = ["Date"], ascending = False)

    with pd.ExcelWriter('FundData.xlsx') as writer:
        df.to_excel(writer, sheet_name='Fund_data')

    print (df)



