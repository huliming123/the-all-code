import json
from datetime  import datetime
from thrif_api.gen_data import transform_post
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from thrif_api.thrift_file.gen_py.example.format_data import Client
from thrif_api.thrift_file.gen_py.example.format_data import Data

__HOST = '192.168.1.113'
__PORT = 8080

index_dict = {'偿债能力': ['流动比率', '速动比率'],
              '营运能力': ['应收账款周转率', '存货周转率', '流动资产周转率'],
              '盈利能力': ['销售毛利率', '净资产收益率', '总资产净利润'],
              '成长能力': ['营业收入同比增长率', '净利润同比增长率', '净资产同比增长率'],
              '现金流量': ['资产的经营现金流量回报率', '经营现金净流量与净利润的比率']}
num =20


final_data = transform_post()
data = {
    "data" : final_data,
    "index_dict" : index_dict,
    "num" : num,
}

# 创建socket
tsocket = TSocket.TSocket(__HOST, __PORT)

# 设置缓存
transport = TTransport.TBufferedTransport(tsocket)

# 包裹协议
protocol = TBinaryProtocol.TBinaryProtocol(transport)

# 用协议建立客户端对象
client = Client(protocol)

time1 = datetime.now()
# 建立连接
transport.open()

data = Data(json.dumps(data, ensure_ascii=False))

print(client.do_format(data).text)
time2 = datetime.now()
print((time2-time1).seconds)