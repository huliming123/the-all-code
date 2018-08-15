# coding:utf-8
import tushare as ts
import pickle
for i in range(1,5):
    # data=ts.get_profit_data(year=2017,quarter=i)
    with open('data_profit_{}'.format(str(i)),'rb') as f:
        data=pickle.load(f)
        data.to_excel('%s.xlsx'%i)
    print('第{}个已经完成了'.format(str(i)))