from concurrent import futures
import time
import json
import grpc
import pandas as pd
from gen_data import final_score
from utils import transform_to_list
import hello_pb2
import hello_pb2_grpc

_ONE_DAY_IN_SECONDS = 60 * 60 * 24


class Greeter(hello_pb2_grpc.GreeterServicer):
    # 工作函数
    def SayHello(self, request, context):
        num = request.num
        index_dict = json.loads(request.index)
        data = json.loads(request.data)
        Financial_data = pd.DataFrame(data)
        data = final_score(Financial_data, num, index_dict)

        return hello_pb2.HelloReply(final_data=json.dumps(transform_to_list(data), ensure_ascii=False))


def serve():
    # gRPC 服务器
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    hello_pb2_grpc.add_GreeterServicer_to_server(Greeter(), server)
    server.add_insecure_port('[::]:8080')
    server.start()  # start() 不会阻塞，如果运行时你的代码没有其它的事情可做，你可能需要循环等待。
    print('服务器已经开启，等待连接......')
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    serve()
