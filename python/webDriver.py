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
    driverLocation = path+"chromedriver"
    os.environ["webdriver.chrome.driver"] = driverLocation
    chrome_options = Options()
    chrome_options.add_argument("--disable-popup-blocking")
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--ignore-ssl-errors')
    driver = webdriver.Chrome(driverLocation)
    driver.create_options()
    return driver

def Pesquisar(vaga):
    driver = criarDriver()
    url = "https://riovagas.com.br/page/"+str(1)+"/?s="+pesquisa
    driver.get(url)
    tag = False
    if driver.current_url.find("/tag/") != -1:
        #print("Modo /tag/")
        tag = True
    driver.implicitly_wait(0.1)
    size = driver.find_elements_by_css_selector("#vce-pagination .page-numbers:nth-last-child(n)")
    #print("Numero de paginas",len(size))
    n = size[len(size)-2].text
    try:
        f = open((osPath.replace("\\","/").replace(name,"").replace("python/","")) + "vagas/" + vaga+".db", "x")
    except FileExistsError:
        print(vaga+".db ja criado !")
    comecoT = time.time() # Tempo do começo da busca
    for x in range(1,int(n)+1):
        total = 0
        if tag == True:
            url = "https://riovagas.com.br/tag/"+vaga.replace(" ","-")+"/page/"+str(x)+"/"
        else:
            url = "https://riovagas.com.br/page/"+str(x)+"/?s="+vaga
        driver.get(url)
        driver.implicitly_wait(10)
        print("Entrando na pagina: ", x ," de ",n," pagina(s)")
        elems = driver.find_elements_by_xpath("//a[@href]")
        print(len(elems),"elementos encontrados")
        print("Abrindo "+vaga+".db")
        conn = sqlite3.connect((osPath.replace("\\","/").replace(name,"").replace("python/","")) + "vagas/" + vaga+".db")
        c = conn.cursor()
        tabela = "CREATE TABLE "+vaga+"(Link text) PRIMARY KEY Link"
        c.execute(tabela)
        for elem in elems:
            links = []
            link = str(elem.get_attribute("href"))
            if link.find("/riovagas/") != -1 and link.find("riovagas-vagas-mais-acessadas") ==-1 and link.find("/category/") == -1 and link != "https://riovagas.com.br/riovagas/":
                total = total + 1
                links.append(elem.get_attribute("href"))
            for url in links:
                sql = "INSERT OR REPLACE INTO table"+vaga+" (Link) VALUES ("+url+")"
                c.execute(sql)
                conn.commit()
                print("Vaga "+link+" adicionada ao Banco de dados")
        conn.close()
    fimT = time.time() #Tempo Final
    print("Total tempo "+str(fimT-comecoT)+" segundos")
    driver.quit()

def eviar(vaga,perfil):
    pass