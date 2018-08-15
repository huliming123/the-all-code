import tushare as ts
import pandas as pd
import numpy as np
import pickle
# data_stock=ts.get_stock_basics()

def get_oneyear_profit():
    # 股票列表获取
    with open('data_stock','rb') as f:
       data_stock=pickle.load(f)

    # 将上市时间是近2年的股票剔除
    data_stock=data_stock[data_stock['timeToMarket']<20160720]
    all_code=data_stock.index
    # data_profit=ts.get_profit_data(year=2017,quarter=1)
    # 分别获取2017年度4个季度的盈利数据
    with open('data_profit_1','rb') as ff:
        data_profit1=pickle.load(ff)
    with open('data_profit_2','rb') as ff:
        data_profit2=pickle.load(ff)
        data_profit2.to_excel('1.xlsx')

    with open('data_profit_3','rb') as ff:
        data_profit3=pickle.load(ff)
        data_profit3.to_excel('1.xlsx')
    with open('data_profit_4','rb') as ff:
        data_profit4=pickle.load(ff)
    # print(data_profit1['net_profits'])

    # 删除盈利数据重复的股票代码
    data_profit1=data_profit1.drop_duplicates('code')
    data_profit2=data_profit2.drop_duplicates('code')
    data_profit3=data_profit3.drop_duplicates('code')
    data_profit4=data_profit4.drop_duplicates('code')

    # 针对盈利数据，将code代码作为Index，净利润作为特征向量
    data_profit1=pd.DataFrame(data_profit1['net_profits'].values,index=data_profit1['code'],columns=['net_profits'])
    # data_profit1.to_excel('test.xlsx')
    data_profit2=pd.DataFrame(data_profit2['net_profits'].values,index=data_profit2['code'],columns=['net_profits'])
    data_profit3=pd.DataFrame(data_profit3['net_profits'].values,index=data_profit3['code'],columns=['net_profits'])
    data_profit4=pd.DataFrame(data_profit4['net_profits'].values,index=data_profit4['code'],columns=['net_profits'])
    # print(data_profit1['net_profits'])
    # print(data_profit2.shape)
    # 获取将上市时间大于2年的股票数据2017年4个季度的总的净利润
    M1=[]
    M2=[]
    M3=[]
    M4=[]
    # print(data_profit1['net_profits']['000953'])
    # print(type(data_profit1['net_profits']['300722']))
    for code in all_code:
        # print(code)
        try:
            # if type(data_profit1['net_profits'][code])!=
            # print(data_profit1['net_profits'][code])
            M1.append(data_profit1['net_profits'][code])
        except:M1.append(0)
        try:
            M2.append(data_profit2['net_profits'][code])
        except:
            M2.append(0)
        try:
            M3.append(data_profit3['net_profits'][code])
        except:
            M3.append(0)
        try:
            M4.append(data_profit4['net_profits'][code])
        except:
            M4.append(0)
    print('开始计算')
    # 计算上市时间是2年的股票的2017年的净利润
    M=np.array(M1)+np.array(M2)+np.array(M3)+np.array(M4)
    data_year=pd.DataFrame(M,index=list(all_code),columns=['one_year_profits'])
    data_year=data_year[data_year['one_year_profits']>0]
    return data_year
if __name__=='__main__':
    M=get_oneyear_profit()
    print(M)

# print(np.array(list(M1)))
# print(len(M2))
# print(len(M4))
# print(M.shape)

# col=data_profit.columns
# 盈利表中的按照code，将市盈率，市净率放在里面
# pe_profit=[]
# pd_profit=[]
# timeToMarke_profit=[]

