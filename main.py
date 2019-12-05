from profileManager import *
from webDriver import *
import eel
import os
from tkinter import filedialog
from tkinter import *

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

@eel.expose
def criarP(NomeP,Nome,Email,celular,telefone,pretensao,pesquisa,carta,curriculo,curriculoT):
    return criarPerfil(NomeP,Nome,Email,celular,telefone,pretensao,pesquisa,curriculo,curriculoT,carta)

@eel.expose
def listarP():
    perfis = os.listdir(((osPath.replace(name,"")) + "profiles"))
    perfis.remove("default")
    if not perfis:
        print("Nem um perfil existente")
    else: 
        print(perfis)
    return perfis;
        

@eel.expose
def apagarP(NomeP):
    pass

@eel.expose
def alterarP(NomeP):
    pass

@eel.expose
def realizarB(NomeP):
    pass

@eel.expose
def realizarE(NomeP):
    pass
eel.start('index.html',size = (900,900),)
