# --------------解决 VScode output 里中文乱码的问题---------------------
import io
import sys

# 改变标准输出的默认编码
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf8")
# --------------解决 VScode output 里中文乱码的问题---------------------


import pandas as pd
import cv2
import pytesseract
import os


from asciimatics.widgets import (
    Frame,
    ListBox,
    Layout,
    Divider,
    Text,
    Button,
    TextBox,
    Widget,
    DropdownList,
)
from asciimatics.scene import Scene
from asciimatics.screen import Screen
from asciimatics.exceptions import ResizeScreenError, NextScene, StopApplication
import sys

import csv  # for scanned log file
from tools import diff
from existing_stock import df_before2020apr

project_path = "/home/guanxv/Python_Project/Stock_Price_Checker/Investment_Analysis/"

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

        # self._df.to_pickle("./Investment_Analysis/stock.pkl")  #path in windonws system
        self._df.to_pickle(
            project_path + "stock.pkl"
        )  # path in linux , may also work in windows

    def load(self):

        # self._df = pd.read_pickle("./Investment_Analysis/stock.pkl") #path in windonws system
        self._df = pd.read_pickle(
            project_path + "stock.pkl"
        )  # path in linux , may also work in windows

    @property
    def names_cn(self):

        return self._df.NameCN.values


