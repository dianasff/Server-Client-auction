# -*- coding: cp1252 -*-
# Echo server program
import socket
import sqlite3, time
import thread
import time
import sys
from threading import Thread, Lock, BoundedSemaphore, Semaphore
from random import random
from datetime import datetime, date, timedelta

global lista  

    
       
def criar_tabela():
    conexao = sqlite3.connect('banco2.db')
    c=conexao.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS cadastro (nome text, telefone varchar,endereco text,email text,senha text)')
    c.execute('CREATE TABLE IF NOT EXISTS produtos(id INTEGER PRIMARY KEY AUTOINCREMENT, nome text, descricao text, lancemin text, data_hora datetime, tmax text, nome_dono text, nome_ganhador text, valor_final text, lance_corrente text, data_criacao text )')
    c.execute('CREATE TABLE IF NOT EXISTS entrar_leilao(id text,nome text)')
    c.execute('CREATE TABLE IF NOT EXISTS logados(nome text, ip text, porta text)')
    
try:
    criar_tabela ()
except:
    print ('Erro ao criar o banco de dados')
else:
    print ('Banco de dados criado com sucesso!')


        
def inserir_cliente(n,t,e,m,s):
    conexao = sqlite3.connect('banco2.db')
    c=conexao.cursor()

    c.execute('INSERT INTO cadastro VALUES(?,?,?,?,?)', (n,t,e,m,s))
    conexao.commit()
        
def inserir_produto(no,dc,lmin,data,n):
    try:        
        conexao = sqlite3.connect('banco2.db')
        c=conexao.cursor()
        d= time.strftime('%d/%m/%Y/%H:%M:%S')
        tmax=40
        c.execute('INSERT INTO produtos (nome,descricao,lancemin,data_hora,tmax,nome_dono,data_criacao) VALUES(?,?,?,?,?,?,?)', (no,dc,lmin,data,tmax,n,d))
        conexao.commit()
    except:
        print('not_ok')
def inserir_logado(n,ih1,ih3):
    conexao = sqlite3.connect('banco2.db')
    c=conexao.cursor()
    c.execute('INSERT INTO logados VALUES(?,?,?)', (n,ih1,ih3))
    conexao.commit()
    
def listar_clientes(conn):
    conexao = sqlite3.connect('banco2.db')
    c=conexao.cursor()
    c.execute('SELECT * FROM cadastro')
    print('Lista de clientes')
    row3 =str(c.fetchall())
    conn.sendall(row3)
    '''for row in c.fetchall():
        print(row)
        #print(row)
        row3=str(row)
        #row2=row3.split(',')
        if row3 == None:
            print('Não há produtos na lista')
        else:
            #for i in row2:
            conn.sendall(row3)'''
def entrar_leilao(id1, n):
    conexao = sqlite3.connect('banco2.db')
    c=conexao.cursor()
    c.execute('INSERT INTO entrar_leilao VALUES(?,?)', (id1,n))
    conexao.commit()
    

def sair_leilao(id1,n,conn):
    conexao = sqlite3.connect('banco2.db')
    c=conexao.cursor()
    c.execute('SELECT * FROM entrar_leilao WHERE id=(?) AND nome=(?)', (id1,n))
    c.execute('DELETE FROM entrar_leilao WHERE id1=(?) AND nome=(?) ', (id1,n))
    print "Você saiu do leilão!"
    conexao.commit()
    conn.sendall('ok')

    
def buscar_leilao(id1):
    conexao = sqlite3.connect('banco2.db')
    c=conexao.cursor()
    sel='SELECT id FROM produtos WHERE id=? '
    
    c.execute(sel,(id1,))
    
    print('Pesquisando cliente:')
    for row in c.fetchall():
        pes=str(row)
        
        print(row)
        if row == id1:
            print('OK')
        
