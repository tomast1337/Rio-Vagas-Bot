from WebDriver import *
import os
import json

path = os.path.realpath(__file__).replace("__init__.py","").replace("c:","").replace("\\","/")

#try:
#    config = {'Nome': 'Seu nome completo vai aqui', 'Email': 'Seu email','Celular' :'(99)999999999','Telefone' :'(22)22222222', 'Pretensao': 99800 }
#    with open(path+'resources/config.json', 'w') as f:
#        json.dump(config, f)
#except:
#    open(path+'resources/config.json', 'x')

with open(path+'resources/config.json', 'r') as f:
    config = json.load(f)

op = ''
Sair = True

def Buscar():
    RioVagas(pesquisa)
    input("Clique qualquer tecla para continuar ...")

def EnviarC():
    Enviar(pesquisa,config)
    input("Clique qualquer tecla para continuar ...")
def Verinfo():
    
    print("--------------------------------------------")
    print("|\tNome:\t\t"   +str(config['Nome']))#Nome
    print("|\tEmail:\t\t"  +str(config['Email']))#Email
    print("|\tCelular:\t"  +str(config['Celular']))#Celular
    print("|\tTelefone:\t" +str(config['Telefone']))#Telefone
    print("|\tPretenção:\t"+str(config['Pretensao']))#Pretensão
    print("--------------------------------------------")

pesquisa = input('Digite a pesquisa Ex:\"Operador de caixa\" ou \"Estagio\" ').lower()
print(pesquisa,"Selecionado")
while(Sair == True):
    print("S-sair ")
    print("B-Buscar ")
    print("E-Enviar ")
    print("P-Mudar pesquisa ")
    print("V-Ver pesquisas feitas pesquisa ")
    print("ES-Enviar varias vezes ")
    print("C-Ver config.json")
    
    op = input("Digite a opção:").upper()
    if op == 's' or op == 'S':
        input("Saindo ...")
        Sair = False
    elif op == 'B' or op == 'b':
        Buscar()
    elif op == 'E' or op == 'e':
        Verinfo()
        EnviarC()
    elif op == 'C' or op == 'c':
        Verinfo()
    elif op == 'P' or op == 'p':
        pesquisa = input('Digite a pesquisa Ex:\"Operador de caixa\" ou \"Estagio\" ').lower()
        print(pesquisa,"Selecionado") 
    elif op == 'ES' or op == 'es':
        Verinfo()
        n = int(input("Digite o numero de vezes"))
        for x in range(n):
            Enviar(pesquisa,config)
            print("Curriculo enviado ",n,"veze(s)")
    else:
        input("Opção invalida\n\nClique qualquer tecla para continuar ...")