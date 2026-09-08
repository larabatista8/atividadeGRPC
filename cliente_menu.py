import grpc
import tarefa_pb2
import tarefa_pb2_grpc
import subprocess
import os

canal = grpc.insecure_channel('192.168.50.10:50051')
stub = tarefa_pb2_grpc.GerenciarTarefasStub(canal)

while True:
    subprocess.run('cls' if os.name == 'nt' else 'clear', shell=True)

    print("1 - Criar uma nova tarefa")
    print("2 - Listar tarefas")
    print("3 - Atualizar tarefa")
    print("4 - Deletar tarefa")
    print("5 - Sair")
    
    opcao = input("Digite o número da opção desejada: ").strip()

    if opcao == '1':
        print("\nNova Tarefa: ")
        tit = input("Titulo: ")
        desc = input("Descricao: ")
        stat = input("Status: ")
        data = input("Data: ")
        resp = input("Responsavel: ")
        
        req = tarefa_pb2.RequestCriarTarefa(
            titulo=tit, 
            descricao=desc, 
            status=stat, 
            dataLimite=data, 
            responsavel=resp
        )
        resposta = stub.CriarTarefa(req)
        print("criou uma tarefa com id:", resposta.id)
        input("\nAperte Enter pra continuar")

    elif opcao == '2':
        print("\nTarefas existentes:")
        req = tarefa_pb2.RequestListarTarefas()
        lista = stub.ListarTarefas(req)
        if len(lista.tarefa) == 0:
            print("Ainda não tem nenhuma tarefa cadastrada")
        else:
            for t in lista.tarefa:
                print("ID:", t.id)
                print("Titulo:", t.titulo)
                print("Status:", t.status)
                print("Responsavel:", t.responsavel)
        input("\nAperte Enter pra continuar")

    elif opcao == '3':
        print("\nAtualizar Tarefa:")
        id_alvo = input("ID da tarefa: ")
        tit = input("Titulo: ")
        desc = input("Descricao: ")
        stat = input("Status: ")
        data = input("Data: ")
        resp = input("Responsavel: ")
        
        req = tarefa_pb2.Tarefa(
            id=id_alvo, 
            titulo=tit, 
            descricao=desc, 
            status=stat, 
            dataLimite=data, 
            responsavel=resp
        )
        atualizou = stub.AtualizarTarefa(req)
        
        if atualizou.id:
            print("atualização concluida")
        else:
            print("tarefa não encontrada")
        input("\nAperte Enter pra continuar")

    elif opcao == '4':
        print("\ntarefa excluida!")
        id_del = input("ID da tarefa pra apagar: ")
        req = tarefa_pb2.RequestDeletarTarefa(id=id_del)
        deletou = stub.DeletarTarefa(req)
        
        if deletou.concluido:
            print("apagado!")
        else:
            print("nao encontrado para apagar!")

        input("\nAperte Enter pra continuar")

    elif opcao == '5':
        print("saindo!")
        break
        
    else:
        print("opção invalida")
        input("\nAperte Enter pra continuar")