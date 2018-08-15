import pickle
import tushare as ts
import numpy as np
import pandas as pd
# data_growth1=ts.get_growth_data(year=2017,quarter=1)
# data_growth2=ts.get_growth_data(year=2017,quarter=2)
# data_growth3=ts.get_growth_data(year=2017,quarter=3)
#
# all_data=pd.concat((data_growth1,data_growth2,data_growth3))

def data_deal(data,my_bool):
    '''
    :param data: DataFrame格式的数据
    :param my_bool: 用均值作为最终值:True，但是有缺失值会降低股票的真实水平；最后的一年作为最终值:False，能够比较真实表达公司的最近的指标水平
    :return: 处理好后的DataFrame格式数据
    '''
    cols=data.columns
    all_final_data=pd.DataFrame()
    # 对每一只股票近三年的数据进行数据清洗后求均值代替当前的
    for code,code_data in data.groupby('code'):
        # 先用前一年进行替代缺失值
        code_data=code_data.fillna(method='pad')
        # 如果没有前一年的数据，那么补0
        code_data=code_data.fillna(0)
        # 求每个指标3年的的均值
        if my_bool:
            code_data_array=code_data.values[:,2:-1].mean(axis=0)
        if not my_bool:
            # 用最后一年的来替代最终指标值，这样不会因为3年内有指标统计缺失，而降低其指标值
            code_data_array = code_data.values[-1,2:-1]
        # 得到一行数据:该股票的所有经过处理后的指标值,于code,name，c_name连接起来
        final_data_array=np.hstack((code_data.values[0,:2],code_data_array,code_data.values[0,-1]))
        print(final_data_array)
        # 构建DataFrame格式的数据
        final_data=pd.DataFrame(final_data_array.reshape(1,-1),columns=cols)
        # 返回最后的数据
        all_final_data=pd.concat((all_final_data,final_data))
    return all_final_data


if __name__=='__main__':
    with open('all_data.pkl', 'rb') as f:
        all_data = pickle.load(f)
    # print(all_data.isnull().sum())
    all_data['c_name'] = ['其他行业'] * all_data.shape[0]
    print(data_deal(all_data,False))