def buscar_hora(id1):
    conexao = sqlite3.connect('banco2.db')
    c=conexao.cursor()
    sel='SELECT data_hora FROM produtos WHERE id=? '
    
    c.execute(sel,(id1,))
    
    print('Pesquisando hora:')
    for row in c.fetchall():
               
        print(row)
        d= time.strftime('%Y/%m/%d/%H:%M:%S')
        newdate1 = datetime.strptime(d, "%Y/%m/%d/%H:%M:%S") 
        newdate2 = datetime.strptime(row[0], "%Y/%m/%d/%H:%M:%S")
        diferenca = (newdate2 - newdate1) #calcula o tempo que falta até  o leilão
        tpl=timedelta.total_seconds(diferenca)
        falta=(tpl-1800)
        '''hora=row[0]
        print hora
        hora_lei = datetime.strptime(hora, "%Y/%m/%d/%H:%M:%S")
        print hora_lei
        dif=(hora-1800)
        hora_leilao=timedelta.total_seconds(dif)
        inicio=(hora_leilao -1800)#calcula o inicio do leilao
        d= time.strftime('%Y/%m/%d/%H:%M:%S')#data corrente
        corrente = datetime.strptime(d, "%Y/%m/%d/%H:%M:%S")
        print ('ok')
        agora_segundos=timedelta.total_seconds(corrente)
        falta= inicio-agora_segundos'''
        if falta >= 0:
            conn.send('not_ok')                
        else:
            print('ok')
    
def listar_produtos(conn):
    conexao = sqlite3.connect('banco2.db')
    c=conexao.cursor()
    lista=[]
    d= time.strftime('%Y/%m/%d/%H:%M:%S')
    newdate1 = datetime.strptime(d, "%Y/%m/%d/%H:%M:%S")
    c.execute('SELECT id,nome, descricao, lancemin, data_hora, tmax, nome_dono FROM produtos')
    for row1 in c.fetchall():
        newdate2 = datetime.strptime(row1[4], "%Y/%m/%d/%H:%M:%S")
        if newdate2>=newdate1:
            print ('ok')
            print('Lista de produtos')
            lista.append(row1)
            row3 =str(c.fetchall())
    envia=str(lista)
    conn.sendall(envia)
    
            
def excluir_cliente(n,s,conn):
    conexao = sqlite3.connect('banco2.db')
    c=conexao.cursor()
    c.execute('DELETE FROM cadastro WHERE nome=? AND senha=? ', (n,s))
    c.execute('DELETE FROM logados WHERE nome=?', (n,))
    print "O  CLIENTE %s FOI EXCLUIDO COM SUCESSO!" %n
    conexao.commit()
    conn.sendall('ok')
    
def alterar_cliente(n):        
    c.execute("UPDATE cadastro SET  telefone = '" + telefone + "',endereco = '" + endereco + "', email = '" + email + "', senha = '" + senha + "' where nome = " + nome + " ")
    print('Atualizando cliente')
    for row in c.fetchall():
        print(row)
def excluir_logados(n):
    conexao = sqlite3.connect('banco2.db')
    c=conexao.cursor()
    c.execute('DELETE FROM logados WHERE nome=?', (n,))
    conexao.commit()
    #c.execute("delete from usuarios where idusuario = " +n+ " ")
    print"O  CLIENTE %s FOI EXCLUIDO COM SUCESSO!" %n
    #, (n,)
    #conn.sendall('ok')
    
def excluir_logados_falha(porta_falha):
    conexao = sqlite3.connect('banco2.db')
    c=conexao.cursor()
    c.execute('DELETE FROM logados WHERE porta=(?)', (porta_falha,))
    print"O  CLIENTE %s FOI EXCLUIDO COM SUCESSO!" %porta_falha
    conexao.commit()
    
def buscar_cliente(n,s): #pode ser parte  do login =D
    conexao = sqlite3.connect('banco2.db')
    c=conexao.cursor()
    sel='SELECT nome, senha FROM cadastro WHERE nome=? AND senha=? '
    
    print('Pesquisando cliente:')
    for row in c.execute(sel,(n,s)):
        print(row)
       
def buscar_nome(n): #faz parte do inserir cliente =D
    conexao = sqlite3.connect('banco2.db')
    c=conexao.cursor()
    sel='SELECT nome FROM cadastro WHERE nome=? '
    #lista=[]
    c.execute(sel,(n,))
    
    print('Pesquisando cliente:')
    for row in c.fetchall():
        pes=str(row)
        #lista.append(pes)
        print(row)
        if row == None:
            print('OK')
        else:
            if linha ==None:
                print('')
                   
