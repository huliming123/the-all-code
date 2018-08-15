import pandas as pd
import numpy as np
import pickle
import tushare as ts
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
from pylab import mpl
import matplotlib
from sklearn.preprocessing import MinMaxScaler
mpl.rcParams['font.sans-serif'] = ['FangSong'] # 指定默认字体
mpl.rcParams['axes.unicode_minus'] = False # 解决保存图像是负号'-'显示为方块的问题

class PB_ROE():
    def __init__(self,c_name,score):
        self.c_name=c_name
        self.score=score

    def get_data(self,year,quarter):
        data=ts.get_stock_basics()
        data_roe=pd.DataFrame()
        for i in range(4):
            quarter+=1
            data_roe=pd.concat((data_roe,ts.get_report_data(year, quarter)))
        self.save_data(data,data_roe)

    def save_data(self,*datas):
        num=0
        for data in datas:
            num+=1
            with open('data/{}.pkl'.format(str(num)),'wb') as f:
                pickle.dump(data,f)

    # 近3年的数据求均值代替最终值
    def roe_mean_deal(self):
        with open('data/2.pkl','rb') as f:
            data=pickle.load(f)
        data=data[['code','name','roe']]
        cols = data.columns
        all_final_data = pd.DataFrame()
        # 对每一只股票近三年的数据进行数据清洗后求均值代替当前的
        for code, code_data in data.groupby('code'):
            code_data_array = code_data.values[:,-1].reshape(-1,1).mean(axis=0)
            final_data_array = np.hstack((code_data.values[0,:2], code_data_array))
            # 构建DataFrame格式的数据
            final_data = pd.DataFrame(final_data_array.reshape(1, -1), columns=cols)
            final_data=final_data.fillna(0)
            # 返回最后的数据
            all_final_data = pd.concat((all_final_data, final_data))
        return all_final_data

    def pb_roe_data(self):
        with open('data/1.pkl', 'rb') as f:
            data = pickle.load(f)
        # data=data[['code','name','pb']]
        roe_data=self.roe_mean_deal()
        M=[]
        for code in roe_data['code']:
            M.append(data['pb'][code])
        roe_data['pb']=M
        return roe_data

    # 保存行业数据
    def get_industry_data(self):
        data=ts.get_industry_classified()
        with open('data/data_industry.pkl','wb') as f:
            pickle.dump(data,f)
        return 'ok'

    # 将股票的行业数据放在最后一列，行业分组,根据用户所要进行的行业，将相应的数据进行保存。
    def industry_pb_roe_data(self):
        pb_roe_data=self.pb_roe_data()
        with open('data/data_industry.pkl','rb') as f:
            industry_data=pickle.load(f)
        industry_data=industry_data.drop_duplicates('code')
        industry_data=pd.DataFrame(industry_data.values[:,1:],index=industry_data['code'],columns=industry_data.columns[1:])
        M,W=[],[]
        # 行业数据放在最后一列
        for code in pb_roe_data['code']:
            try:
                M.append(industry_data['c_name'][code])
            except KeyError:
                M.append(np.nan)
        # 行业数据在最后一列
        pb_roe_data['c_name']=M
        # 将用户想要研究的行业里面的股票放在列表里面
        for stock in pb_roe_data.values:
            if self.c_name==stock[-1]:
                W.append(stock)
        # 列表转换为DataFrame的数据格式
        industry_pb_row_data=pd.DataFrame(W,columns=pb_roe_data.columns)
        # 剔除最小值与最大值
        industry_pb_row_data=industry_pb_row_data.sort_values(by='pb').iloc[1:-1]
        industry_pb_row_data = industry_pb_row_data.sort_values(by='roe').iloc[1:-1]
        return industry_pb_row_data

    def main(self):
        # 数据的准备
        data=self.industry_pb_roe_data()
        roe_data=data.values[:,2].reshape(-1,1)
        pb_data=data.values[:,3].reshape(-1,1)
        # roe_data = MinMaxScaler([0, 10]).fit_transform(roe_data)
        # pb_data = MinMaxScaler([0, 10]).fit_transform(pb_data)
        #   线性回归模型
        model=LinearRegression()
        model.fit(roe_data,pb_data)
        # 回归系数
        coef='%.3f'%float(model.coef_)
        # 回归方程常数项
        inter='%.3f'%float(model.intercept_)
        # 预测值
        y_pre=model.predict(roe_data)
        # 将被低估或者被高估的结果保存在excel里面
        self.lower_or_upper(data,y_pre)
        # 绘图
        self.get_image(roe_data,pb_data,y_pre,coef,inter)
        return 'ok'

    def get_image(self, roe_data,pb_data,y_pre,coef,inter):
        matplotlib.style.use('ggplot')
        plt.title('{}的PB-ROE模型'.format(self.c_name))
        plt.ylabel('P/B')
        plt.xlabel('ROE')
        plt.scatter(roe_data, pb_data, c='g')
        plt.plot(roe_data, y_pre, c='red', linewidth=5,label='y=%s*x+%s'%(coef,inter))
        plt.vlines(self.score,0,10, colors="c", linestyles="dashed",linewidth=3)
        plt.legend()
        plt.show()

    def lower_or_upper(self,data,y_pre):
        cols=data.columns
        data_array=data.values
        pb_data=data_array[:,3].reshape(-1,1)
        M,M1,W,W1=[],[],[],[]
        for i in range(len(cols)):
           M.append(data_array[:,i].reshape(-1,1)[[pb_data - y_pre.reshape(-1, 1) < 0]])
        lower_data=pd.DataFrame(np.array(M).T,columns=cols)
        # 将满足大于用户指定的roe最小值筛选出来
        for stock_low in lower_data.values:
            if stock_low[2]>self.score:
                M1.append(stock_low)
        try:
            new_lower_data=pd.DataFrame(np.array(M1),columns=cols)
            # 用户指定的roe, 剔除roe小于该得分的股票
            # 保存被低估的股票
            new_lower_data.to_excel('lower_stock.xlsx')
        except:
            print('请给出较小的roe值')

        # 将满足大于用户指定的roe最小值筛选出来
        for j in range(len(cols)):
            W.append(data_array[:,j].reshape(-1, 1)[[pb_data - y_pre.reshape(-1, 1) > 0]])
        upper_data = pd.DataFrame(np.array(W).T, columns=cols)
        for stock_upper in upper_data.values:
            if stock_upper[2] > self.score:
                W1.append(stock_upper)
        try:
            new_upper_data = pd.DataFrame(np.array(W1), columns=cols)
            # 存在被高估的股票
            new_upper_data.to_excel('upper_stock.xlsx')
        except:
            print('没有满足的股票，请调整roe')
        return 'ok'