class TradeHistoryModel(object):  # 交易记录
    def __init__(self):

        # Current trade id when editing.
        self.current_id = None

        try:

            # load from disk, once file has been save
            self.load()

        except FileNotFoundError:

            print("Trade.pkl not found! Blank file will be created!")
            self.initBlankdf()

        if (
            not "已有份额"
            in self._df["Type"].unique()
            # and not "2021-06-11 11:04:15" in self._df["DateStr"].unique()
        ):

            self._df = pd.concat([self._df, df_before2020apr])

        # Generate the list of pictures

        # path = '/home/guanxv/Python_Project/Stock_Price_Checker/Investment_Analysis/TradeHistoryPhoto'

        # path = "./TradeHistoryPhoto"
        path = project_path + "TradeHistoryPhoto"

        # path = os.getcwd()
        # print(path)

        # try to load scaned log file

        scanned = []

        try:

            with open(project_path + "scan.log") as scanned_csv:

                reader = csv.reader(scanned_csv)
                for row in reader:
                    scanned.append(row[0])

        except FileNotFoundError:

            scanned = []

        # get a list of picture files

        files = os.listdir(path)

        scans = []

        for f in files:

            if ".PNG" in f or ".png" in f or ".jpg" in f:

                scans.append(os.path.join(path, f))

        # excluded the scanned files

        scans = diff(scans, scanned)

        scanned = []

        # Scan all the remain pictures.

        for scan in scans:

            scanResult = self.scanImg(scan)
            self.add_scan_result(scanResult)
            scanned.append(scan)  # add the file name back to scanned

        # write scanned file back to log file
        with open(project_path + "scan.log", "a", newline="") as f:
            writer = csv.writer(f)
            for item in scanned:
                writer.writerow([item])

        # self._df['Date'] = pd.to_datetime(self._df['Date'], format='%Y-%m-%d %H:%M:%S') #将字符转换为 pd datatime 数据
        # self._df['Date'] = pd.to_datetime(self._df['Date'], format='%Y-%m-%d') #将字符转换为 pd datatime 数据
        # df['date'] = df['datetime'].dt.date # 只保留日期。建立新column

        self.dfUpdate()

        # print(self._df)

        self.total_id = len(self._df)

    def initBlankdf(self):

        # initiate the datafram , only need for first run
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
            ["买入", "TEST", "2000-06-11 11:04:15", 0, 0, 0, 0, "00000000"],
        ]

        self._df = pd.DataFrame(data, columns=columns)

    def save(self):

        # self._df.to_pickle("./Investment_Analysis/trade.pkl")
        self._df.to_pickle(project_path + "trade.pkl")

    def load(self):

        # self._df = pd.read_pickle("./Investment_Analysis/trade.pkl")
        self._df = pd.read_pickle(project_path + "trade.pkl")

    def show(self):

        # self._df.style.set_properties(**{'text-align': 'right'})
        print(self._df)

    def add_scan_result(self, result):

        duplicated = False

        for orderNumber in self._df.OrderNumber.values:

            # print(orderNumber)
            # print(result["OrderNumber"])

            if orderNumber == result["OrderNumber"]:

                duplicated = True

                return

        if not duplicated:

            self._df = self._df.append(result, ignore_index=True)

        # hello

    def updateFloatValue(self):

        self._df["Amount"] = self._df["AmountStr"].apply(float)
        self._df["Unit"] = self._df["UnitStr"].apply(float)
        self._df["NetWorth"] = self._df["NetWorthStr"].apply(float)
        self._df["Fees"] = self._df["FeesStr"].apply(float)

    def updateStrValue(self):

        self._df["AmountStr"] = self._df["Amount"].apply(str)
        self._df["UnitStr"] = self._df["Unit"].apply(str)
        self._df["NetWorthStr"] = self._df["NetWorth"].apply(str)
        self._df["FeesStr"] = self._df["Fees"].apply(str)

    def updateTotalAmount(self):

        self._df["TotalAmount"] = self._df["Fees"] + self._df["Amount"]

    def updateDate(self):

        self._df["Date"] = self._df["DateStr"].apply(lambda x: x[:10])
        self._df["Date"] = pd.to_datetime(self._df["Date"], format="%Y-%m-%d")

        # print(self._df)

    def dfUpdate(self):

        self.updateTotalAmount()
        self.updateStrValue()
        self.updateDate()

        self._df = self._df.sort_values(by=["Date", "Name"], ascending=True)
        self._df.reset_index(drop=True, inplace=True)

    def monthCapital(self):

        monthCap = self._df.groupby(
            pd.Grouper(key="Date", freq="M").TotalAmount.sum().reset_index()
        )
        print(monthCap)

    def scanImg(self, picPath):

        # Get the short name of Stock List in Chinese
        temp = []

        stock_cn_names = stocklist.names_cn

        for name_cn in stock_cn_names:
            name_cn = name_cn[:6]
            temp.append(name_cn)

        stock_cn_names_srt = temp

        # print(picPath)
        # 图像识别结果输入数据格式。
        # 交易类型 = ['买入', '卖出', '红利再投资' ,'增强']

        scanResult = {
            "Type": "",  # 交易类型
            "Name": "",  # 基金名称
            "DateStr": "",  # 操作时间
            "Amount": 0,  # 总金额
            "Unit": 0,  # 确认份额
            "NetWorth": 0,  # 单位净值
            "Fees": 0,  # 手续费
            "OrderNumber": "",  # 订单号
        }

        # -----图像加载，识别部分------
        pytesseract.pytesseract.tesseract_cmd = (
            # "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
            "/usr/bin/tesseract"
        )

        img = cv2.imread(
            # "C:/Users/Administrator/PycharmProjects/Stock_Price_Checker/Investment_Analysis/IMG-9738.png"
            #  "./Investment_Analysis/IMG-9736.PNG"
            picPath
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
        # print(result)

        result = result.splitlines()

        # print(result)

        temp = []

        for item in result:
            if len(item) > 2:
                temp.append(item)

        result = temp
        # print(result)
        # -----图像加载，识别部分------ 结束

        # ------分析数据，生成返回数据 scanResult
        orderNumRaw = ""
        unitRaw = ""
        netWorthRaw = ""
        feesRaw = ""
        timeRaw = ""
        stockNameRaw = ""
        amountRaw = ""

        for index, item in enumerate(result, start=0):

            # 名称
            for i, name in enumerate(stock_cn_names_srt, start=0):

                if name in item:

                    stockNameRaw = stock_cn_names[i]

                elif "景顺长城" in item and "益混合(LOF)" in item:

                    stockNameRaw = "景顺长城鼎益混合（LOF）"

            # 交易类型
            if "红利再投资" in item:
                scanResult["Type"] = "红利再投资"
            elif "买入成功" in item:
                scanResult["Type"] = "买入"
            elif "卖出成功" in item:
                scanResult["Type"] = "卖出"
            elif "交易类型" in item and "强增" in item:
                scanResult["Type"] = "强增"

            # 金额

            elif "确认金额" in item:
                amountRaw = item

            # 时间
            elif "时间" in item and "确认时间" not in item:
                timeRaw = item

            # 订单号
            elif "订单号" in item and len(item) < 4:
                orderNumRaw = result[index + 1]
            elif "订单号" in item and len(item) > 4:
                orderNumRaw = item

            # 确认份额
            elif (
                "份" in item and unitRaw == "" and "股份" not in item
            ):  # 增加 unitRaw == ""，这样只会处理第一个含“份”的字符
                unitRaw = item  # 增加 "股份" not in item, 这样不会处理"银华基金管理股份有限公司"

            # 确认净值
            elif "确认净值" in item:
                netWorthRaw = item

            # 手续费
            elif "手续费" in item:
                feesRaw = item

        # post process
        unitRaw = "".join(c for c in unitRaw if c.isdigit() or c == ".")
        orderNumRaw = orderNumRaw.strip("订单号").strip(" ")
        netWorthRaw = netWorthRaw.strip(" ").strip("确认净值")
        feesRaw = "".join(c for c in feesRaw if c.isdigit() or c == ".")
        timeRaw = "".join(c for c in timeRaw if c.isdigit() or c in ".:-")
        timeRaw = timeRaw[:10] + " " + timeRaw[10:]
        amountRaw = "".join(c for c in amountRaw if c.isdigit() or c in ".")
        lHalf = amountRaw[:-3]
        lHalf = lHalf.replace(".", "")
        rHalf = amountRaw[-3:]
        amountRaw = lHalf + rHalf

        # print(netWorthRaw)

        # 给dictionary赋值
        scanResult["OrderNumber"] = orderNumRaw
        scanResult["Unit"] = float(unitRaw) if unitRaw != "" else 0
        netWorthRaw = float(netWorthRaw) if netWorthRaw != "" else 0
        scanResult["NetWorth"] = (
            netWorthRaw if netWorthRaw < 100 else netWorthRaw / 10000
        )
        scanResult["Fees"] = float(feesRaw) if feesRaw != "" else 0
        scanResult["DateStr"] = timeRaw
        scanResult["Amount"] = float(amountRaw) if amountRaw != "" else 0
        scanResult["Name"] = stockNameRaw

        # print(scanResult)
        return scanResult


stocklist = StockListModel()
stocklist.save()
# stocklist.load()
stocklist.show()


tradehistory = TradeHistoryModel()
tradehistory.save()
tradehistory.dfUpdate()
tradehistory.show()

# ------------ asciimatic TUI 图形界面 ---------------------

# ----- Trade History view -----
class TradeView(Frame):
    def __init__(self, screen, model):
        super(TradeView, self).__init__(
            screen,
            screen.height * 4 // 5,
            screen.width * 4 // 5,
            hover_focus=True,
            can_scroll=False,
            title="交易记录",
            reduce_cpu=True,
        )
        # Save off the model that accesses the contacts database.
        self._model = model
        self._df = model._df

        # Create the form for displaying the list of contacts.
        layout = Layout([100], fill_frame=True)
        self.add_layout(layout)
        layout.add_widget(
            Text("交易类型:", "Type")
        )  # Label = "Type:" 在TUI 显示的标题 , Name "Type" 与Dataframe / List / Dict 对应的column名称
        layout.add_widget(Text("基金名称:", "Name"))
        layout.add_widget(Text("买入时间:", "DateStr"))
        layout.add_widget(Text("确认金额:", "AmountStr"))
        layout.add_widget(Text("确认份额:", "UnitStr"))
        layout.add_widget(Text("确认净值:", "NetWorthStr"))
        layout.add_widget(Text("手续费:", "FeesStr"))
        layout.add_widget(Text("订单号:", "OrderNumber"))

        layout2 = Layout([1, 1, 1, 1])
        self.add_layout(layout2)
        layout2.add_widget(Button("确认", self._ok), 0)
        layout2.add_widget(Button("上一条", self._previous), 1)
        layout2.add_widget(Button("下一条", self._next), 2)
        layout2.add_widget(Button("取消", self._cancel), 3)
        self.fix()

    def reset(self):
        # Do standard reset to clear out form, then populate with new data.
        super(TradeView, self).reset()
        if self._model.current_id is None:

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
                ["买入", "TEST", "2000-06-11 11:04:15", 0, 0, 0, 0, "00000000"],
            ]

            self.data = pd.DataFrame(data, columns=columns).iloc[0]

        else:
            self.data = self._df.iloc[self._model.current_id]
            # self.data = self._df.iloc[4]

    def _ok(self):
        self.save()
        if self._model.current_id is None:
            self._model.contacts.append(self.data)
        else:

            self._df.iloc[self._model.current_id] = self.data.values()
            self._model.updateFloatValue()
            self._model.save()

        # raise NextScene("Main")

    def _next(self):

        if self._model.current_id == None:
            self._model.current_id = 0

        if self._model.current_id < self._model.total_id - 1:

            self._model.current_id += 1

        self.data = self._df.iloc[self._model.current_id]

    def _previous(self):
        if self._model.current_id == None:
            self._model.current_id = 0

        if self._model.current_id > 0:

            self._model.current_id += -1

        self.data = self._df.iloc[self._model.current_id]

    @staticmethod
    def _cancel():
        raise NextScene("Main")


