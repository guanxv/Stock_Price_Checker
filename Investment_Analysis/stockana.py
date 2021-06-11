import pandas as pd

class StockListModel(object):
    
    def __init__(self):

        #initiate the datafram , only need for first run
        columns = ['NameCN','NameEN', 'Code', 'Type', 'Note']
        data = [
        
        ['易方达中小盘混合','YFDZXPHH','110011','Hunhe','None'],
        ['景顺长城鼎益混合（LOF）','JSCHDYHH','162605','Hunhe','None'],
        ['银华富裕主题混合','YHFYZTHH','180012','Hunhe','None'],
        ['景顺长城鼎益混合（LOF）','JSCHDYHH','162605','Hunhe','None'],
        ['景顺长城鼎益混合（LOF）','JSCHDYHH','162605','Hunhe','None'],
        ['景顺长城鼎益混合（LOF）','JSCHDYHH','162605','Hunhe','None'],
        ['景顺长城鼎益混合（LOF）','JSCHDYHH','162605','Hunhe','None'],
        ['景顺长城鼎益混合（LOF）','JSCHDYHH','162605','Hunhe','None'],
        ['景顺长城鼎益混合（LOF）','JSCHDYHH','162605','Hunhe','None'],
        ['景顺长城鼎益混合（LOF）','JSCHDYHH','162605','Hunhe','None'],
        ['景顺长城鼎益混合（LOF）','JSCHDYHH','162605','Hunhe','None'],
        ['景顺长城鼎益混合（LOF）','JSCHDYHH','162605','Hunhe','None']
        ]      
        
        
        self._df = pd.DataFrame(data,columns = columns)

        
        #load from disk, once file has been save

        #self._df.style.set_properties(**{'text-align': 'left'})
        


    def show(self):

        print (self._df)


stocklist = StockListModel()

stocklist.show()



#stock list,
#holding stock
#trade history /record #monthly report
#all equity status

