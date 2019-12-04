from profileManager import *
from webDriver import *
import eel
from tkinter import filedialog
from tkinter import *
eel.init('web')

@eel.expose
def SelecionarCurriculo():
	root = Tk()
	root.withdraw()
	root.wm_attributes('-topmost', 1)
	folder = filedialog.askopenfilename(title = "Selecione o curriculo",filetypes = (("Arquivo PDF","*.pdf"),("Todos os tipo","*.*")))
	return folder

@eel.expose
def criarp(NomeP,Nome,Email,celular,telefone,pretensao,pesquisa,carta,curriculo,curriculoT):
    return criarPerfil(NomeP,Nome,Email,celular,telefone,pretensao,pesquisa,curriculo,curriculoT,carta)

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
eel.start('index.html',size = (800,800),)
