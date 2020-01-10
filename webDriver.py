from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from random import *
import sqlite3
import os
import time
import json
slash = r'\\'
name = "webDriver.py"
osPath = os.path.realpath(__file__)
relativePath = "\python\profile.py" 

def typein(text,elem,speedMin = 2,speedMax = 5):
    for character in text:
            speed = float(uniform(speedMin,speedMax))/100
            elem.send_keys(character)
            time.sleep(speed)

def criarDriver():
    driverLocation = (osPath.replace(name,"")+"chromedriver")
    os.environ["webdriver.chrome.driver"] = driverLocation
    chrome_options = Options()
    chrome_options.add_argument("--disable-popup-blocking")
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--ignore-ssl-errors')
    driver = webdriver.Chrome(driverLocation)
    driver.create_options()
    return driver

def Pesquisar(vaga):
    comecoT = time.time() # Tempo do começo da busca
    driver = criarDriver()
    url = "https://riovagas.com.br/page/"+str(1)+"/?s="+vaga
    driver.get(url)
    tag = False
    if driver.current_url.find("/tag/") != -1:
        tag = True
    driver.implicitly_wait(0.1)
    size = driver.find_elements_by_css_selector("#vce-pagination .page-numbers:nth-last-child(n)")
    n = size[len(size)-2].text
    try:
        f = open((osPath.replace("\\","/").replace(name,"")) + "vagas/" + vaga+".db", "x")
    except FileExistsError:
        print(vaga+".db ja criado !")
    for x in range(1,int(n)+1):
        total = 0
        if tag == True:
            url = "https://riovagas.com.br/tag/"+vaga.replace(" ","-")+"/page/"+str(x)+"/"
        else:
            url = "https://riovagas.com.br/page/"+str(x)+"/?s="+vaga
        driver.get(url)
        driver.implicitly_wait(3)
        print("Entrando na pagina: ", x ," de ",n," pagina(s)")
        elems = driver.find_elements_by_xpath("//a[@href]")
        print(len(elems),"elementos encontrados")
        print("Abrindo "+vaga+".db")
        conn = sqlite3.connect((osPath.replace("\\","/").replace(name,"").replace("python/","")) + "vagas/" + vaga+".db")
        c = conn.cursor()
        conn.execute('CREATE TABLE IF NOT EXISTS '+"'"+vaga+"'"+' (Link text PRIMARY KEY)')
        for elem in elems:
            links = []
            link = str(elem.get_attribute("href"))
            if link.find("/riovagas/") != -1 and link.find("riovagas-vagas-mais-acessadas") ==-1 and link.find("/category/") == -1 and link != "https://riovagas.com.br/riovagas/":
                total = total + 1
                links.append(elem.get_attribute("href"))
            for url in links:
                c.execute('INSERT OR REPLACE INTO '+"'"+vaga+"'"+'(Link) VALUES ("'+url+'")')
                conn.commit()
                print("Vaga "+link+" adicionada ao Banco de dados")
        conn.close()
    fimT = time.time() #Tempo Final
    print("Total tempo "+str(fimT-comecoT)+" segundos")
    driver.quit()

def eviar(vaga,perfil):
    path = (osPath.replace("\\","/").replace(name,""))
    comecoT = time.time()  # Tempo do começo dos envios
    print("Abrindo "+vaga+".db")
    conn = sqlite3.connect((osPath.replace("\\","/").replace(name,"")) + "vagas/" + vaga+".db")
    c = conn.cursor()
    vagas = c.execute("SELECT Link FROM "+"'"+vaga+"'").fetchall()
    driver = criarDriver()
    url = "https://riovagas.com.br/page/"+str(1)+"/?s="+vaga
    driver.get(url)
    for url in vagas:
        vag = url[0]
        if vag == "":
            break
        print("Indo para:",vag)
        driver.get(vag)
        try:
            elem = driver.find_element_by_css_selector(".btn-candidatar [target]")
            url = str(elem.get_attribute("href"))
            driver.get(url)
            driver.implicitly_wait(2)
            try:
                print("Desativando news Letter")
                driver.find_element_by_xpath("//input[@id='newsletter_rv']").click()
                valido = True
            except:
                valido = False
                print("Link Invalido")
            if valido == True:
                Cartatexto = open(path+"profiles/"+perfil["PNome"]+"/Carta.txt","r",encoding="utf-8")
                print("Digitando nome",end=" ... ")
                typein(perfil['Nome']    ,driver.find_element_by_xpath("//input[@id='nome_candidato']")     ,0.01)#Nome
                print("Digitando email",end=" ... ")
                typein(str(perfil['Email'])   ,driver.find_element_by_xpath("//input[@id='email_candidato']")    ,0.01)#Email
                print("Digitando Celular",end=" ... ")
                typein(str(perfil['Celular']) ,driver.find_element_by_xpath("//input[@id='celular_candidato']")  ,0.3 )#celular
                print("Digitando telefone",end=" ... ")
                typein(str(perfil['Telefone']),driver.find_element_by_xpath("//input[@id='telefone_candidato']") ,0.3 )#Telefone
                print("Digitando carta",end=" ... ")
                typein(Cartatexto.read(),driver.find_element_by_xpath("//textarea[@id='apresentacao_candidato']"),0.01)#Carta apresentação
                #Pretensao
                try:
                    Texto = driver.find_element_by_xpath("//input[@id='pretensao_salarial']")
                    print("Digitando Pretensao")
                    typein(str(perfil['Pretensao']),Texto,20,30)
                except:
                    print("Essa vaga não possu pretenção salarial")
                #Eviar curriculo PDF ou TEXTO NO EMAIL
                forma_envio = driver.find_elements_by_xpath("//input[@id='forma_envio']")
                print(str(len(forma_envio)))
                if len(forma_envio) == 2:#PDF
                    driver.implicitly_wait(1)
                    forma_envio[0].click()
                    forma_envio = driver.find_element_by_xpath("/html//input[@id='anexo']")
                    print(""+path+"profiles/"+perfil["PNome"]+r"resources\Curiculo.pdf")
                    print("Digitando caminho do Pdf")
                    forma_envio.send_keys(""+path+"profiles/"+perfil["PNome"]+r"\Curiculo.pdf")
                    print("O curriculo foi enviado como pdf")
                else:#Texto
                    driver.implicitly_wait(2)
                    try:
                        driver.find_element_by_xpath("//textarea[@id='curriculo_candidato']")
                        curriculo = open(path+"profiles/"+perfil["PNome"]+"/Curiculo.txt",encoding="utf-8")
                        print("Digitando curriculo como email")
                        driver.implicitly_wait(2)
                        typein(curriculo,driver.find_element_by_xpath("//textarea[@id='curriculo_candidato']"),30,50)
                        print("O curriculo foi enviado como texto no email")
                    except:
                        driver.implicitly_wait(2)
                        driver.find_element_by_css_selector("[value='anexo']").click()
                        forma_envio = driver.find_element_by_xpath("/html//input[@id='anexo']")
                        print("Digitando caminho do PDF")
                        forma_envio.send_keys(""+path+"profiles/"+perfil["PNome"]+r"resources\Curiculo.pdf")
                        print("O curriculo foi enviado como pdf")
                driver.implicitly_wait(4)
                button = driver.find_element_by_xpath("//main[@id='main']/article//form[@method='POST']/button[@type='submit']")
                button.click()
        except:
            print("Vaga invalida")
    fimT = time.time()  # Tempo do fim dos envios
    print("Todos os curriculos para "+vaga+" enviados em Tempo = "+str(format((fimT-comecoT)/60, '.2f')) +" Minutos")
    driver.quit()