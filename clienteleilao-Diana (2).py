# -*- coding: cp1252 -*-
# Echo client program
import socket



def menu_principal():
    global o
    o = 0
    o = eval(raw_input ('Digite:\n 1- Para cadastrar um usuario \n 2- Para fazer login \n 3- Para listar produtos \n 0- Para sair '))
    o = int(o)
    
def menu_logado():
    global l
    l = 0
    l = eval(raw_input ('Digite:\n 1- Apagar o usuario \n 2- Para lançar produto \n 3- Entrar no leilao/enviar lance \n 4- Sair do leilao \n 5- Para listar produtos \n 0- Para sair '))
    l = int(l)

HOST = '127.0.0.1'    #IP da mesma maquina
PORT = 50136             # porta do servidor para comunicação
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #IPv4,tipo de socket
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.connect((HOST, PORT))  #Abre uma conexão com IP e porta especificados
print "Conectou"

HOST1 = '127.0.0.1'    #IP da mesma maquina
PORT1 = 50137             # porta do servidor para comunicação
s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #IPv4,tipo de socket
s1.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s1.connect((HOST1, PORT1))  #Abre uma conexão com IP e porta especificados
print "Conectou2"
#receber o dado do usuario

'''
o = raw_input ('Digite:\n 1- Para cadastrar um usuario \n 2- Para fazer login \n 3- Para listar produtos \n 0- Para sair ')
o = int(o)  '''
while True:

    menu_principal()
    
