# Sistema de Gerenciamento de Tarefas com gRPC

## Integrantes
- Alexsandra da Costa Andrade  
- Larissa Batista dos Santos  
- Ruslan Andruscha Duete Lima Moreira  
- Éricles Barros de Sá

## Descrição
Este projeto é um sistema de gerenciamento de tarefas utilizando a arquitetura Cliente-Servidor com **gRPC** e **Protocol Buffers** em Python. O servidor oferece as operações básicas de CRUD (Criar, Listar, Atualizar, Deletar) para as tarefas.

O projeto conta com duas implementações de servidor:
- `servidor.py`: Armazena as tarefas apenas em memória.
- `servidor_pers_arq.py`: Persiste as tarefas salvando-as em arquivos JSON dentro da pasta `tarefas/`.

## Pré-requisitos
- Python 3.x instalado
- Dependências do gRPC

Para instalar as dependências necessárias, execute o comando:
```bash
pip install grpcio grpcio-tools
```

## Configuração de IP (Localhost vs VirtualBox)
O servidor está configurado para escutar conexões em todas as interfaces de rede na porta 50051 (`0.0.0.0:50051`).

Por padrão, os arquivos de cliente (`cliente.py`, `cliente2.py`, `cliente_menu.py`) estão tentando se conectar a um servidor rodando no IP `192.168.50.10:50051` (provavelmente uma configuração de rede de máquina virtual).

### 1. Rodando na mesma máquina (Localhost)
Se você for executar tanto o servidor quanto o cliente na mesma máquina, você precisará alterar os arquivos dos clientes.
Abra os arquivos `cliente.py`, `cliente2.py` e `cliente_menu.py` e mude a seguinte linha:
```python
canal = grpc.insecure_channel('192.168.50.10:50051')
```
Para usar o localhost:
```python
canal = grpc.insecure_channel('localhost:50051')
```

### 2. Rodando com Múltiplas Máquinas Virtuais (VirtualBox - Rede Interna)
Este projeto foi idealizado e pode ser perfeitamente testado usando várias máquinas virtuais (por exemplo, 3 VMs: 1 atuando como Servidor e 2 como Clientes). Para essa configuração:
1. No VirtualBox, defina o adaptador de rede de **todas as 3 máquinas virtuais** como **"Rede Interna"** (Internal Network), garantindo que usem o mesmo nome de rede (ex: `intnet`).
2. Configure os IPs manualmente dentro do sistema operacional de cada máquina para que pertençam à mesma sub-rede. Exemplo de topologia:
   - **VM 1 (Servidor):** `192.168.50.10`
   - **VM 2 (Cliente 1):** `192.168.50.11`
   - **VM 3 (Cliente 2):** `192.168.50.12`
3. Nas VMs que atuarão como cliente, garanta que os arquivos (`cliente.py`, `cliente2.py`, `cliente_menu.py`) apontem especificamente para o IP que você deu à VM do servidor:
```python
canal = grpc.insecure_channel('192.168.50.10:50051')  # IP manual configurado no servidor
```

## Como Executar

### Passo 1: Iniciar o Servidor
Abra um terminal na pasta do projeto e inicie o servidor. Você pode escolher a versão com ou sem persistência:

**Sem persistência (apenas memória):**
```bash
python servidor.py
```

**Com persistência (salva em arquivos):**
```bash
python servidor_pers_arq.py
```
*(O terminal ficará bloqueado mostrando que o servidor está funcionando)*

### Passo 2: Iniciar o Cliente
Abra um **novo terminal**, navegue novamente até a pasta do projeto e inicie a interface de menu:
```bash
python cliente_menu.py
```
A partir do menu interativo no terminal, você poderá escolher as opções digitando os números para interagir com o sistema.

Para testar as operações sem o menu interativo, você também pode executar os scripts de teste:
```bash
python cliente.py
# ou
python cliente2.py
```