'''def conta_pessoas(id1):#conta quantas poessoas tem no leilao
    sel1='SELECT * FROM entrar_leilao WHERE id=(?) '
        print('Pesquisando lance minimo:')
        conta=0
        for row1 in c.execute(sel1,(id1,)):
            print(row1)
            conta=conta+1'''
    
    
def comeca_leilao(tpl,id1,conn1):
    try:
        
        conta_lance=0
        semaphore.acquire() # decrements the counter
        time.sleep(tpl)
        print 'Connected by', addr1
        try:
            conexao = sqlite3.connect('banco2.db')
            c=conexao.cursor()
            sel='SELECT lancemin FROM produtos WHERE id=(?) '
            print('Pesquisando lance minimo:')
            lancemin= c.execute(sel,(id1,))
            for row in c.execute(sel,(id1,)):
                                print(row)           
            lcorrente=int(row[0])

        
        

            while 1:
                
                data1 = conn1.recv(4096) #Recebe o dados enviados
                msg1 = data1.split(',')
                print "Chegou ", data1, "gerei",msg1

                if msg1[0]=="entrar_leilao":
                    h1=str("o lance minimo e %d" %lcorrente)
                    conn1.sendall(h1)
                    
                        
                    
                if msg1[0]=="enviar_lance":
                    
                    try:
                        
                        if (lcorrente>msg1[1]):
                            
                            print('valor inválido!')
                            conn1.send('not_ok')
                        
                        if(lcorrente<msg1[1]): #SERVIDOR, compara o valor
                            sem.acquire()
                            lcorrente=int(msg1[1]) #essa variavel tem que estar protegida usando semaforo
                            conta_lance=conta_lance+1
                            sem.release()
                            print('ok')
                            conta=0
                            sel1='SELECT * FROM entrar_leilao WHERE id=(?) '
                            print('Pesquisando lance minimo:')
                            #conn1.sendall('ok')
                            for row1 in c.execute(sel1,(id1,)):
                                print(row1)
                                conta=conta+1
                            print "o cliente %s , enviou o lance %d" %(msg1[2],lcorrente)
                            
                            msg2= str("(OK) id do  leialo: %d O cliente: %s , enviou o lance: %d, o numero de usuarios no leilao e:%d, o numero de lances dados e %d" %(id1,msg1[2],lcorrente,conta, conta_lance))
                            conn1.sendall(msg2)#SERVIDOR repassa o nome do autor e o valor do lance para todos os participantes MSG LANCE
                            atual = time.time()
                            print "O tempo e %d" %(atual)
                            #print "o tempo e %s , enviou o lance %d" %(msg1[2],lcorrente)
                            print 'ok'
                            while (atual+40>time.time()):
                                print 'contando o tempo'
                                time.sleep(1)
                                print msg2
                            print('o leilao acabou')
                            msg3= str("O LEILAO ACABOU: LEILAO DE ID %d  , VALOR DA VENDA: %d, USUARIO GANHADOR %s" %(id1,lcorrente,msg1[2])) #msg  de fim do leilao
                            conn1.sendall("fim_leilao,"+msg3)
                            '''#TENTATIVA DE ENVIAR OS DADOS DO VENDEDOR PARA O CLIENTE
                                conexao = sqlite3.connect('teste.db')
                                c=conexao.cursor()
                                conexao.commit()
                                conn.sendall('ok')
                                listadeenvio=[]
                                c.execute("SELECT * FROM cadastro, entrar_leilao,logados WHERE cadastro.nome=entrar_leilao.nome") 
                                for row in c.fetchall():
                                    print row[8]
                                    print row[9]
                                    destino= "('"+row[8]+"',"+row[9]+")"
                                    print destino
                                    destino.send('Voce e o ganhador!')
                                selec= "SELECT nome_dono FROM produtos WHERE id=(?)"
                                c.execute(selec,(id1,))
                                for  row in c.fetchall():
                                    selec= "SELECT nome, telefone, endereco FROM cadastro WHERE nome=(?)"
                                    c.execute(selec,(row[0],))
                                    for i in c.fetchall():
                                            listadeenvio.append(row1)
            
                                    envia=str(listadeenvio) 
                                    destino.send(envia)
                                #INICIO DA TENTATIVA DE BUSCAR OS DADOS DO VENDEDOR    
                                seleciona="SELECT nome_dono FROM produtos WHERE id=(?)"
                                c.execute(seleciona,(id1,))
                                for linha in c.fetchall():
                                           c.execute("SELECT * FROM cadastro,logados WHERE cadastro.nome=entrar_leilao.nome")#pesquisaria o ip e a porta e os dados do dono do leilao
                                           
                                        '''
                    except Exception,err:
                        print(err)
                        conn1.send('not_ok')

                if msg1[0] == 'tchau':
                        conn1.sendall ('fim')
                        print('Sem conexao')
                             
                             
                      
                if not data1: break     

            conn1.close() #Fecha conexão
        except Exception,err:
            print (err)
            print('Erro ao lancar')
            conn1.send('not_ok')
            conn1.close() #Fecha conexão
    except Exception,err:
        print err
        semaphore.release() # increments the counter    
