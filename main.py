from profileManager import *
from webDriver import *
import eel
import os
from tkinter import filedialog
from tkinter import *
import json

name = "main.py"
osPath = os.path.realpath(__file__)

eel.init('web')

@eel.expose
def SelecionarCurriculo():
	root = Tk()
	root.withdraw()
	root.wm_attributes('-topmost', 1)
	folder = filedialog.askopenfilename(title = "Selecione o curriculo",filetypes = (("Arquivo PDF","*.pdf"),("Todos os tipo","*.*")))
	return folder
def dadosPerfil(NomeP):
    perfil = ((osPath.replace(name,"").replace("\\","/"))+ "profiles/"+(NomeP))
    return json.loads(open(perfil+"\\config.json","r").read())
@eel.expose
def listarP():
    perfis = os.listdir(((osPath.replace(name,"")) + "profiles"))
    perfis.remove("default")
    if not perfis:
        print("Nem um perfil existente")
    else: 
        print(perfis)
    return perfis;
#Manipulação de perfis
@eel.expose
def criarP(NomeP,Nome,Email,celular,telefone,pretensao,pesquisa,carta,curriculo,curriculoT):
    return criarPerfil(NomeP,Nome,Email,celular,telefone,pretensao,pesquisa,curriculo,curriculoT,carta)
@eel.expose
def apagarP(NomeP):
    return apagarPerfil(NomeP)

#Manipulação de pesquisas e envios
@eel.expose
def realizarB(NomeP):
    Dados = dadosPerfil(NomeP)
    Pesquisar(Dados['Pesquisa'])

@eel.expose
def realizarE(NomeP):
    Dados = dadosPerfil(NomeP)
    eviar(Dados['Pesquisa'],Dados)
realizarE("Nicolas dev")

@eel.expose
def realizarEB(NomeP):
    realizarB(NomeP)
    realizarE(NomeP)
    
realizarE("Nicolas dev")

eel.start('index.html',size = (900,900),)
