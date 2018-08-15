# coding:utf-8
import tushare as ts
import numpy as np
import pandas as pd
import scipy.optimize as sco
import matplotlib.pyplot as plt
import pickle
#返回的特征解释
# date：日期
# open：开盘价
# high：最高价
# close：收盘价
# low：最低价
# volume：成交量
# price_change：价格变动
# p_change：涨跌幅
# ma5：5日均价
# ma10：10日均价
# ma20:20日均价
# v_ma5:5日均量
# v_ma10:10日均量
# v_ma20:20日均量
# turnover:换手率[注：指数无此项]
def get_data():
    data_stockcode = pd.read_excel('results.xlsx')
    data = pd.DataFrame()
    for code in data_stockcode[0]:
        origin_data = ts.get_hist_data(code=str(code), start='2017-01-01', end='2017-3-31', ktype='D')
        data[str(code)] = origin_data['close']
    # print(data.isnull().sum())
    new_data = data.fillna(method='pad')
    return new_data

def get_comb(new_data):
    # print(new_data.describe())
    # print(new_data.isnull().sum())
    noa=int(new_data.shape[1])
    returns = np.log(new_data / new_data.shift(1))
    variables=returns.cov()*noa
    # print(returns.head())
    # 夏普指数的负值最大化,
    def min_shar(weights):
        x_mean=(returns.mean().dot(weights.T))*noa
        x_variable=np.sqrt(np.dot(weights.T,np.dot(variables,weights)))
        return -1*(x_mean/x_variable)
    weights_begin=np.random.random_sample(noa)
    # 增加限制条件，权重总和是1
    cons = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
    # 权重限制在0,1之间
    bnds = tuple((0, 1) for x in range(noa))
    ops=sco.minimize(min_shar,x0=weights_begin,method='SLSQP',constraints=cons,bounds=bnds)
    print(ops['x'].round(3))
    print('---------')
    min_shar(ops['x'].round(3))
    #方差最小
    def min_variable(weights):
        x_variable=np.sqrt(np.dot(weights.reshape(1,-1),np.dot(variables,weights.reshape(-1,1))))
        return x_variable
    ops2=sco.minimize(min_variable,x0=weights_begin,method='SLSQP',bounds=bnds,constraints=cons)
    print(ops2['x'])
    min_shar(ops2['x'])
#     组合的有效前沿,给定收益率，使得是最小的,约束条件有2个，一个是收益率是确定的，其次是投资组合之和是1

    target_profit=np.linspace(0.01,0.3,2000)
    all_variables=[]
    for tar in target_profit:
        cons=({'type':'eq','fun':lambda x:(returns.mean().dot(x.T))*noa-tar},{'type':'eq','fun':lambda x:np.sum(x)-1})
        bons=tuple((0,1) for i in range(noa))
        ops3=sco.minimize(min_variable,np.array(15*[1/15,]),method='SLSQP',bounds=bons,constraints=cons)
        print('目标收益%s'%tar)
        print(ops3['x'].round(3))
        # weights=ops3['fun']
        all_variables.append(ops3['fun'])

    print(all_variables)
    plt.title('profit-variables')
    plt.xlabel('profit')
    plt.ylabel('variables')
    plt.grid(True)
    plt.scatter(target_profit,all_variables,c='r',label='profit-variables')
    plt.show()

if __name__=='__main__':
    new_data=get_data()
    get_comb(new_data)