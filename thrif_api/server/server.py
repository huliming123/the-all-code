import json
import pandas as pd
from thrif_api.gen_data import final_score
from thrif_api.utils import transform_to_list
from thrif_api.thrift_file.gen_py.example import format_data
from thrif_api.thrift_file.gen_py.example import ttypes
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from thrift.server import TServer

__HOST = '192.168.1.113'
__PORT = 8080


class FormatDataHandler(object):
    def do_format(self, data):
        d = json.loads(data.text)

        data = d['data']
        num = d['num']
        index_dict = d['index_dict']
        # print(index_dict)
        Financial_data = pd.DataFrame(data)
        data = final_score(Financial_data, num, index_dict)
        return ttypes.Data(json.dumps({"data": transform_to_list(data)}, ensure_ascii=False))


if __name__ == '__main__':
    handler = FormatDataHandler()

    processor = format_data.Processor(handler)
    transport = TSocket.TServerSocket(__HOST, __PORT)
    tfactory = TTransport.TBufferedTransportFactory()
    pfactory = TBinaryProtocol.TBinaryProtocolFactory()

    rpcServer = TServer.TSimpleServer(processor,transport, tfactory, pfactory)

    print('Starting the rpc server at', __HOST,':', __PORT)
    rpcServer.serve()
