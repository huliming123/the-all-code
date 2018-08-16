from __future__ import print_function
import json
import grpc
from datetime import datetime
import hello_pb2
import hello_pb2_grpc
from gen_data import transform_post


final_data = json.dumps(transform_post(), ensure_ascii=False)


index_dict = json.dumps({'偿债能力': ['流动比率', '速动比率'],
              '营运能力': ['应收账款周转率', '存货周转率', '流动资产周转率'],
              '盈利能力': ['销售毛利率', '净资产收益率', '总资产净利润'],
              '成长能力': ['营业收入同比增长率', '净利润同比增长率', '净资产同比增长率'],
              '现金流量': ['资产的经营现金流量回报率', '经营现金净流量与净利润的比率']}, ensure_ascii=False)
num = 20



def run():
    time1 = datetime.now()
    channel = grpc.insecure_channel('192.168.1.113:8080')
    stub = hello_pb2_grpc.GreeterStub(channel)
    response = stub.SayHello(hello_pb2.HelloRequest(
        index=index_dict,
        data= final_data,
        num=num
    ))
    print(response.final_data)
    time2 = datetime.now()
    print((time2-time1).seconds)


if __name__ == '__main__':
    run()
    # pass