# ----- Month view -----
class MonthView(Frame):
    def __init__(self, screen, model):
        super(MonthView, self).__init__(
            screen,
            screen.height * 4 // 5,
            screen.width * 4 // 5,
            hover_focus=True,
            can_scroll=False,
            title="月度汇总",
            reduce_cpu=True,
        )
        # Save off the model that accesses the contacts database.
        self._model = model
        self._df = model._df

        layout = Layout([1, 18, 1])
        self.add_layout(layout)

        layout.add_widget(
            DropdownList(
                [
                    ("Item 1", 1),
                    ("Item 2", 2),
                    ("Item 3", 3),
                    ("Item 3", 4),
                    ("Item 3", 5),
                    ("Item 3", 6),
                    ("Item 3", 7),
                    ("Item 3", 8),
                    ("Item 3", 9),
                    ("Item 3", 10),
                    ("Item 3", 11),
                    ("Item 3", 12),
                    ("Item 3", 13),
                    ("Item 3", 14),
                    ("Item 3", 15),
                    ("Item 3", 16),
                    ("Item 4", 17),
                    ("Item 5", 18),
                ],
                label="Dropdown",
                name="DD",
                # on_change=self._on_change,
            ),
            1,
        )

        layout2 = Layout([1, 1, 1, 1])
        self.add_layout(layout2)
        # layout2.add_widget(self._reset_button, 0)
        # layout2.add_widget(Button("View Data", self._view), 1)
        layout2.add_widget(Button("取消", self._cancel), 3)
        self.fix()


    @staticmethod
    def _cancel():
        raise NextScene("Main")


