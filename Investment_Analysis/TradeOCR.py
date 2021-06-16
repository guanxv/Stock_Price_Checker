# --------------解决 VScode output 里中文乱码的问题---------------------
import io
import sys

# 改变标准输出的默认编码
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf8")
# --------------解决 VScode output 里中文乱码的问题---------------------

#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-
#把整个流程做成function，可以把这个function坐在别的class里 （比如trade）
#trade class里可以有增加记录 删除记录，浏览记录，手动输入记录。
# 可以用filter看某一个产品的基金交易，或者某一个月的交易
#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-




import cv2
import pytesseract

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
img = img[50 : img.shape[0], 0 : img.shape[1]]  # crop the image, remove top staus bar

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

    #-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-
    #加载stock data frame 用来确认交易产品名称
    #-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-

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

print(scanResult)