if __name__=='__main__':
    # 根据不同行业设置不同的阈值,大于该阈值的值是我们要进行判别高估或者低估的股票。
    a=PB_ROE('钢铁行业',0)
    a.main()
    # print(a.final_regress_model())

# 0       综合行业
# 33      公路桥梁
# 53      化纤行业
# 79      机械行业
# 290     生物制药
# 445     石油行业
# 469     玻璃行业
# 488     仪器仪表
# 536     交通运输
# 623     飞机制造
# 637     农林牧渔
# 701     建筑建材
# 792     塑料制品
# 825     商业百货
# 918     纺织行业
# 960     医疗器械
# 991     有色金属
# 1063    供水供气
# 1088    发电设备
# 1153    造纸行业
# 1177    船舶制造
# 1185    煤炭行业
# 1226    食品行业
# 1284    陶瓷行业
# 1292    纺织机械
# 1300    钢铁行业
# 1360    环保行业
# 1387    酿酒行业
# 1420     次新股
# 1472    电器行业
# 1530    传媒娱乐
# 1570    化工行业
# 1720     房地产
# 1843    金融行业
# 1894    其它行业
# 2077     开发区
# 2087    电子信息
# 2334    服装鞋类
# 2383    电子器件
# 2535    电力行业
# 2597    汽车制造
# 2700    家具行业
# 2716    农药化肥
# 2762    酒店旅游
# 2798    水泥行业
# 2824    物资外贸
# 2845     摩托车
# 2851    印刷包装
# 2871    家电行业