# ----- Main Menu view -----
class MainView(Frame):
    def __init__(self, screen):
        super(MainView, self).__init__(
            screen,
            screen.height * 4 // 5,
            screen.width * 4 // 5,
            #    on_load=self._reload_list,
            hover_focus=True,
            can_scroll=False,
            title="Main Menu",
        )

        # Create the form for displaying the list of contacts.

        self._tradeview_button = Button("交易记录", self._tradeview)
        self._monthview_button = Button("月度汇总", self._monthview)
        self._fundview_button = Button("基金汇总", self._fundview)
        layout = Layout([100], fill_frame=True)
        self.add_layout(layout)
        layout.add_widget(self._tradeview_button)
        layout.add_widget(Divider())
        layout.add_widget(self._monthview_button)
        layout.add_widget(Divider())
        layout.add_widget(self._fundview_button)

        self._edit_button = Button("Edit", self._edit)
        self._delete_button = Button("Edit", self._delete)

        layout2 = Layout([1, 1, 1, 1])
        self.add_layout(layout2)
        # layout2.add_widget(Button("Add", self._add), 0)
        # layout2.add_widget(self._edit_button, 1)
        # layout2.add_widget(self._delete_button, 2)
        layout2.add_widget(Button("Quit", self._quit), 3)
        self.fix()
        self._on_pick()

    def _tradeview(self):
        raise NextScene("TradeDetail")

    def _monthview(self):
        raise NextScene("MonthView")

    def _fundview(self):
        raise NextScene("FundView")

    def _on_pick(self):
        # self._edit_button.disabled = self._list_view.value is None
        # self._delete_button.disabled = self._list_view.value is None
        pass

    def _add(self):
        self._model.current_id = None
        raise NextScene("Edit Contact")

    def _edit(self):
        self.save()
        self._model.current_id = self.data["contacts"]
        raise NextScene("Edit Contact")

    def _delete(self):
        self.save()
        del self._model.contacts[self.data["contacts"]]
        self._reload_list()

    @staticmethod
    def _quit():
        raise StopApplication("User pressed quit")


def demo(screen, scene):
    scenes = [
        Scene([TradeView(screen, tradehistory)], -1, name="TradeDetail"),
        Scene([MonthView(screen,tradehistory)], -1, name="MonthView"),
        Scene([MainView(screen)], -1, name="Main"),
    ]

    screen.play(scenes, stop_on_resize=True, start_scene=scene, allow_int=True)


last_scene = None
while True:
    try:
        Screen.wrapper(demo, catch_interrupt=True, arguments=[last_scene])
        sys.exit(0)
    except ResizeScreenError as e:
        last_scene = e.scene


# stock list,
# holding stock
# trade history /record #monthly report
# all equity status
# price history of each equity
# 图表显示

# link the dataframe with assicmatic TUI
