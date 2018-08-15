import csv
import numpy as np
import pandas as pd
def read_owntxt(txt_path):
    M=[]
    with open('{}'.format(txt_path),'r') as f:
        for i in csv.reader(f):
            M.append(i[0].split('\t')[:-1])

    data=np.array(M)
    cols=data[0]
    data_pd=pd.DataFrame(data[1:,:2],columns=data[0][:2])
    num=2
    for col in cols[2:]:
        data_pd[col]=data[1:,num].astype('f4')
        num+=1
    print(data_pd)
    return data_pd


if __name__=='__main__':
    read_owntxt('data_debt.txt').to_excel('my.xlsx')


# for stock in data:
