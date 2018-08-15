# coding:utf-8
# data=np.arange(1000).reshape(250,4)
# np.savetxt('data.txt',data),data的格式必须是数字类型的
# ['a b c'].split(' ')可以这样进行转换。

import pandas as pd
import numpy as np
import tushare as ts
import csv
import os
class base_class():
    '''
    该类功能:
    1.对处理好的数据根据用户指定的指标进行排序(从大到小，或者从小到大)；method='sort+'或者method='sort-'(从大到小)

    2.首先用户指定一个指标，并给予该指标一个阈值，返回大于该阈值的股票代码,threshold可自己设置让用户选择.
    '''

    # 这里的参数：输入文件路径,排序方法，指标名，指标值的阈值，由用户自己进行设置
    # 不同的输入文件表示上市公司的不同能力,例如:盈利能力,偿债能力，成长能力，营运能力
    def __init__(self,file_path,save_txt):
        self.save_txt=save_txt
        self.file_path=file_path

    def write_txt(self,final_data):
        # final_data=final_data[['code','name',self.target]]
        # 文件名
        file_name='{}'.format(str(self.save_txt))
        # 当前目录如果有相同名字的文件，删除该文件
        if os.path.exists(file_name):
            os.remove(file_name)
        try:
            cols = list(final_data.columns)
            name = ''
            for col in cols:
                name = name + col + '\t'
            name = name + '\n'
            # name = str(col[0]) + '\t' + str(col[1]) + '\t' + str(col[2]) + '\t' + '\n'
            with open(file_name, 'a') as f:
                f.write(name)
            final_data_array = final_data.values
            # 将数据写入txt文件里面

            for stock in final_data_array:
                row = ''
                for i in stock:
                    row = row + str(i) + '\t'
                row = row + '\n'
                # row = str(stock[0]) + '\t' + str(stock[1]) + '\t' + str(stock[2]) + '\t' + '\n'
                with open(file_name, 'a') as f:
                    f.write(row)

        except Exception as e:
            print(e)
        return 'ok'

    def read_owntxt(self):
        M = []
        with open('{}'.format('data/{}'.format(self.file_path)), 'r') as f:
            for i in csv.reader(f):
                M.append(i[0].split('\t')[:-1])

        data = np.array(M)
        cols = data[0]
        data_pd = pd.DataFrame(data[1:, :2], columns=data[0][:2])
        num = 2
        for col in cols[2:]:
            data_pd[col] = data[1:, num].astype('f4')
            num += 1
        return data_pd


    def sort_stock(self,method='sort+'):
        try:
            data = self.read_owntxt()
            if method=='sort+':
                new_data=data.sort_values(by=self.target)
            if method=='sort-':
                new_data=data.sort_values(by=self.target,ascending=False)
            self.write_txt(new_data)
            return new_data
        except Exception as e:
            print(e)
    # 根据用户选定的指标，将大于或者等于用户设定阈值的股票筛选出来(threshold=0默认值)
    def set_thresthold(self,threshold=0):
        try:
            data=self.read_owntxt()
            new_data=data[data[self.target]>=threshold]
            self.write_txt(new_data)
        except Exception as e:
            print('error:%s'%e)

if __name__=='__main__':
    # 例子:文件名字:file_path='data_debt.txt',排序方法:method='sort-',阈值:threshold=10,指标:target='currentratio'
    a=base_class(file_path='data_growth.txt',save_txt='xxxxxxdg.txt',target='epsg')
    # 输出大于阈值10的股票池,参数是:文件路径/文件名字：例如,stocks_pool/tar1
    # a.set_thresthold(threshold=1000)
    #输出指标'currentratio'的指标值从大到小的排好顺序的股票池，参数是:文件路径/文件名字：例如,stocks_pool/tar1_sort
    a.sort_stock('sort+')