def dorme_acorda(nome,lcorrente):
    try:
                   
        while True:
            time.sleep(1)
            h=str("o cliente %s , enviou o lance %d" %(nome,lcorrente))          
            conn1.sendall(h)           
            if msg[0] == 'tchau':
                       conn.sendall ('fim')
                       print('Sem conexao')
                     
                     
              
            if not data: break     

        conn1.close() #Fecha conexão
    except Exception,err:
        print (err)
        print('A conexão falhou')
        conn1.close() #Fecha conexão                     
  
def aceita(conn):
    print 'Connected by', addr
    try:
        
        while 1:
            
            data = conn.recv(4096) #Recebe o dados enviados
            msg = data.split(',')
            print "Chegou ", data, "gerei",msg
            if msg[0]=="adiciona_usuario":
                try:
                    buscar_nome(msg[1])#busca o nome no banco de dados
                    print('Usuário nao encontrado, pode cadastrar')
                    inserir_cliente(msg[1],msg[2],msg[3],msg[4],msg[5])
                    print('Cadastrado com sucesso!')
                    conn.send('ok')
                    #se não encontrar vai para a exceção e faz o cadastro
                        
                except:                 
                     print('Erro ao cadastrar')
                     conn.send('not_ok')
                     '''
                     inserir_cliente(msg[1],msg[2],msg[3],msg[4],msg[5])
                     print('Cadastrado com sucesso!')
                     conn.send("ok")'''
                
            
            if msg[0] == "faz_login":
                try:
                    buscar_cliente(msg[1],msg[2])
                    print('Login efetuado com sucesso')
                    '''ih =str(addr)
                    print (ih)
                    ih2 = ih.split(',')
                    ih2[0],ih2[1]'''
                    ih= str(addr[0])
                    ih2=str(addr[1])
                    print "Chegou ", ih, "gerei",ih2
                    inserir_logado(msg[1],ih,ih2) #insere o nome, ip e porta na tabela logados
                    print('inserido')
                    conn.send ("ok")
                except Exception,err:
                    print err
                    print('Cliente nao encontrado')
                    conn.send("not_ok")
                    
            if msg[0]== "listar_leiloes":
                listar_produtos(conn)

            if msg[0]== "apaga":
                try:
                    excluir_cliente(msg[1],msg[2])#recebe nome e senha
                except:
                    conn.send('not_ok')

            if msg[0]== "lanca":
                try:
                    d= time.strftime('%Y/%m/%d/%H:%M:%S')
                    newdate1 = datetime.strptime(d, "%Y/%m/%d/%H:%M:%S") 
                    newdate2 = datetime.strptime(msg[4], "%Y/%m/%d/%H:%M:%S")
                    if newdate1<newdate2:
                        inserir_produto(msg[1],msg[2],msg[3],msg[4],msg[5]) #insere nome, descrição e lance mínimo,tenho que pedir a data don leilao tb
                        print('ok')
                        diferenca = (newdate2 - newdate1) #calcula o tempo que falta até  o leilão
                        print ('ok')
                        conexao = sqlite3.connect('banco2.db')
                        c=conexao.cursor()
                        sel='SELECT id FROM produtos WHERE descricao=(?) ' 
                        print('Pesquisando id:')
                                                
                        for row in c.execute(sel,(msg[2],)):
                                       print(row)
                                       
                                       
                                       print row[0]
                                       id1=row[0]
                        tpl=timedelta.total_seconds(diferenca)               
                        ti= Thread(target=comeca_leilao,name=(id1,), args=(tpl,id1,conn1))
                        ti.start()
                        print ('ok')

                        
                        
                        
                            
                        '''t2=Thread(target=conta_tempo,args=())
                        t2.start()'''
                        conn.send('ok')
                    else:
                        conn.send('not_ok')
                except Exception,err:
                    print err
                    conn.send('not_ok')
            if msg[0]=="entrar_leilao":
                try:
                    
                    buscar_leilao(msg[1])
                    buscar_hora(msg[1])
                    entrar_leilao(msg[1],msg[2])
                    conn.send('ok')
                
                    '''if msg[1].isAlive():
                        while(1):
                            s1.listen(1) #espera chegar pacotes na porta especificada
                            conn1, addr1 = s1.accept()#Aceita uma conexão
                            print "Aceitou mais uma"
                            conn.send('ok')
                    else:
                        conn.send('not_ok')'''               
                                       
                except Exception, err:
                    print err
                    conn.sendall('not_ok')
            if msg[0]== "sair_leilao":
                try:
                    sair_leilao(msg[1],msg[2])
                except:
                    conn.sendall('not_ok')
            if msg[0] == 'tchau':
                excluir_logados(msg[1])
                conn.sendall ('fim')
                print('Sem conexao')
                 
                 
          
            if not data: break     

        conn.close() #Fecha conexão
    except Exception,err:
        print (err)
        print('A conexão falhou')
        #ip_falha=(str(addr[0]))
        porta_falha=str(addr[1])
        print(porta_falha)
        excluir_logados_falha(porta_falha)
        conn.close() #Fecha conexão
                    
   


