import pandas  as pd
import numpy as np
# from step1 import get_data_year
import pickle
import tushare as ts
from step1 import get_oneyear_profit
# pe,pb,esp
with open('data_stock','rb') as f:
    data=pickle.load(f)
data_1=get_oneyear_profit()
M_pe=[]
M_pb=[]
for code in data_1.index:
    M_pe.append(data['pe'][str(code)])
    M_pb.append(data['pb'][str(code)])

data_1['pe']=M_pe
data_1['pb']=M_pb
# print(data_1['pe'].sort_values(ascending=False))

# 删除指标为0的股票，并且将每个指标的进行排序，结果以DataFrame形式返回
def drop_row(data,target):
    data=data_1[target].sort_values(ascending=False)
    M=[]
    N=[]
    for code,pe in zip(data.index,data):
        if pe >np.array([0]):
            M.append(code)
            N.append(pe)
    new_data=pd.DataFrame(N,index=M,columns=[target])
    return new_data

# 参数是drop_row中的返回值,也就是进行过排序的数据(DataFrame格式的)
def data_sort(data):
    num=data.values.shape[0]
    # print(num)
    data_pe=np.zeros(shape=[num,1])
    # print(data_pe[100 * (num // 100):, :])
    for i in range(1,102):
        if i==101:
            data_pe[(i - 1) * (num // 100):, :] = np.array([100,] * (num-100*(num // 100))).reshape(-1, 1)
            break
        data_pe[(i-1)*(num//100):(num//100)*i,:]=np.array([i]*(num//100)).reshape(-1,1)
    # for j in data_pe:
    #     print(j)
    data=pd.DataFrame(data_pe,index=data.index,columns=data.columns)
    return data
# print
# xx=data_sort(x)
# print(xx)

# 最后一步是以code为标准，将各个指标列结合到一个DataFrame里面，然后进行相加，最后进行排序得到最好的指标
def final_step(data_pb,data_pe):
    M=[]
    for code in data_pe.index:
        M.append(data_pb['pb'][code])
    data_pe['pb']=M
    return data_pe

if __name__=='__main__':
    # 返回的是DataFrame格式的数据,排好序并且将pe或者pb是0的进行删除
    data_pe = drop_row(data_1, 'pe')
    data_pb = drop_row(data_1, 'pb')
    # 给pe,pb进行按照排序进行打分
    data_pe_sort=data_sort(data_pe)
    data_pb_sort = data_sort(data_pb)
    # 将排序好的，并且打好分的pe,pb进行等权重求和,能得到一个综合价值因子，最后根据这个价值因子，对股票进行排序，能够得到排好序的因子。。。。
    data_merge=final_step(data_pb_sort,data_pe_sort)
    data_merge_array=data_merge.values[:,0]+data_merge.values[:,1]
    final_data=pd.DataFrame(data_merge_array,index=data_merge.index,columns=['values'])
    final_data_sort=final_data['values'].sort_values(ascending=False)
    final_data_sort.to_excel('final_sort.xlsx')
    print(final_data_sort)