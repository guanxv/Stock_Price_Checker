# --------------解决 VScode output 里中文乱码的问题---------------------
import io
import sys

# 改变标准输出的默认编码
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf8")
# --------------解决 VScode output 里中文乱码的问题---------------------


import pandas as pd
import cv2
import pytesseract


# ----------------数据模型，用来建立，读取，写入数据。于TUI对接。---------------
class StockListModel(object):  # 基金列表
    def __init__(self):

        try:

            # load from disk, once file has been save
            self.load()

        except FileNotFoundError:

            print("Stock.pkl not found! Blank file will be created!")
            self.initBlankdf()

    def initBlankdf(self):

        # initiate the datafram , only need for first run
        columns = ["NameCN", "NameEN", "Code", "Type", "Note"]
        data = [
            ["易方达中小盘混合", "YFDZXPHH", "110011", "混合", "None"],
            ["景顺长城鼎益混合（LOF）", "JSCHDYHH", "162605", "混合", "None"],
            ["银华富裕主题混合", "YHFYZTHH", "180012", "混合", "None"],
            ["诺德价值优势混合", "NDJZYSHH", "570001", "混合", "None"],
            ["兴全合润混合（LOF）", "XQHRHH", "163406", "混合", "None"],
            ["中欧医疗健康混合A", "ZOYLJKHH", "003095", "医疗", "None"],
            ["易方达中证银行指数（LOF）A", "YFDZZYHZS", "161121", "银行", "None"],
            ["工银瑞信全球精选股票（QDII）", "HYRXQQJXGP", "486002", "全球股票", "None"],
            ["国泰纳斯达克100指数（QDII）", "GTNSDK100ZS", "160213", "纳斯达克", "None"],
            ["交银海外中国互联网指数", "JYHWZGHLWZS", "164906", "中概", "None"],
            ["易方达中证海外中国互联网50ETF联接（QDII）C", "YFDZZHWZGHL50ETF", "006328", "中概", "None"],
        ]

        self._df = pd.DataFrame(data, columns=columns)

        # self._df.style.set_properties(**{'text-align': 'left'})

    def show(self):

        print(self._df)

    def save(self):

        self._df.to_pickle("./Investment_Analysis/stock.pkl")

    def load(self):

        self._df = pd.read_pickle("./Investment_Analysis/stock.pkl")


class TradeModel(object):  # 交易记录
    def __init__(self):

        try:

            # load from disk, once file has been save
            self.load()

        except FileNotFoundError:

            print("Trade.pkl not found! Blank file will be created!")
            self.initBlankdf()

    def initBlankdf(self):

        # initiate the datafram , only need for first run
        columns = [
            "Type",
            "Name",
            "Date",
            "Amount",
            "Unit",
            "NetWorth",
            "Fees",
            "OrderNumber",
        ]
        data = [
            ["买入", "景顺长城鼎益混合（LOF）", "2021-06-1 11:04:15", 0, 0, 0, 0, "202100000000"],
        ]

        self._df = pd.DataFrame(data, columns=columns)

    def save(self):

        self._df.to_pickle("./Investment_Analysis/trade.pkl")

    def load(self):

        self._df = pd.read_pickle("./Investment_Analysis/trade.pkl")

    def scanImg(self):

        # 图像识别结果输入数据格式。
        # 交易类型 = ['买入', '卖出', '红利再投资' ,'增强']

        scanResult = {
            "Type": "",  # 交易类型
            "Name": "",  # 基金名称
            "Date": "",  # 操作时间
            "Amount": 0,  # 总金额
            "Unit": 0,  # 确认份额
            "NetWorth": 0,  # 单位净值
            "Fees": 0,  # 手续费
            "OrderNumber": "",  # 订单号
        }

        # -----图像加载，识别部分------
        pytesseract.pytesseract.tesseract_cmd = (
            "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
        )

        img = cv2.imread(
            "C:/Users/Administrator/PycharmProjects/Stock_Price_Checker/Investment_Analysis/IMG-9738.png"
        )  #
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img = cv2.adaptiveThreshold(
            img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 85, 11
        )
        # print (img.shape) check image height and width, img.shape[0] is height, img.shape[1] is width
        img = img[
            50 : img.shape[0], 0 : img.shape[1]
        ]  # crop the image, remove top staus bar

        # cv2.imshow("Result", img)
        # cv2.waitKey(0)

        result = pytesseract.image_to_string(img, lang="chi_sim")
        result = result.splitlines()

        # print(result)

        temp = []

        for item in result:
            if len(item) > 2:
                temp.append(item)

        result = temp
        print(result)
        # -----图像加载，识别部分------ 结束

        # ------分析数据，生成返回数据 scanResult
        orderNumRaw = ""
        unitRaw = ""
        netWorthRaw = ""
        feesRaw = ""
        timeRaw = ""

        for index, item in enumerate(result, start=0):
            # 交易类型
            if "红利再投资" in item:
                scanResult["Type"] = "红利再投资"
            elif "买入成功" in item:
                scanResult["Type"] = "买入"
            elif "卖出成功" in item:
                scanResult["Type"] = "卖出"
            elif "交易类型" in item and "强增" in item:
                scanResult["Type"] = "强增"

            # -#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-
            # 加载stock data frame 用来确认交易产品名称
            # -#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-

            # 时间
            elif "时间" in item and "确认时间" not in item:
                timeRaw = item

            # 订单号
            elif "订单号" in item and len(item) < 4:
                orderNumRaw = result[index + 1]
            elif "订单号" in item and len(item) > 4:
                orderNumRaw = item

            # 确认份额
            elif "份" in item and unitRaw == "":  # 增加 unitRaw == ""，这样只会处理第一个含“份”的字符
                unitRaw = item

            # 确认净值
            elif "确认净值" in item:
                netWorthRaw = item

            # 手续费
            elif "手续费" in item:
                feesRaw = item

        # post process
        unitRaw = "".join(c for c in unitRaw if c.isdigit() or c == ".")
        orderNumRaw = orderNumRaw.strip(" ").strip("订单号")
        netWorthRaw = netWorthRaw.strip(" ").strip("确认净值")
        feesRaw = "".join(c for c in feesRaw if c.isdigit() or c == ".")
        timeRaw = "".join(c for c in timeRaw if c.isdigit() or c in ".:-")
        timeRaw = timeRaw[:9] + " " + timeRaw[10:]

        # print(netWorthRaw)

        # 给dictionary赋值
        scanResult["OrderNumber"] = orderNumRaw
        scanResult["Unit"] = float(unitRaw)
        scanResult["NetWorth"] = float(netWorthRaw) if netWorthRaw != "" else 0
        scanResult["Fees"] = float(feesRaw) if netWorthRaw != "" else 0
        scanResult["Date"] = timeRaw

        #return scanResult
        print(scanResult)


stocklist = StockListModel()
stocklist.save()
# stocklist.load()
stocklist.show()

trade = TradeModel()
trade.save()

# stock list,
# holding stock
# trade history /record #monthly report
# all equity status
# price history of each equity
# 图表显示

# link the dataframe with assicmatic TUI
