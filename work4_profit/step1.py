# coding=utf-8
import pandas as pd
import numpy as np
import pickle
import tushare as ts
#     销售毛利率=（销售收入-销售成本）/销售收入(gross_profit_rate)
#     销售净利率=净利/销售收入(net_profit_ratio)
# 每股现金流量/每股业绩(epcf/esp(stock表))

# 这里用的数据都是2018年的第一季度的最新数据
def save_data():
    data_profit = ts.get_profit_data(year=2018, quarter=1)
    with open('step1/data_profit.pkl','wb') as f:
        pickle.dump(data_profit,f)
    data_stock=ts.get_stock_basics()
    with open('step1/data_stock.pkl','wb') as ff:
        pickle.dump(data_stock,ff)
    data_report=ts.get_report_data(year=2018,quarter=1)
    with open('step1/data_report.pkl','wb') as fff:
        pickle.dump(data_report,fff)

def find_stocks():
    # gross_profit_rate(销售毛利率),net_profit_ratio(销售净利率)
    with open('step1/data_profit.pkl', 'rb') as f:
        data_profit=pickle.load(f)
    # print(data_profit.isnull().sum())
    # 提取需要的指标，并且缺失值用各自的指标均值进行填充
    data_profit=data_profit[['code','name','gross_profit_rate','net_profit_ratio']]
    data_profit=data_profit.fillna(data_profit.mean())
    data_profit_array=data_profit.values
    # 对数据进行剔除st与*st

    M=[]
    for stock in data_profit_array:
        if stock[1][:3]!='*ST' and stock[1][:2]!='ST':
            M.append(stock)
    data_profit=pd.DataFrame(np.array(M),columns=['code','name','gross_profit_rate','net_profit_ratio'])
    #
    data_gross=data_profit.sort_values(by='gross_profit_rate',ascending=False)
    data_gross_500=data_gross.values[:150]
    data_net=data_profit.sort_values(by='net_profit_ratio',ascending=False)
    data_net_500=data_net.values[:150]
    # 对出现在前500的股票放进集合容器中，然后进行集合的交集运算，求出同时出现在俩个指标排名前500的股票代码
    codes=set(data_gross_500[:,0])&set(data_net_500[:,0])

    # 股票代码保存在txt,构建股票池
    with open('code.txt','a') as f:
        for code in codes:
            code=str(code)+'\n'
            f.write(code)

if __name__=='__main__':
    pass
