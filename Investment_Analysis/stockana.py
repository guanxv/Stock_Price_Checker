# --------------解决 VScode output 里中文乱码的问题---------------------
import io
import sys

# 改变标准输出的默认编码
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf8")
# --------------解决 VScode output 里中文乱码的问题---------------------


import pandas as pd


#----------------数据模型，用来建立，读取，写入数据。于TUI对接。---------------
class StockListModel(object):
    
    def __init__(self):

        #initiate the datafram , only need for first run
        columns = ['NameCN','NameEN', 'Code', 'Type', 'Note']
        data = [
        
        ['易方达中小盘混合','YFDZXPHH','110011','混合','None'],
        ['景顺长城鼎益混合（LOF）','JSCHDYHH','162605','混合','None'],
        ['银华富裕主题混合','YHFYZTHH','180012','混合','None'],
        ['诺德价值优势混合','NDJZYSHH','570001','混合','None'],
        ['兴全合润混合（LOF）','XQHRHH','163406','混合','None'],
        ['中欧医疗健康混合A','ZOYLJKHH','003095','医疗','None'],
        ['易方达中证银行指数（LOF）A','YFDZZYHZS','161121','银行','None'],
        ['工银瑞信全球精选股票（QDII）','HYRXQQJXGP','486002','全球股票','None'],
        ['国泰纳斯达克100指数（QDII）','GTNSDK100ZS','160213','纳斯达克','None'],
        ['交银海外中国互联网指数','JYHWZGHLWZS','164906','中概','None'],
        ['易方达中证海外中国互联网50ETF联接（QDII）C','YFDZZHWZGHL50ETF','006328','中概','None']
        
        ]      
        
        
        self._df = pd.DataFrame(data,columns = columns)

        
        #load from disk, once file has been save

        #self._df.style.set_properties(**{'text-align': 'left'})
        


    def show(self):

        print (self._df)

    def save(self):

        self._df.to_pickle("./stock.pkl")

    def load(self):

        self._df = pd.read_pickle("./stock.pkl")




stocklist = StockListModel()

# stocklist.load()
stocklist.show()







#stock list,
#holding stock
#trade history /record #monthly report
#all equity status
#price history of each equity
# 图表显示

#link the dataframe with assicmatic TUI