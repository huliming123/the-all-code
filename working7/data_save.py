import tushare as ts
import pickle
import pandas as pd
import numpy as np
def save_data(data,file_path):
    with open(file_path,'wb') as f:
        pickle.dump(data,f)
        print('ok')
def save_data2():
    pass



if __name__=='__main__':
    with open('data_pkl/data_growth','rb') as f:
        data=pickle.load( f)
        data=data.drop_duplicates('code')
        cols=data.columns

    industry_data=ts.get_industry_classified()
    industry_data=industry_data.drop_duplicates('code')
    industry_data=pd.DataFrame(industry_data.values[:,1:],index=industry_data['code'],columns=industry_data.columns[1:])
    print(industry_data)
    M=[]
    for code in data['code']:
        try:
            M.append(industry_data['c_name'][code])
        except Exception as e:
            M.append(0)
    data['c_name']=M
    print(data.values)
    W=[]
    for stock in data.values:
        if 0 not in stock:
            W.append(stock)
    data=np.array(W)
    data_pd=pd.DataFrame(data,columns=list(cols)+['c_name'])
    print(data_pd)
    with open('input_data','wb') as f:
        pickle.dump(data_pd,f)
        print('ok')











