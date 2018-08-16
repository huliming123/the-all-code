import numpy as np
import pandas as pd


# 打分
def my_sigmoid(x):
    return 1 / (1 + np.exp(-x))


# 均值标准化
def my_scale(data):
    if data.mean() == 0:
        return pd.DataFrame(np.zeros(data.shape), columns=data.columns)
    else:
        return (data - data.mean()) / data.mean()


def method_scores(data, *args):
    '''
        :param data: DataFrame格式的数据
        :param args: 元组,布尔类型的值，True表示相应的指标值越大，该指标越好;False表示相应的指标值越小越好。
        :return: 返回每个行业排名在前num1位置的好股票
    '''
    cols = data.columns
    final_data = pd.DataFrame()
    if len(cols) - 3 != len(args[0]):
        print('参数出错，重新输入')
        return ''
    for c_name, industry_data in data.groupby('c_name'):
        M, num = [], 1
        for my_bool in args[0]:
            num += 1
            if my_bool:
                M.append(my_scale(industry_data.values[:, num]))
            if not my_bool:
                M.append(-1 * (my_scale(industry_data.values[:, num])))
        industry_data_scale = np.array(M).T.astype('f4')
        data_score = my_sigmoid(industry_data_scale)
        industry_data.values[:, 2:-1] = data_score
        new_data = pd.DataFrame(industry_data, columns=cols)
        new_data['scores'] = data_score.sum(axis=1) / (len(cols)-3)
        final_data = pd.concat((final_data, new_data))
    return final_data


def final_score(data, num1, index_dict):
    '''
    :param data: DataFrame格式的数据
    :param num1: 每个行业取出的排名前num1数量
    :param index_dict: 不同维度的指标字典
    :return: 返回每个行业排名在前num1位置的好股票
    '''
    columns = data.columns
    final_df = pd.DataFrame()
    count = 0
    for key, value in index_dict.items():
        # 选取该维度列名
        cols = data.columns[:2].tolist()
        cols.extend(value)
        cols.extend([data.columns[-1]])
        tmp_df = data.loc[:, cols]
        # print(tmp_df)
        # 计算该维度得分
        tmp_score = method_scores(tmp_df, [True] * len(value))
        tmp_score.rename(columns={'scores': key}, inplace=True)
        if count == 0:
            final_df = tmp_score.loc[:, [columns[0], key]]

        else:
            final_df = pd.merge(final_df, tmp_score.loc[:, [columns[0], key]], how='left', on=columns[0])
        count += 1
    # 各维度得分求均值
    final_df = pd.concat((final_df.iloc[:,0], final_df.iloc[:,1:].mean(axis=1)), axis=1)

    final_df.to_excel('1111.xlsx')
    final_df.rename(columns={0:'score'}, inplace=True)
    score = pd.merge(data, final_df, on=columns[0])
    final_data = pd.DataFrame()
    # 根据行业进行分组，并按照得分排序
    for c_name, industry_data in score.groupby('c_name'):
        new_data = industry_data.sort_values(by='score', ascending=False)
        new_data = new_data.iloc[:num1]
        final_data = pd.concat((final_data, new_data))
    return final_data


def transform_data():
    Financial_data = pd.read_excel(r'C:\Users\Administrator\Desktop\cp_hulimin\thrif_api\Financial_data.xlsx', 'sheet1')
    # print(Financial_data)
    index_dict = {'偿债能力': ['流动比率', '速动比率'],
                  '营运能力': ['应收账款周转率', '存货周转率', '流动资产周转率'],
                  '盈利能力': ['销售毛利率', '净资产收益率', '总资产净利润'],
                  '成长能力': ['营业收入同比增长率', '净利润同比增长率', '净资产同比增长率'],
                  '现金流量': ['资产的经营现金流量回报率', '经营现金净流量与净利润的比率']}

    data = final_score(Financial_data, 20, index_dict)
    return data


def transform_post():
    Financial_data = pd.read_excel(r'C:\Users\Administrator\Desktop\cp_hulimin\thrif_api\Financial_data.xlsx', 'sheet1')
    cols = list(Financial_data.columns)
    values = Financial_data.values
    d = {}
    for i in cols:
        d[i] = values[:,cols.index(i)].tolist()
    return d


if __name__ == '__main__':
    Financial_data = pd.read_excel(r'C:\Users\Administrator\Desktop\cp_hulimin\thrif_api\Financial_data.xlsx', 'sheet1')
    index_dict = {'偿债能力': ['流动比率', '速动比率'],
                  '营运能力': ['应收账款周转率', '存货周转率', '流动资产周转率'],
                  '盈利能力': ['销售毛利率', '净资产收益率', '总资产净利润'],
                  '成长能力': ['营业收入同比增长率', '净利润同比增长率', '净资产同比增长率'],
                  '现金流量': ['资产的经营现金流量回报率', '经营现金净流量与净利润的比率']}

    print(final_score(Financial_data, 20, index_dict))
    # print(transform_post())
