# coding:utf-8
from Base_class import base_class
import pandas as pd
import numpy as np
class Sort_threshold(base_class):
    '''
    该类的功能:(1)交叉选股：提供用户选择指标，并且选择相应阈值，求满足各个阈值要求后的股票池的交集,获得最终股票池
    (2)提供用户的单个指标的排序功能
    股票池保存txt文件
    '''
    # 在父类的基础上，由于不知道用户给多少指标进行操作，增加了*args这一参数
    def __init__(self, file_path, save_txt,*args):
        base_class.__init__(self,file_path,save_txt)
        self.ar=args

    def result_func(self,data,first_set,cols,W=[]):
        '''

        :param data: DataFrame格式的数据，从txt读取的数据（经过稍微处理后的）
        :param first_set: (各个股票池交集后的股票池集合)
        :param W: (空的列表)
        :param cols:(列名，code,name,以及指标名)
        :return: 'ok'
        '''
        for stock in data.values:
            for code in first_set:
                if code==stock[0]:
                    W.append(stock)
        try:
            final_data=pd.DataFrame(np.array(W),columns=cols)
            print('-' * 100)
            print(final_data)
            # 调用父类方法,写入txt文件
            self.write_txt(final_data)
        # 捕捉异常：W=[]，表示没有股票被选择进来，此时报错（ValueError）
        except ValueError:
            print('没有任何股票被选择')

    def set_and(self,M):
        '''
        :param M: 参数形如:[{'300028', '002316'},{'600416', '002316'}]
        :return: 交集后的股票池代码的集合{'002316'}
        '''
        first_set = M[0]
        for code_set in range(len(M)):
            # 求集合的交集（相同的股票放在一个first_set里面）
            first_set = first_set & M[code_set]
        return first_set

    # 重写父类的阈值方法，增加的功能就是可以对任意多个指标进行操作得到大于或者小于阈值的股票池，最终得到股票池的交集（最终的股票池）
    def set_thresthold(self,*thresholds):
        '''

        :param thresholds: 参数形如：'>',10,'<',10,'>',800
        :return: 'ok'
        '''
        # 这里用了父类的方法，读取用户输入的txt文件，返回DataFrame格式的数据
        data = self.read_owntxt()
        # 删除重复股票代码
        data=data.drop_duplicates('code')
        # 表示列名；code,name是必须的，以及相应的要操作的指标
        cols=['code','name']+list(self.ar)
        try:
            # 只需要相应的要操作的数据
            data=data[cols]
        # 捕捉错误：txt里面没有相应的指标名称
        except KeyError:
            print('请输入正确的指标名称')
            return
        M,num=[],-1
        # 将各个指标满足对应阈值的要求的股票池代码(code)，分别以集合的形式放进列表中

        for tar in self.ar:
            num+=1
            # 保证奇数位置是'>'或者'<'
            if thresholds[num] != '<' and thresholds[num] != '>':
                print('请输入对指标的操作，大于或者小于')
                return
            if thresholds[num]=='>':
                num += 1
                try:
                    # 当指标前面是大于号，表示求大于该指标的股票池
                    new_data = data[data[tar] >= thresholds[num]]
                    print(new_data.shape)
                    # 将满足大于指标的阈值的股票代码以放在集合里面，并放进列表中
                    M.append(set(new_data['code']))

                except Exception as e:
                    print('error:%s' % e)
            if thresholds[num] == '<':
                num += 1
                try:
                    # 当指标前面是小于号，表示求小于该指标的股票池
                    new_data = data[data[tar] <= thresholds[num]]
                    print(new_data.shape)
                    # 将满足小于指标的阈值的股票代码以放在集合里面，并放进列表中
                    M.append(set(new_data['code']))
                except Exception as e:
                    print('error:%s' % e)
        # 现在列表里面的对象是各个集合，集合是各个指标对应的满足阈值条件的股票代码
        #各个股票池根据集合求交集，最后得到的是各个股票池都有的股票。
        # 求集合的交集（相同的股票放在一个first_set里面）
        first_set=self.set_and(M)
        # 根据上面的股票代码(放在集合first_set里面的股票代码)，构建DataFrame格式的数据(包含进行操作的指标数据),并写入txt文件中
        self.result_func(data=data,first_set=first_set,cols=cols)
        return 'ok'

    # 重写父类的排序方法，功能增加了取出排序后的前n股票，默认是15,主要还是对单个指标进行排序,对要求同时排序的用户给予拒绝
    def sort_stock(self,num1=15,*method):
        '''
        :param method: 排序方式,'sort+'从小到大，'sort-'从大到小,元组形式
        :param num: 取前n只股票
        :return: 返回'ok'
        '''
        # 这里用了父类的方法，读取用户输入的txt文件，返回DataFrame格式的数据
        data = self.read_owntxt()
        # 删除重复股票代码
        data=data.drop_duplicates('code')
        # 表示列名；code,name是必须的，以及相应的要操作的指标
        cols=['code','name']+list(self.ar)
        try:
            # 只需要相应的要操作的数据
            data=data[cols]
        # 捕捉错误：txt里面没有相应的指标名称
        except KeyError:
            print('请输入正确的指标名称')
            return
        M,num=[],-1
        for tar in self.ar:
            num+=1
            try:
                if method[num]=='sort+':
                    new_data=data.sort_values(by=tar)
                if method[num]=='sort-':
                    new_data=data.sort_values(by=tar,ascending=False)
                M.append(set(new_data.iloc[:num1]['code']))
            except Exception as e:
                print(e)
        #返回交集
        first_set=self.set_and(M)
        #...
        self.result_func(data=data,first_set=first_set,cols=cols)
        return 'ok'


if __name__=='__main__':
    '''
    for example:此处用例仅供参考;
    该类主要用于后面的选择优质股的研究；
    '''
    # 第一个参数是要读取的txt文件,第二个参数是处理好，输出股票池保存的txt文件地址,
    # 后面的参数是要操作的指标的名称（前提是必须要有相应的指标，设置的报错:'请输入正确的指标名称'）
    # a=Sort_threshold('data_growth.txt','666.txt','mbrg','nprg')
    # 这里的参数是相应指标的阈值以及对阈值的操作，这里是输出大于该阈值的股票，'mbrg'大于10的股票池与'nprg'小于10，'targ'大于500的股票池的交集....
    # 表示相应指标大于10，小于10，大于5000三个股票池的交集，最终的股票池
    # a.set_thresthold('>',16,'<',20)

    # 对指标mbrg排序，注意只能是一个指标，否则报错:'指标选择过多，请重新选择',取前30只股票（用户自己定义）
    b = Sort_threshold('data_growth.txt', '2.txt', 'nprg')
    # 各自取前1000只股票求交集，排序方式为后面的参数(俩个指标都是从大到小排序)
    b.sort_stock(50,'sort-')
