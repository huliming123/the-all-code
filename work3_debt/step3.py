import pandas as pd
import numpy as np
import pickle
import matplotlib.pyplot as plt
import matplotlib

def save_stocks(final_data_pandas):
    # 按照综合指标从小到大进行排序
    final_data_sort=final_data_pandas.sort_values(by='debt_values',ascending=False).iloc[:300]
    return final_data_sort
    # print(final_data_sort)
    # plt.title('stocks_sort')
    # plt.xlabel('code')
    # plt.ylabel('debt_values')
    # final_data_sort_plt=pd.DataFrame(final_data_sort[['code','debt_values']].values,columns=['code','debt_values'])
    # x=final_data_sort_plt.values[:10,0]
    # height=final_data_sort_plt.values[:10,1]
    # # 斜体,观察更加好
    # plt.gcf().autofmt_xdate()
    # plt.bar(x,height,color='r',label='debt_values')
    # plt.legend()
    # plt.show()
    # with open('step4/final_data_sort.pkl','wb') as f:
    #     pickle.dump(final_data_sort,f)
    # num=0
    # for yangben in final_data_sort.values:
    #     num+=1
    #     name=str(yangben[0])+'\t'+str(yangben[1])+'\t'+str('%.3f'%yangben[2])+'\n'
    #     with open('step3/the_result.txt','a') as f:
    #         if yangben[0]==final_data_sort.values[0][0]:
    #             f.write('code' + '\t' + 'name' + '\t' + 'debt_values' + '\n')
    #         f.write(name)
    #     if num==300:
    #         break

if __name__=='__main__':
    with open('step3/final_data_pandas.pkl','rb') as f:
        data=pickle.load(f)
        data=save_stocks(data)
        print(data)


        # data=data.iloc[:30]
        # from pyecharts import Line
        # attr = list(data['name'])
        # print(attr)
        # v1 = list(data['debt_values'])
        # line = Line("综合偿债能力前30的股票排名",width=1200,height=600)
        # line.add("", attr, v1, mark_point=["average", "max", "min"],
        #          mark_point_symbol='diamond', mark_point_textcolor='#40ff27')
        # line.render(path='stocks_debt_values.html')
