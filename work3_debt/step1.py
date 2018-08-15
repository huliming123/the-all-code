# coding:utf-8
import pandas as pd
import numpy as np
import pickle
import tushare as ts
import matplotlib.pyplot as plt
from pylab import mpl
from sklearn.preprocessing import Imputer
from write_txt import write_txt
import matplotlib
from pyecharts import Scatter3D,Line
def save_data():
    data=ts.get_debtpaying_data(year=2017,quarter=1)
    with open('step1/data_debt.pkl','wb') as f:
        pickle.dump(data,f)
def get_data():
    with open('step1/data_debt.pkl','rb') as f:
        data=pickle.load(f)
    return data

def data_deal():
    data=get_data()
    # print(data.columns)
    data_array=data.values

    # 删除具有缺少值的股票,以及删除*st与st的股票
    x_data=[]
    for stock in data_array:
        if '--' not in stock and stock[1][:3]!='*ST' and stock[1][:2]!='ST':
            x_data.append(stock)
    new_data=np.array(x_data)

    # 将流动比率，速动比率，现金比率拿出来,numpy.adarry格式的
    new_data=new_data[:,:5]
    #行业分类表格，上次出错就在这里
    data_industry=ts.get_industry_classified()
    # 删除重复出现的代码，一个股票只能是一个行业
    data_industry=data_industry.drop_duplicates('code')
    data_industry=pd.DataFrame(data_industry.values[:,-1],index=data_industry['code'],columns=['c_name'])
    #按照负债表得到的code,再依据行业分类表格，对负债表中的股票进行行业分类
    w=[]
    for code in new_data:
        try:
            w.append(data_industry['c_name'][code[0]])
        except:
            #对行业分类缺失的股票认定为：其他行业
            w.append('其它行业')

    final_data=np.hstack((new_data,np.array(w).reshape(-1,1)))
    # 负债表中的股票分好类，转换为DataFrame形式的
    final_data=pd.DataFrame(final_data,columns=['code','name','currentratio','quickratio','cashratio','c_name'])
    # print(final_data)
    final_data=pd.DataFrame(np.hstack((final_data.values[:,:2],final_data.values[:,2:5].astype('f4'),final_data.values[:,-1].reshape(-1,1))),columns=['code','name','currentratio','quickratio','cashratio','c_name'])
    # 求均值，每个行业的三个指标的均值，放在字典里面{'电器行业':[1,23,2],....}
    data_dic={}
    for i in final_data.groupby(final_data['c_name']):
        cur_mean,quic_mean,cash_mean=i[1]['currentratio'].values.mean(),i[1]['quickratio'].values.mean(),i[1]['cashratio'].values.mean()
        data_dic[i[0]] = [cur_mean,quic_mean,cash_mean]
    return data_dic
    # 按照每只股票所属行业，根据行业指标字典，将三个指标的行业均值放入进去.
    # M=[]
    # for c_name in final_data['c_name']:
    #     M.append(data_dic[c_name])
    # final_data=np.hstack((final_data.values,np.array(M)))
    # with open('step2/final_data.pkl','wb') as g:
    #     pickle.dump(final_data,g)
    # for stock in final_data:
    #     name=str(stock[0])+'\t'+str(stock[1])+'\t'+str(stock[2])+'\t'+str(stock[3])+'\t'+str(stock[4])+'\t'+str(stock[5])+'\t'+str(stock[6])+'\t'+str(stock[7])+'\t'+str(stock[8])+'\n'
    #     with open('step1/data_deal.txt','a') as f:
    #         if stock[0]==final_data[0][0]:
    #            f.write('code'+'\t'+'name'+'\t'+'currentratio'+'\t'+'quickratio'+'\t'+'cashratio'+'\t'+'c_name''\t'+'currentratio_mean'+'\t'+'quickratio_mean'+'\t'+'cashratio_mean'+'\n')
    #         f.write(name)
    # return final_data

# print(final_data_pandas[final_data_pandas['debt_values']>500])


from pyecharts import Bar,Page

if __name__=='__main__':
    # # 流动比率，速动比率，现金比率
    page=Page()
    data=data_deal()
    print(data)
    # data=data[:,2:5]
    # print(data)
    def tets(data):
        data = pd.DataFrame(data[:, 2:5], index=data[:, 1], columns=['currentratio', 'quickratio', 'cashratio'])
        # data = data.iloc[:300, ]
        def stocks_(data,target,tar_china):
            data= data.sort_values(by=target,ascending=False)
            print(data)
            attr = ["{}".format(i) for i in list(data.index)[:20]]
            v1 =data[target].values[:20]
            bar = Bar("{}排名前20的股票展示图".format(tar_china),width=1200,height=600)
            bar.add("", attr, v1, is_datazoom_show=True)
            page.add(bar)
            page.render(path='stocks_rank.html')
            # 速动比率，现金比率
        stocks_(data,'currentratio','流动比率')
        stocks_(data, 'quickratio', '速动比率')
        stocks_(data, 'cashratio', '现金比率')



    def industry_():
        from pyecharts import Page
        page=Page()
        def test():
            scatter3D = Scatter3D("基于3个指标的行业偿债能力图", width=1200, height=600)
            scatter3D.add("", data.values,is_visualmap=True)
            page.add(scatter3D)
            page.render(path='stocks_debt_values.html')
        def get_images_(num,target):
            line = Line("{}折线图示例".format(target), width=1200*0.8, height=600*0.8)
            attr = list(data.index)[:]
            line.add(
                '',
                attr,
                data.values[:,num],
                mark_point=["max", "min"],
                mark_line=["average"],
            )
            page.add(line)
            page.render(path='{}.html'.format(str(target)))
        get_images_(0,'流动比率')
        get_images_(1,'速动比率')
        get_images_(2,'现金比率')
        test()

# matplotlib.style.use('ggplot')
# mpl.rcParams['font.sans-serif'] = ['FangSong'] # 指定默认字体
# mpl.rcParams['axes.unicode_minus'] = False # 解决保存图像是负号'-'显示为方块的问题
# def get_image(data_industry,target,tar_china,industry='行业'):
#     # print(data_industry.sort_values(by=str(target),ascending=False))
#     plt.title(str(tar_china)+'排名')
#     plt.xlabel(str(industry))
#     plt.ylabel(str(tar_china))
#     data_industry.sort_values(by=str(target),ascending=False).iloc[:10,][str(target)].plot.bar()
#     plt.gcf().autofmt_xdate()
#     plt.show()
#
# # 流动比率，速动比率，现金比率
# get_image(data_industry,'currentratio','流动比率')