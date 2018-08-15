import pandas as pd
import numpy as np
# from step1 import data_deal,get_data
import pickle
import tushare as ts
# 建立股票池
def get_target(final_data):
    # 3.确定单项量化指标
    # tar1=(流动比率-理论值)/理论值
    # tar2=(速动比率-理论值)/理论值
    # tar3=(现金比率-理论值)/理论值
    final_data[:,2]=(final_data[:,2]-final_data[:,6])/final_data[:,6]
    final_data[:,3]=(final_data[:,3]-final_data[:,7])/final_data[:,7]
    final_data[:,4]=(final_data[:,4]-final_data[:,8])/final_data[:,8]
    # 确定偿债能力量化指标(加权)
    # final_tar=1/3*tar1+1/3*tar2+1/3*tar3
    final_data[:,8]=(final_data[:,2]+final_data[:,3]+final_data[:,4])*1/3
    for i in final_data:
        print(i)
    # 提取股票的代码以及名称
    final_data=np.hstack((final_data[:,:2],final_data[:,-1].reshape(-1,1)))
    final_data_pandas=pd.DataFrame(final_data,columns=['code','name','debt_values'])
    with open('step3/final_data_pandas.pkl','wb') as g:
        pickle.dump(final_data_pandas,g)
    for yangben in final_data_pandas.values:
        name=str(yangben[0])+'\t'+str(yangben[1])+'\t'+str('%.3f'%yangben[2])+'\n'
        with open('step2/the_result.txt','a') as f:
            if yangben[0]==final_data_pandas.values[0][0]:
                f.write('code'+'\t'+'name'+'\t'+'debt_values'+'\n')
            f.write(name)
    return final_data_pandas

if __name__=='__main__':
    with open('step2/final_data.pkl','rb') as f:
        data=pickle.load(f)
    get_target(data)
