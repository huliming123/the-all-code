import numpy as np
import pandas as pd
import os

def write_txt(final_data, name_txt):
    # final_data = final_data[['code', 'name', self.target]]
    # 文件名
    file_name = 'data/{}.txt'.format(str(name_txt))
    # 当前目录如果有相同名字的文件，删除该文件
    if os.path.exists(file_name):
        os.remove(file_name)
    try:
        # 特征名
        cols = list(final_data.columns)
        indexs=list(final_data.index)
        name=''
        for col in cols:
            name=name+col+'\t'
        name=name+'\n'
        # name = str(col[0]) + '\t' + str(col[1]) + '\t' + str(col[2]) + '\t' + '\n'
        with open(file_name, 'a') as f:
            f.write(name)
        final_data_array = final_data.values
        # 将数据写入txt文件里面

        for stock,index in zip(final_data_array,indexs):
            row = index+'\t'+''
            for i in stock:
                row = row +str(i)+'\t'
            row = row + '\n'
            # row = str(stock[0]) + '\t' + str(stock[1]) + '\t' + str(stock[2]) + '\t' + '\n'
            with open(file_name, 'a') as f:
                f.write(row)
    except Exception as e:
        print(e)
    return 'ok'
