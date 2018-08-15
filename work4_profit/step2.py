import csv
import numpy as np
import pandas as pd
import pickle
import tushare as ts
import scipy.optimize as sco
from sklearn.preprocessing import Imputer
def save_data():
    # 取出股票池中的股票，并查找相应2017年交易日的收盘价
    codes=[]
    with open('code.txt','r') as f:
        for i in csv.reader(f):
            codes.append(i[0])
    data=pd.DataFrame()
    for code in codes:
        try:
            data_stock=ts.get_hist_data(str(code), start='2017-01-01', end='2017-12-31', ktype='D')['close']
            print(data_stock.shape[0])
            # 一年交易日数据低于200的股票自动筛选
            if data_stock.shape[0]>=200:
                data[str(code)]=data_stock
        #对于全年都没有交易的股票自动筛选出去
        except TypeError:
            print('error')
    # 缺失值用均值替代
    data = data.fillna(data.mean())

    # 将数据保存
    with open('data.pkl','wb') as ff:
        pickle.dump(data,ff)
    return 'save successfully'



def get_comb(data):
    returns= np.log(data / data.shift(1))
    # 计算总共有多少个股票
    noa=len(data.columns)
    day=len(data)
    # print(returns)
    #
    def statistics(weights):
        weights = np.array(weights)
        # 特定的权重(weights)下面，总的收益
        port_returns = np.sum(returns.mean()*weights)*day
        # 改权重下面，计算标准差
        port_variance = np.sqrt(np.dot(weights.T, np.dot(returns.cov()*day,weights)))
        return np.array([port_returns, port_variance, port_returns/port_variance])
    def min_var_(weights):
        return -1*statistics(weights)[2]
    bnds = tuple((0, 1) for x in range(noa))
    cons = ( {'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
    ops=sco.minimize(min_var_, noa * [1. / noa, ], method='SLSQP', bounds=bnds, constraints=cons)
    return ops['x']

# def get_comb(data):
#     returns= np.log(data / data.shift(1))
#     # 计算总共有多少个股票
#     noa=len(data.columns)
#     day=len(data)
#     # print(returns)
#
#     def statistics(weights):
#         weights = np.array(weights)
#         # 特定的权重(weights)下面，总的收益
#         port_returns = np.sum(returns.mean()*weights)*day
#         # 改权重下面，计算标准差
#         port_variance = np.sqrt(np.dot(weights.T, np.dot(returns.cov()*day,weights)))
#         return np.array([port_returns, port_variance, port_returns/port_variance])
#
#     # 使得方差最小
#     def min_variance(weights):
#         return statistics(weights)[1]
#     target_returns = np.linspace(0.0, 0.5, 500)
#
#     # weights是都在0-1之间的
#     bnds = tuple((0, 1) for x in range(noa))
#     target_variance = []
#     weights_list = []
#     for tar in target_returns:
#         # 约束是:收益约束为tar,权重值之和为1
#         cons = ({'type': 'eq', 'fun': lambda x: statistics(x)[0] - tar}, {'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
#         res = sco.minimize(min_variance, noa * [1. / noa, ], method='SLSQP', bounds=bnds, constraints=cons)
#         print(res['fun'])
#         # 在收益为tar下面，计算标准差值
#         target_variance.append(res['fun'])
#         weights_list.append(res['x'])
#     #     保存全年总收益以及相应的标准差
#     results = np.hstack((target_returns.reshape(-1, 1), np.array(target_variance).reshape(-1, 1)))
#     results=pd.DataFrame(results,columns=['profilt_year','variable'])
#     results.to_excel('results.xlsx')
#     # 保存组合方式
#     weights_pandas=pd.DataFrame(weights_list,columns=data.columns)
#     weights_pandas.to_excel('combingd.xlsx')

if __name__=='__main__':
    # save_data()
    with open('data.pkl', 'rb') as ff:
        data=pickle.load(ff)
    # print(get_comb(data))
    x=get_comb(data)
    data_result=pd.DataFrame(x.reshape(1,-1),columns=data.columns)
    # result_panadas=data_result[data_result>0.0001]
    data=np.hstack((np.array(data_result.columns).reshape(-1,1),data_result.values.reshape(-1,1)))
    print(data[data[:,1]>0.00001])

