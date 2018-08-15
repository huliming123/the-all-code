import numpy as np
import pandas as pd
import pickle
from sklearn.preprocessing import scale,MinMaxScaler
import matplotlib.pyplot as plt
import matplotlib
# matplotlib.style.use('ggplot')
# x=np.linspace(-10,10,1000)
# y=my_sigmoid(x)
# plt.plot(x,y)
# plt.show()

# 打分函数
def my_sigmoid(x):
    return 1/(1+np.exp(-x))

# 均值标准化函数
def my_scale(data):
    return (data-data.mean())/data.mean()

def method_scores(data,num1,*args):
    '''
    :param data: DataFrame格式的数据
    :param num1: 每个行业取出的排名前num数量
    :param args: 元组,布尔类型的值，True表示相应的指标值越大，该指标越好;False表示相应的指标值越小越好。
    :return: 返回每个行业排名在前num位置的好股票
    '''
    cols=data.columns
    final_data=pd.DataFrame()
    if len(cols)-3!=len(args[0]):
        print('参数出错，重新输入')
        return
    # 根据行业进行分组
    for c_name ,industry_data in data.groupby('c_name'):
        # 对每个行业各个指标，进行按照单个指标进行标准化以及对指标值越小指标越好的指标求负值
        M,num=[],1
        for my_bool in args[0]:
            num += 1
            if my_bool ==True:
                # 每个指标值进行标准化
                M.append(my_scale(industry_data.values[:,num]))
            if my_bool==False:
                M.append(-1*(my_scale(industry_data.values[:,num])))
        # 最后得到的是标准化以及指标纠正后的numpy.adarray数据
        industry_data_scale=np.array(M).T.astype('f4')
        # 对每个指标值进行打分
        data_score=my_sigmoid(industry_data_scale)
        # 打分之后，修改industry_data的指标的值
        industry_data.values[:,2:-1]=data_score
        #做成DataFrame格式的数据
        new_data=pd.DataFrame(industry_data,columns=cols)
        # 计算分数等权重之和，添加新的列，列名为'scores'
        new_data['scores']=data_score.sum(axis=1)/(len(args[0]))
        # 从大到小排序
        new_data=new_data.sort_values(by='scores',ascending=False)
        # 取每个行业前面num个股票
        new_data=new_data.iloc[:num1]
        # 行连接到最终得到股票池
        final_data=pd.concat((final_data,new_data))
    #  放入excel 里面
    final_data.to_excel('final10_data.xlsx')
    return final_data


if __name__=='__main__':
    with open('input_data', 'rb') as f:
        data = pickle.load(f)
    args = (True,)*6
    method_scores(data,20,args)
