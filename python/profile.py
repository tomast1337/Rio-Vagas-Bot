import os
import shutil
import json
name = "profile.py"
osPath = os.path.realpath(__file__)
relativePath = "\python\profile.py" 
def criarPerfil(Perfil,nome,email,celular,telefone,pretencao,Curriculo,CurriculoTexto,Carta): #Implementado cria uma nova pasta com o nome do perfil
    if not( type(Perfil) is str and
            type(nome) is str and
            type(email) is str and
            type(celular) is str and
            type(telefone) is str and
            type(pretencao) is int and
            type(Curriculo) is str and
            type(CurriculoTexto) is str and
            type(Carta) is str
          ):
        return False
    else:
        p = ((osPath.replace("\\","/").replace(name,"").replace("python/","")) + "profiles/default")
        d = ((osPath.replace("\\","/").replace(name,"").replace("python/","")) + "profiles/" + Perfil)
        try:
            shutil.copytree(p,d)
        except Exception as e:
            print(e)
            return False
        else:
            #print("Criado pasta do perfil",Perfil)
            CriarJson(Perfil,nome,email,celular,telefone,pretencao)
            #Curriculo a fazer
            p = ((osPath.replace("\\","/").replace(name,"").replace("python/","")) + "profiles/" + Perfil)
            writeFile(p+"/Carta.txt",Carta)
            writeFile(p+"/Curiculo.txt",CurriculoTexto)
            return True      
def writeFile(path,texto):
    f = open(path,"w")
    f.write(texto)
    f.close()
def apagarPerfil(Perfil):
    p = ((osPath.replace("\\","/").replace(name,"").replace("python/","")) + "profiles/" + Perfil)
    try:
        shutil.rmtree(p)
    except Exception as e:
        print(e)
        return False
    else:
        return True
def CriarJson(Perfil,nome,email,celular,telefone,pretencao):
    p = ((osPath.replace("\\","/").replace(name,"").replace("python/","")) + "profiles/" + Perfil)
    data = {"Nome": nome,
            "Email": email,
            "Celular": celular,
            "Telefone": telefone,
            "Pretensao": int(pretencao)
           }
    f = open(p+"/config.json","w")
    f.write(json.dumps(data, indent=4))
    f.close()
    pass
if __name__ == "__main__":
    print(criarPerfil("Perfil de Teste",
                    "Nome da Silva",
                    "email@email.com",
                    "(11)911111111",
                    "(11)11111111",
                    99800,
                    "Path",
                    "Bla bla",
                    "Carta bla bla"
                    ))
    input("Entre para apagar")
    apagarPerfil("Perfil de Teste")