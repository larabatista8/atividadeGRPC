from concurrent import futures
import uuid
import grpc
import tarefa_pb2
import tarefa_pb2_grpc

class TarefaServicer(tarefa_pb2_grpc.GerenciarTarefasServicer):
    def __init__(self):
        self.bd_tarefas= {}

    def CriarTarefa(self, request, context):
        #cria id, converte pra string e cria dicionario com os dados
        id_uuid = uuid.uuid4()
        id_str = str(id_uuid)
        #extrai dados da request
        tarefa = tarefa_pb2.Tarefa(
        id=id_str,
        titulo=request.titulo,
        descricao=request.descricao,
        status=request.status,
        dataLimite=request.dataLimite,
        responsavel=request.responsavel
    )
        #salva tarefa
        self.bd_tarefas[id_str]=tarefa

        return tarefa

    def ListarTarefas(self, request, context):
        lista = tarefa_pb2.ResponseListarTarefas()
    # percorre os item do dicionario
        for item in self.bd_tarefas.values():
            lista.tarefa.append(item)
        return lista

    def AtualizarTarefa(self, request, context):
            return ""

    def DeletarTarefa(self, request, context):
                return ""

    #configura o servidor
def serve():
          server = grpc.server(futures.ThreadPoolExecutor(max_workers =10)) 
          tarefa_pb2_grpc.add_GerenciarTarefasServicer_to_server(TarefaServicer(),server)
          server.add_insecure_port('0.0.0.0:50051')
          server.start()
          server.wait_for_termination()

if __name__ == "__main__" :
    serve()
    