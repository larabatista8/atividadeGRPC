import time
import grpc
import tarefa_pb2
import tarefa_pb2_grpc

# conectando no server
canal = grpc.insecure_channel('192.168.50.10:50051')
stub = tarefa_pb2_grpc.GerenciarTarefasStub(canal)

print("teste criar tarefa")
req_criar = tarefa_pb2.RequestCriarTarefa(
    titulo="fazer trabalho de sd",
    descricao="terminar as funcoes",
    status="fazendo",
    dataLimite="amanha",
    responsavel="alexsandra e larissa"
)
tarefa_nova = stub.CriarTarefa(req_criar)
print("criou a tarefa com id:", tarefa_nova.id)

print("\ntestando listar")
req_listar = tarefa_pb2.RequestListarTarefas()
lista = stub.ListarTarefas(req_listar)
for t in lista.tarefa:
    print(t.id, "-", t.titulo, "-", t.status)

print("\ntestando atualizar")
tarefa_nova.status = "pronto"
tarefa_nova.descricao = "finalizado as rotas"
atualizou = stub.AtualizarTarefa(tarefa_nova)
print("status:", atualizou.status)

print("\n testando deletar")
req_del = tarefa_pb2.RequestDeletarTarefa(id=tarefa_nova.id)
deletou = stub.DeletarTarefa(req_del)

if deletou.concluido:
    print("apagou")
else:
    print("nao achou para apagar")
    
print("\nlista final")
lista_final = stub.ListarTarefas(req_listar)
print(lista_final)
