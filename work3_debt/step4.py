# coding:utf-8
import tushare as ts
import numpy as np
import pandas as pd
import scipy.optimize as sco
import matplotlib.pyplot as plt
import pickle
def save_data():
    with open('step4/final_data_sort.pkl','rb') as f:
        data=pickle.load(f)
    #  综合指标是排名前面50名的股票
    final_data = pd.DataFrame(data.values[:50, :], columns=['code', 'name', 'debt_values'])
    # print(final_data)
    data=pd.DataFrame()
    for code in final_data['code']:
        data_onecode=ts.get_hist_data(code,start='2017-01-01',end='2017-12-31')
        try:
            # 一年至少有200天交易的股票，其余的交易数据缺失过多，所以去掉
            if data_onecode.shape[0]>200:
                data[code]=data_onecode['close']
        # 对于缺失的股票代码直接过滤
        except AttributeError:
            print('NoneType')
 # 用均值填充缺失值，并且保存数据，方便下次使用
    print('the finally')
    data=data.fillna(data.mean())
    print(data.isnull().sum())
    with open('step4/data.pkl','wb') as ff:
        pickle.dump(data,ff)
    return 'just okk'

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

def test():
    returns = np.log(data / data.shift(1))
    # 计算总共有多少个股票
    noa = len(data.columns)
    day = len(data)

    # print(returns)
    #
    def statistics(weights):
        weights = np.array(weights)
        # 特定的权重(weights)下面，总的收益
        port_returns = np.sum(returns.mean() * weights) * day
        # 改权重下面，计算标准差
        port_variance = np.sqrt(np.dot(weights.T, np.dot(returns.cov() * day, weights)))
        return np.array([port_returns, port_variance, port_returns / port_variance])
    # 使得方差最小
    def min_variance(weights):
        return statistics(weights)[1]
    target_returns = np.linspace(0.0, 0.5, 500)
    # weights是都在0-1之间的
    bnds = tuple((0, 1) for x in range(noa))
    target_variance = []
    weights_list = []
    for tar in target_returns:
        # 约束是:收益约束为tar,权重值之和为1
        cons = ({'type': 'eq', 'fun': lambda x: statistics(x)[0] - tar}, {'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
        res = sco.minimize(min_variance, noa * [1. / noa, ], method='SLSQP', bounds=bnds, constraints=cons)
        print(res['fun'])
        # 在收益为tar下面，计算标准差值
        target_variance.append(res['fun'])
        weights_list.append(res['x'])
    #     保存结果
    results = np.hstack((target_returns.reshape(-1, 1), np.array(target_variance).reshape(-1, 1)))
    results=pd.DataFrame(results,columns=['profilt_year','variable'])
    results.to_excel('results.xlsx')
    # 保存组合方式
    weights_pandas=pd.DataFrame(weights_list,columns=data.columns)
    weights_pandas.to_excel('combingd.xlsx')
    #     target_variance_array = np.array(target_variance)
    # final_profit=np.hstack((target_returns.reshape(-1,1),target_variance_array.reshape(-1,1)))
    # print(final_profit)

if __name__=='__main__':
    with open('step4/data.pkl','rb') as f:
        data=pickle.load(f)
    # print(data)
    x=get_comb(data)
    data_result=pd.DataFrame(x.reshape(1,-1),columns=data.columns)
    # result_panadas=data_result[data_result>0.0001]
    data=np.hstack((np.array(data_result.columns).reshape(-1,1),data_result.values.reshape(-1,1)))
    print(data[data[:,1]>0.00001])

    # for i in data.values:
    #     print(i)