HOST = ''                 
PORT = 50136            
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #IPv4,tipo de socket
s.bind((HOST, PORT)) #liga o socket com IP e porta

HOST1 = ''                 
PORT1 = 50137            
s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #IPv4,tipo de socket
s1.bind((HOST1, PORT1)) #liga o socket com IP e porta



while(1):
    s.listen(1) #espera chegar pacotes na porta especificada
    conn, addr = s.accept()#Aceita uma conexão
    print "Aceitou mais uma"
    s1.listen(1) #espera chegar pacotes na porta especificada
    conn1, addr1 = s1.accept()#Aceita uma conexão
    print "Aceitou mais uma"
    sem= BoundedSemaphore()
    t = Thread(target=aceita, args=(conn,))
    t.start()
    t1 = Thread(args=(conn1,))
    t1.start()
    conexao = sqlite3.connect('banco2.db')
    c=conexao.cursor()
    d= time.strftime('%Y/%m/%d/%H:%M:%S')
    newdate1 = datetime.strptime(d, "%Y/%m/%d/%H:%M:%S")
    sel1='SELECT id,data_hora FROM produtos'
    for row1 in c.execute(sel1):
        newdate2 = datetime.strptime(row1[1], "%Y/%m/%d/%H:%M:%S")
        if newdate1<newdate2:
            diferenca = (newdate2 - newdate1) #calcula o tempo que falta até  o leilão
            print ('ok')
            semaphore = BoundedSemaphore(200)
            print "Permito até 200 leilões em paralelo"
            tpl=timedelta.total_seconds(diferenca)               
            ti= Thread(target=comeca_leilao,name=(row1[0],), args=(tpl,row1[0],conn1))
            ti.start()
    ti.join()
    print "Acabou o leilao"
    
        







	
        
	
	



    
