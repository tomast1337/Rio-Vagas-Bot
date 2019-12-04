from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from random import *
import os
import time
import simplejson as json

path = os.path.realpath(__file__).replace("WebDriver.py","")
slash = r'\\'
def typein(text,elem,speed):
    for character in text:
            elem.send_keys(character)
            time.sleep(speed)
def typeinran(text,elem,speedMin,speedMax):
    for character in text:
            speed = float(uniform(speedMin,speedMax))/100
            elem.send_keys(character)
            time.sleep(speed)
def RPopupClose(button):
    try:
        button.click()
        print("Popup fechado\n")
    except ValueError:
        print("Não tem botão de popup\n")
    except Exception:
        print("Não tem botão de popup")
def criardiver():
    driverLocation = path+"chromedriver"
    os.environ["webdriver.chrome.driver"] = driverLocation
    chrome_options = Options()
    chrome_options.add_argument("--disable-popup-blocking")
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--ignore-ssl-errors')
    driver = webdriver.Chrome(driverLocation)
    driver.create_options()
    return driver
def RioVagas(pesquisa):
    driver = criardiver()
    url = "https://riovagas.com.br/page/"+str(1)+"/?s="+pesquisa
    driver.get(url)
    tag = False
    if driver.current_url.find("/tag/") != -1:
        print("Modo /tag/")
        tag = True
    driver.implicitly_wait(0.1)
    
    size = driver.find_elements_by_css_selector("#vce-pagination .page-numbers:nth-last-child(n)")
    print(len(size))
    n = size[len(size)-2].text

    print(n," Paginas encontradas!")
    try:
        f = open(path+"resources/Vagas/"+pesquisa+".txt", "x")
    except FileExistsError:
        print(pesquisa+".txt ja criado !")
    comecoT = time.time()
    TodasVagas = 0
    for x in range(1,int(n)+1):
        total = 0
        if tag == True:
            url = "https://riovagas.com.br/tag/"+pesquisa.replace(" ","-")+"/page/"+str(x)+"/"
        else:
            url = "https://riovagas.com.br/page/"+str(x)+"/?s="+pesquisa
        driver.get(url)
        driver.implicitly_wait(10)
        print("Entrando na pagina: ", x ," de ",n," pagina(s)")
        elems = driver.find_elements_by_xpath("//a[@href]")
        print(len(elems),"elementos encontrados")
        print("Abrindo "+pesquisa+".txt")
        for elem in elems:
            links = []
            comeco = time.time()
            link = str(elem.get_attribute("href"))
            repetido = False
            for i in range(len(links)):#Checa se o link ja esta na lista
                if links[i] == link:
                    repetido = True
                    print("Link repetido")
                    break
            if link.find("/riovagas/") != -1 and link.find("riovagas-vagas-mais-acessadas") ==-1 and link.find("/category/") == -1 and link != "https://riovagas.com.br/riovagas/" and repetido == False:
                total = total + 1
                links.append(elem.get_attribute("href"))
                print("Vaga "+link+" adicionada a "+pesquisa+".txt")
            for url in links:
                f = open(path+"resources/Vagas/"+pesquisa+".txt", "a")
                f.write(url+"\n")
                f.close()
            fim = time.time()
        print(total," vagas encontradas "+str(fim - comeco)+" segundos")
        TodasVagas = TodasVagas + total
    fimT = time.time()
    print("No total foram ",TodasVagas," encontradas no tempo de "+str(fimT-comecoT)+" segundos")
    driver.quit()
def Enviar(pesquisa,config):
    driver = criardiver()
    path.replace("c:/","")
    listaVagas = []
    f = open(path+"resources/Vagas/"+pesquisa+".txt","r")
    listaVagas = f.read().split('\n')
    comecoT = time.time()
    for i in range(len(listaVagas)):
        comeco = time.time()
        url = listaVagas[i]
        if url == "":
            break
        print("Indo para:",url)
        driver.get(url)
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
                Cartatexto = open(path+"resources/Carta.txt","r",encoding="utf-8")
                print("Digitando nome",end=" ... ")
                typein(config['Nome']    ,driver.find_element_by_xpath("//input[@id='nome_candidato']")     ,0.01)#Nome
                print("Digitando email",end=" ... ")
                typein(str(config['Email'])   ,driver.find_element_by_xpath("//input[@id='email_candidato']")    ,0.01)#Email
                print("Digitando Celular",end=" ... ")
                typein(str(config['Celular']) ,driver.find_element_by_xpath("//input[@id='celular_candidato']")  ,0.3 )#celular
                print("Digitando telefone",end=" ... ")
                typein(str(config['Telefone']),driver.find_element_by_xpath("//input[@id='telefone_candidato']") ,0.3 )#Telefone
                print("Digitando carta",end=" ... ")
                typein(Cartatexto.read(),driver.find_element_by_xpath("//textarea[@id='apresentacao_candidato']"),0.01)#Carta apresentação
                #Pretensao
                try:
                    Texto = driver.find_element_by_xpath("//input[@id='pretensao_salarial']")
                    print("Digitando Pretensao")
                    Texto.send_keys(str(config['Pretensao']))    
                except:
                    print("Essa vaga não possu pretenção salarial")
                #Eviar curriculo PDF ou TEXTO NO EMAIL
                forma_envio = driver.find_elements_by_xpath("//input[@id='forma_envio']")
                print(str(len(forma_envio)))
                if len(forma_envio) == 2:#PDF
                    driver.implicitly_wait(1)
                    forma_envio[0].click()
                    forma_envio = driver.find_element_by_xpath("/html//input[@id='anexo']")
                    print(""+path.replace("/",slash)+r"resources\Curiculo.pdf")
                    print("Digitando caminho do Pdf")
                    forma_envio.send_keys(""+path.replace("/",slash)+r"resources\Curiculo.pdf")
                    print("O curriculo foi enviado como pdf")
                else:#Texto
                    driver.implicitly_wait(2)
                    try:
                        driver.find_element_by_xpath("//textarea[@id='curriculo_candidato']")
                        curriculo = open(path+"resources/Curiculo.txt",encoding="utf-8")
                        print("Digitando curriculo como email")
                        driver.implicitly_wait(2)
                        typeinran(curriculo,driver.find_element_by_xpath("//textarea[@id='curriculo_candidato']"),30,50)
                        print("O curriculo foi enviado como texto no email")
                    except:
                        driver.implicitly_wait(2)
                        driver.find_element_by_css_selector("[value='anexo']").click()
                        forma_envio = driver.find_element_by_xpath("/html//input[@id='anexo']")
                        print(""+path.replace("/",slash)+r"resources\Curiculo.pdf")
                        print("Digitando caminho do PDF")
                        forma_envio.send_keys(""+path.replace("/",slash)+r"resources\Curiculo.pdf")
                        print("O curriculo foi enviado como pdf")
                fim = time.time()
                print("Curriculo enviado em Tempo = "+str(format(fim-comeco, '.2f'))+" Segundos")
                driver.implicitly_wait(4)
                button = driver.find_element_by_xpath("//main[@id='main']/article//form[@method='POST']/button[@type='submit']")
                button.click()
        except:
            print("Vaga invalida")
    fimT = time.time()
    print("Todos os curriculos para "+pesquisa+" enviados em Tempo = "+str(format((fimT-comecoT)/60, '.2f')) +" Minutos")
    driver.quit()