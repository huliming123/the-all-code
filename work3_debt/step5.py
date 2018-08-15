# 0.039*上汽集团+0.056*中国神华+0.003*中国石化+0.271*农业银行+0.631
# *工商银行

# 导入函数库
# import jqdata

# def initialize(context):
#     # 每天执行period函数
#     run_daily(period,time='every_bar')
#     # 股票代码是这个
#     g.security = '000001.XSHE'
#
# # 循环周期，购买000001股票100股
# def period(context):
#     order(g.security,100)

#   def initialize(context):
#       run_daily(period,time='every_bar')
#       # 代码：设定好要交易的股票数量stocksnum
#
#   def period(context):
#       # 代码：找出市值排名最小的前stocksnum只股票作为要买入的股票
#       # 代码：若已持有的股票的市值已经不够小而不在要买入的股票中，则卖出这些股票。
#       # 代码：买入要买入的股票，买入金额为可用资金的stocksnum分之一


# # 0.039*上汽集团+0.056*中国神华+0.003*中国石化+0.271*农业银行+0.631 *工商银行




# [['000416' 0.15504336919953637]
#  ['000722' 0.20395813651028555]
#  ['600506' 0.10064878823801143]
#  ['000813' 0.04408714645622606]
#  ['000616' 0.06095751078595749]
#  ['300018' 0.3271157954813233]
#  ['600527' 0.022843426798885447]
#  ['002802' 0.08534582652976774]]
# XSHE:深圳交易所上市
# XSHG:上海交易所上市
import numpy as np
def initialize(context):
    # 每天执行period函数
    run_daily(period,time='every_bar')
    # 股票代码是这个
    g.security = ['000416.XSHE','000722.XSHE','600506.XSHG','000813.XSHE','000616.XSHE','300018.XSHE','600527.XSHG']
    g.security2=np.array([0.16976999, 0.22343921, 0.10952903, 0.04819277, 0.06681271,
       0.35815991, 0.02409639])
    g.period=30
    g.days=0



def period(context):
    
        position_per_stk =(context.portfolio.cash)*g.security2
        num=-1
        for stock in g.security:
            num+=1
            order_value(stock,position_per_stk[num])
    

























