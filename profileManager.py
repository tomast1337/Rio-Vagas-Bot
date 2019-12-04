import os
import shutil
import json
name = "profileManager.py"
osPath = os.path.realpath(__file__)
relativePath = "\python\profileManager.py" 
def criarPerfil(Perfil,nome,email,celular,telefone,pretencao,Pesquisa,Curriculo,CurriculoTexto,Carta): #Implementado cria uma nova pasta com o nome do perfil
    if not( type(Perfil) is str and type(nome) is str and type(email) is str and type(celular) is str and type(telefone) is str and type(pretencao) is int and type(Pesquisa) is str and type(Curriculo) is str and type(CurriculoTexto) is str and type(Carta) is str):
        return False
    else:
        print(Perfil,nome,email,celular,telefone,pretencao,Pesquisa,Curriculo,CurriculoTexto,Carta)
        Curriculo = Curriculo.replace('\\','/')
        p = ((osPath.replace("\\","/").replace(name,"").replace("python/","")) + "profiles/default")
        dst_dir = ((osPath.replace("\\","/").replace(name,"").replace("python/","")) + "profiles/" + Perfil)
        print(dst_dir)
        try:
            shutil.copytree(p,dst_dir)
        except IOError as e:
            print(e)
            return False
        try:
            shutil.copy2(Curriculo, dst_dir+"/Curiculo.pdf")
        except IOError as e:
            print(e)
            return False
        else:
            #print("Criado pasta do perfil",Perfil)
            CriarJson(Perfil,nome,email,celular,telefone,pretencao,Pesquisa)
            #Curriculo a fazer
            p = ((osPath.replace("\\","/").replace(name,"") + "profiles/" + Perfil))
            writeFile(p+"/Carta.txt",Carta)
            writeFile(p+"/Curiculo.txt",CurriculoTexto)
            print("Perfil Criado")
            return True      
def writeFile(path,texto):
    f = open(path,"w")
    f.write(texto)
    f.close()
def apagarPerfil(Perfil):
    p = ((osPath.replace("\\","/").replace(name,"") + "profiles/" + Perfil))
    try:
        shutil.rmtree(p)
        
    except Exception as e:
        print(e)
        return False
    else:
        return True
def CriarJson(Perfil,nome,email,celular,telefone,pretencao,Pesquisa):
    p = ((osPath.replace("\\","/").replace(name,"") + "profiles/" + Perfil))
    data = {"Nome": nome,
            "Email": email,
            "Celular": celular,
            "Telefone": telefone,
            "Pretensao": int(pretencao),
            "Pesquisa":Pesquisa
           }
    f = open(p+"/config.json","w")
    f.write(json.dumps(data, indent=4))
    f.close()
    pass
if __name__ == "__main__":
    print(criarPerfil("Perfil","nome","email","celular","telefone",99800,"Pesquisa","T:\Rio-Vagas-Bot\Curriculo Leticia - Documentos Google.pdf","CurriculoTexto","Carta"))
    input("Entre para apagar perfil de teste")
    apagarPerfil("Perfil")