#recebe o dado do usuario 
    if o==1:
        print ('Cadastro de cliente')
        #CADASTRO DO CLIENTE 
        n = raw_input (" Digite o nome")
        t = raw_input ("Digite o número de telefone")
        e = raw_input ("Digite seu endereço")
        m = raw_input ("Digite seu email")
        se = raw_input ("Digite a senha")
        s.sendall("adiciona_usuario,"+n+","+t+","+e+","+m+","+se) #Envia dados
        print "Enviou e está esperando receber"
        data = s.recv(1024) #Recebe dados
        print 'Received', repr (data)
        menu_principal()
        #retirei pq o servidor que vai falar se foi ou nao
    '''
    except Exception,err:
        print('Erro ao cadastrar')
        print err
    else:
        print('Cadastrado com sucesso!')'''
        
    if o==2:
        try:
               
            print ('Autenticaçao')
        
            n = raw_input (" Digite o nome")
            se = raw_input ("Digite a senha")
            s.sendall("faz_login,"+n+","+se) #Envia dados
            print "Enviou e está esperando receber"
            data = s.recv(1024) #Recebe dados
            print 'Received', repr (data)
            menu_logado()
        
                
        except Exception,err:    
            print('Erro ao autenticar')
            menu_principal()
        else:
            print('Login efetuado com sucesso!')        
            
    if o==3:
        try:
               
            print ('Lista de produtos')
        
            s.sendall("listar_leiloes") #Envia dados
            print "Enviou e está esperando receber"
            data = s.recv(4096) #Recebe dados
            msgr=data.split('(')
            for i in msgr:
                print 'Received', repr (i)
                #print 'Received', repr (data)
            
            menu_principal()
        except Exception,err:    
            print('Erro ao receber a lista')
            menu_principal()
        else:
            print('Fim da lista!')
            menu_principal()
    if o==0:
        try:
               
            print ('Adios')
        
            s.sendall("tchau,"+n) #Envia dados
            print "Enviou e está esperando receber"
            data = s.recv(1024) #Recebe dados
            print 'Received', repr (data)
            s.close() #Termina conexão
            print "Fechou a conexão"
        except Exception,err:    
            print('Erro ao dar tchau')
            
    if l==0:
        try:
            print ('Adios')
            
            s.sendall("tchau,"+n) #Envia dados
            print "Enviou e está esperando receber"
            data = s.recv(1024) #Recebe dados
            print 'Received', repr (data)
            s.close() #Termina conexão
            print "Fechou a conexão"
        except Exception,err:    
            print('Erro ao dar tchau')
            
    if l== 1:
        try:
            print('Você escolheu a opção de excluir o usuário')
            decide = str(raw_input (" Digite 's' para confirmar e 'n' para declinar!"))
            if decide=='s':
                s.sendall("apaga,"+n+","+se)#envia dados
                data=s.recv(1024)#espera receber um ok ou um not_ok
                print 'Received', repr (data)
            
                menu_principal()
            else:
                menu_logado()
        except Exception,err:    
            print('Erro ao excluir')            
    if l==2:
        try:
            print('Você escolheu a opção lançar um produto')
            decide = str(raw_input (" Digite 's' para confirmar e 'n' para declinar!"))
            if decide=='s':
                np = raw_input (" Digite o nome do produto")
                dc = raw_input ("Digite a descrição do produto")
                lmin = raw_input ("Digite o lance mínimo do produto")
                ano= raw_input("Digite o ano do leilão")#por enquanto não vou enviar esses dados, pq o banco de dados não está recebendo isso
                mes= raw_input("Digite o mes do leilão")
                dia=raw_input("Digite o dia do leilão")
                hora=raw_input("Digite a hora do leilao")
                minuto=raw_input("Digite os minutos")
                seg= raw_input("Digite os segundos")
                diahora= ano+"/"+mes+"/"+dia+"/"+hora+":"+minuto+":"+seg
                print(diahora)
                s.sendall("lanca,"+np+","+dc+","+lmin+","+diahora+","+n)#envia nome do produto, descrição do produto e lance minimo
                data=s.recv(1024)#espera receber um ok ou um not_ok
                print 'Received', repr (data)
                menu_logado()
            else:
                menu_logado()#não sei se vai funcionar
        except Exception,err:    
            print('Erro ao lançar o produto')            
    if l==3:
        try:
            print('Você escolheu a opção entrar no leilao') #essa função ainda nao está no servidor
            decide = str(raw_input (" Digite 's' para confirmar e 'n' para declinar!"))
            if decide=='s':
                codigo = raw_input (" Digite o id do leilao que deseja entrar")
                s.sendall("entrar_leilao,"+codigo+","+n)#envia entrar
                data=s.recv(1024)#espera receber um ok ou um not_ok
                print 'Received', repr (data)
                while 1:
                    s1.sendall("entrar_leilao,"+codigo)#envia entrar para a porta 2
                    data1=s1.recv(1024)#recebe o valor do lance minimo
                    print 'Received', repr (data1)
                        
                    decide_lance = str(raw_input ("Deseja fazer um lance? Digite 's' para confirmar e 'n' para declinar!"))
                    if decide_lance == 's':
                        lance=str(raw_input (" Digite o seu lance"))
                        s1.sendall("enviar_lance,"+lance+","+n)
                        data2=s1.recv(1024)#recebe os dados da porta do leilao
                        print 'Received', repr (data2)
                        menu_logado()#imprime as opções
                        if l==0:
                            try:
                                
                                print ('Adios')
                                
                                s1.sendall("tchau,"+n) #Envia dados
                                print "Enviou e está esperando receber"
                                data = s1.recv(1024) #Recebe dados
                                print 'Received', repr (data)
                                s1.close() #Termina conexão
                                print "Fechou a conexão"
                            except Exception,err:    
                                print('Erro ao dar tchau')
                            
                    else:
                        s1.sendall("entrar_leilao,")#envia entrar para a porta 2
                        data1=s1.recv(1024)#recebe o valor do lance minimo
                        print 'Received', repr (data1)
                        

                    
                    #menu_logado()#VOLTA PARA O MENU
                    
        except Exception,err:
            print err
            print('Erro ao entrar')

    if l==4:
        try:
            print('Voce escolheu a opção sair do leilão')
            decide = str(raw_input (" Digite 's' para confirmar e 'n' para declinar!"))
            if decide == 's':
                codigo = ("Digite o id do leilao que você deseja sair")
                s.sendall("sair_leilao,"+codigo+","+n)
                sair_leilao()
                data=s.recv(1024) #espera receber um ok ou um not_ok
                print 'Received', repr (data)
            
                menu_logados()

            else:
                menu_logado()
        except Exception, err:
            print('Erro ao sair')

    if l==5:
        try:
               
            print ('Lista de produtos')
        
            s.sendall("listar_leiloes") #Envia dados
            print "Enviou e está esperando receber"
            data = s.recv(4096) #Recebe dados
            msgr=data.split('(')
            for i in msgr:
                print 'Received', repr (i)
                #print 'Received', repr (data)
            
            menu_logado()
        except Exception,err:    
            print('Erro ao receber a lista')
            menu_logado()
        else:
            print('Fim da lista!')
            menu_principal()      
          
