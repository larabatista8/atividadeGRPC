import time
import grpc
import tarefa_pb2
import tarefa_pb2_grpc

canal = grpc.insecure_channel('192.168.50.10:50051')
stub = tarefa_pb2_grpc.GerenciarTarefasStub(canal)

print("teste cliente2")

req_criar2 = tarefa_pb2.RequestCriarTarefa(
    titulo="Trabalho de Cripto",
    descricao="Desenvolver Cifra de Playfair",
    status="Em andamento",
    dataLimite="segunda",
    responsavel="alexsandra"
)

tarefa_nova2 = stub.CriarTarefa(req_criar2)
print("criou a tarefa com id:", tarefa_nova2.id)

time.sleep(2)

print("\ntestando listar do cliente 2")
req_listar = tarefa_pb2.RequestListarTarefas()
lista = stub.ListarTarefas(req_listar)

for t in lista.tarefa:
    print(t.id, "-", t.titulo, "-", t.responsavel)

print("\nteste cliente2 finalizado")