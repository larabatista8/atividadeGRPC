from concurrent import futures
import uuid
import os
import json

import grpc
import tarefa_pb2
import tarefa_pb2_grpc

PASTA_TAREFAS = "tarefas"

class TarefaServicer(tarefa_pb2_grpc.GerenciarTarefasServicer):
    def __init__(self):
        self.bd_tarefas = {}

        # cria a pasta e carrega as tarefas salvas
        os.makedirs(PASTA_TAREFAS, exist_ok=True)
        for arquivo in os.listdir(PASTA_TAREFAS):
            if arquivo.endswith(".json"):
                caminho = os.path.join(PASTA_TAREFAS, arquivo)

                with open(caminho, "r", encoding="utf-8") as f:
                    dados = json.load(f)
                tarefa = tarefa_pb2.Tarefa(
                    id=dados["id"],
                    titulo=dados["titulo"],
                    descricao=dados["descricao"],
                    status=dados["status"],
                    dataLimite=dados["dataLimite"],
                    responsavel=dados["responsavel"]
                )
                self.bd_tarefas[tarefa.id] = tarefa

    def salvar_arquivo(self, tarefa):
        dados = {
            "id": tarefa.id,
            "titulo": tarefa.titulo,
            "descricao": tarefa.descricao,
            "status": tarefa.status,
            "dataLimite": tarefa.dataLimite,
            "responsavel": tarefa.responsavel
        }
        caminho = os.path.join(PASTA_TAREFAS, tarefa.id + ".json")
        with open(caminho, "w", encoding="utf-8") as f:
            json.dump(dados, f, ensure_ascii=False, indent=2)

    def CriarTarefa(self, request, context):
        # cria id
        id_uuid = uuid.uuid4()
        id_str = str(id_uuid)
        print('\nCriando tarefa ', id_str)
        tarefa = tarefa_pb2.Tarefa(
            id=id_str,
            titulo=request.titulo,
            descricao=request.descricao,
            status=request.status,
            dataLimite=request.dataLimite,
            responsavel=request.responsavel
        )
        # salva tarefa
        self.bd_tarefas[id_str] = tarefa
        self.salvar_arquivo(tarefa)
        print('Tarefa criada!')
        return tarefa

    def ListarTarefas(self, request, context):
        lista = tarefa_pb2.ResponseListarTarefas()
    # percorre os item do dicionario
        print('\nListando tarefas...')
        for item in self.bd_tarefas.values():
            lista.tarefa.append(item)
        return lista

    def AtualizarTarefa(self, request, context):
        # ve se o id existe no dicionario
        print(f'\nVerificando se tarefa {request.id} está no banco...')
        if request.id in self.bd_tarefas:
            self.bd_tarefas[request.id] = request
            self.salvar_arquivo(request)
            print('Tarefa atualizada!')
            return request
        else:
            print('Tarefa não encontrada! :(')
            return tarefa_pb2.Tarefa()

    def DeletarTarefa(self, request, context):
        # tenta achar o id pra apagar
        print(f'\nVerificando se tarefa {request.id} está no banco...')
        if request.id in self.bd_tarefas:
            del self.bd_tarefas[request.id]
            caminho = os.path.join(PASTA_TAREFAS, request.id + ".json")
            if os.path.exists(caminho):
                os.remove(caminho)
            print('\nTarefa deletada com sucesso!')
            return tarefa_pb2.ResponseDeletarTarefa(concluido=True)
        else:
            print('\nTarefa não encontrada! :(')
            return tarefa_pb2.ResponseDeletarTarefa(concluido=False)


# configura o servidor
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    tarefa_pb2_grpc.add_GerenciarTarefasServicer_to_server(TarefaServicer(), server)
    server.add_insecure_port('0.0.0.0:50051')
    print("Servidor está funcionando!")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    serve()