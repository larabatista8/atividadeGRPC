from concurrent import futures
import time

import grpc
import greet_pb2
import greet_pb2_grpc

class GeetServicer(greet_pb2_grpc.GreeterSErvicer):
    def SayHello(self, request, context):
        return super().SayHello(request, context)

    def ParrotSaysHello(self, request, context):
            return super().ParrotSaysHello(request, context)

    def ChattyClientSaysHello(self, request, context):
            return super().ChattyClientSaysHello(request, context)

    def InteractingHello(self, request, context):
                return super().InteractingHello(request, context)

    #configura o servidor
    def serve():
          server = grpc.Server(futures.ThreadPoolExecutor(max_workers =10)) 
          greet_pb2.grpc.add_GreetServicer_to_server(GreeterServicer(),server)
          server.add_insecure_port('localhost:50051')
          server.start()
          server.wait_for_termination()

    if __name__ == "__main__" :
        serve()
    