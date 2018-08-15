# coding:utf-8
import tushare as ts
import matplotlib.pyplot as plt
import scipy.optimize as sco
import pickle
import pandas as pd
import numpy as np
from sklearn.feature_selection import VarianceThreshold
from sklearn .cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.model_selection import GridSearchCV
from sklearn.preprocessing import Imputer,scale
#  roe 缺失值过多，删除该特征变量.business_income，net_profits相关性较高，删除business_income,eps 与bips 相关性较高，删除bips
# 剩余net_profit_ratio，gross_profit_rate，net_profits，eps

def get_data():
    data=ts.get_profit_data(year=2017,quarter=1)
    # 2017年度第一季度的盈利数据
    with open('data.pkl','wb') as f:
        pickle.dump(data,f)
    return data

def select_fea():
    with open('1.pkl','rb') as f:
        data=pickle.load(f)
    # print(data.isnull().sum())都有缺失值，roe缺失值达到225个，缺失值过多
    print(data.columns)
    #  roe 缺失值过多，删除该特征变量.business_income，net_profits相关性较高，删除business_income,eps 与bips 相关性较高，删除bips
    # 剩余net_profit_ratio，gross_profit_rate，net_profits，eps
    data = data.drop('roe', axis=1)
    data = data.drop('business_income',axis=1)
    data = data.drop('bips',axis=1)
    data_array=data.values[:,2:]
    new_data=Imputer(missing_values=np.nan,strategy='mean').fit_transform(data_array)
    with open('new_data.pkl','wb') as f:
        pickle.dump(new_data,f)

def select_stock():
    with open('new_data.pkl','rb') as f:
        new_data=pickle.load(f)
    # new_data=scale(new_data)
    clu=KMeans(n_clusters=3,max_iter=300)
    clu.fit(new_data)
    y_class=clu.predict(new_data)
    # num=-1
    # for i in y_class:
    #     num+=1
    #     if i!=np.array([0]):
    #         print('第%d行，样本类别是%d类别'%(num,i))
    #         # print('第%d行%s'%(num,new_data[num],))


    # 各个类别的聚类中心点坐标
    print(clu.cluster_centers_)
    with open('1.pkl','rb') as g:
        origin_data=pickle.load(g)
        print(origin_data.shape)
    with open('new_data.pkl', 'rb') as gg:
        origin_new_data = pickle.load(gg)
        print(origin_data.shape)
    # 将聚类结果与原始数据列合并
    fina_data=np.hstack((origin_data.values[:,:2],origin_new_data,y_class.reshape(-1,1)))
    # 保存到excel文件中
    pd.DataFrame(fina_data).to_excel('results.xlsx')


def get_comb():
    data=pd.read_excel('results.xlsx')
    data_stock=pd.DataFrame()
    noa = len(data_stock)
    for code in data[0]:
        data1 = ts.get_hist_data(code=str(code), start='2017-01-01', end='2017-03-31', ktype='D')
        data_stock[str(code)]=data1['close']
    # print(data_stock.shape)
    returns = np.log(data_stock / data_stock.shift(1))
    means=returns.mean() * 59
    # 协方差
    covs=returns.cov() * 59
    print(covs.shape)
    def strat(weights):
        # 分配权重
        # weights=np.random.random_sample(size=[15,1])
        # weights=weights/weights.sum()
        # 组合的总收益
        x_means=returns.mean().dot(weights.reshape(-1,1))*59
        # print(x_means)
        # 组合的方差
        x_variable=np.dot(weights.T,np.dot(covs,weights))
        return x_means,x_variable

    def min_sharpe(weights):
      return strat(weights)[0]/strat(weights)[1]
    bnds = tuple((0, 1) for x in range(15))
    cons = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
    opts = sco.minimize(min_sharpe,x0=15*(1/15,),method='SLSQP', bounds=bnds, constraints=cons)
    print(opts['x'].round(3))

def get_optimi():
    # 组合总收益
    port_returns = []
    # 组合方差
    port_variance = []
    # 随机权重，总共循环4000次
    for _ in range(4000):
        # 随机赋权
        weights = np.random.random_sample(size=[15, 1])
        weights = weights / weights.sum()
        # 将总收益放进列表中
        port_returns.append(x_means)
        # 将组合方差放进列表中
        port_variance.append(x_variable)
    # 格式转换成numpy.adarray格式的
    port_returns = np.array(port_returns)
    port_variance = np.array(port_variance)
    print(port_returns)
    risk_free = 0.04
    plt.figure(figsize=(8, 4))
    plt.scatter(port_variance, port_returns,c='red',marker='o')
    plt.grid(True)
    plt.xlabel('excepted volatility')
    plt.ylabel('expected return')
    plt.show()
    # plt.colorbar(label='Sharpe ratio')
    return get_optimi
    # new_data=data[[2,3,4,5]]
    # # print(data.corr())
    # data1=ts.get_hist_data(code='601318',start='2017-01-01',end='2017-03-31',ktype='D')
    # print(data1.shape)
    # returns=np.diff(data1['close'].values).sum()
    # print(returns)
if __name__=='__main__':
    print('just working')
    # select_fea()
    # select_stock()
    func=get_comb()
    print('end working')

    # param_dict={'init':['k-means++','random'],'n_clusters':[2,3],'max_iter':[300,400,500,200]}
    # model=GridSearchCV(clu,param_dict)
    # model.fit(new_data)
    # scores = model.best_params_
    # print(scores)
    # 分类越多越好，但是我们最多将其分为3类别（盈利较好的股票，盈利一般的股票，以及盈利不好的股票），参数给出是3,init='K-means'
    # 'max_iter=300'
    # data=data.drop([data.columns[[0,1,7,8]]], axis=1,inplace=True)
    # data_array=data.values[1:]
    # print(data_array)
    # data_array=data.values
    # new_data=data_array[:,2:]
    # print(new_data.shape)
    # model=PCA(n_components=)