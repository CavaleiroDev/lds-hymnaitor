# https://github.com/CavaleiroDev/lds-hymnaitor
# this code is NOT optimized. It was made to extract data in Portuguese and, for now, might not work properly with English

import json
import requests
from pathlib import Path
from bs4 import BeautifulSoup

URL = "https://www.churchofjesuschrist.org/study/music/hymns-for-home-and-church?lang=por"

DIR = Path("dados/hinos")
typstReaderDIR = Path("../dados/hinos")
indexPath = Path("dados/hinos.json")
columnsPath = Path("dados/columns.json")

page = requests.get(URL)
hymnlist = BeautifulSoup(page.text, "html.parser")
hinos = hymnlist.find_all("li", attrs={"data-content-type":"music"})

citation_blacklist = [
    "para voz e violão"
]

def GetHymn(URL):
    hino = requests.get(URL)
    soup = BeautifulSoup(hino.text, "html.parser")
    
    hino_data = {}

    nome = soup.find("h1", attrs={"id":"title1"}).text.encode("latin1").decode("utf-8")
    numero_obj = soup.find("p", attrs={"class":"song-number"})
    if numero_obj:
        numero = numero_obj.text
    else:
        numero = nome
    

    hino_data["id"] = numero
    hino_data["name"] = nome

    poetry = soup.find("div", attrs={"class":"poetry"})
    estrofes_raw = poetry.find_all("div") # estrofes_raw = soup.find("div", attrs={"class":"poetry"})
    estrofes = []
    for e in estrofes_raw:
        novaestrofe = {}

        tipo = e["class"][0] # type
        number_obj = e.find("span", attrs={"class":"verse-number"})
        if number_obj:
            number = number_obj.text
            number = number.strip()
            number = number[:-1]
            try:
                number = int(number)
            except ValueError:
                print(hino_data["id"])
                print(number)
                number = 0
                pass  # it was a string, not an int
            # number = int(number)   # é boa prática ter mas n quero consertar para conseguir rodar o hino 1041!   ISSO TEM QUE CONSERTAR PARA A FORMATAÇÃO FUNCIONAR!!!!
            number_obj.decompose()
        else:
            number = 0
        
        chorus_tag_obj = e.find("p", attrs={"class":"label"})
        if chorus_tag_obj: # removes undesirable "[chorus]" text
            chorus_tag_obj.decompose()
        
        text = e.text.encode("latin1").decode("utf-8") ###################### PRECISO QUE O "\n" NO INICIO DE CADA ESTROFE SEJA REMOVIDO

        novaestrofe["tipo"] = tipo
        novaestrofe["number"] = number
        novaestrofe["text"] = text

        estrofes.append(novaestrofe)

    citation_info = soup.find("div", attrs={"class":"citation-info"})
    citation_raw = citation_info.find_all("p")
    citation = []
    for c in citation_raw:
        append = True
        links = c.find_all("a")
        for l in links:
            for b in citation_blacklist:
                if l.text.encode("latin1").decode("utf-8") == b: # checa se um dos links na citação está na black list e se for verdadeiro: não o salva
                    #print("elemento proibido encontrado! ignorando")
                    append = False
        if(append):
            citation.append(c.text.encode("latin1").decode("utf-8"))

    print(citation)
    
    body_block = soup.find("div", attrs={"class":"body-block"})
    scriptures_raw = body_block.find_all("a", attrs={"class":"scripture-ref"})
    scriptures = []
    for s in scriptures_raw:
        scriptures.append(s.text.encode("latin1").decode("utf-8")) ######################################### COLOCAR UM FILTRO PARA NÃO VIR "para voz e violão"

    hino_data["content"] = estrofes
    hino_data["citation"] = citation
    hino_data["scriptures"] = scriptures

    CleanseHymnText(hino_data)

    return json.dumps(hino_data, indent=4)

def SaveHymnAsJson(URL):
    dados = GetHymn(URL)
    dados = json.loads(dados)
    RegisterEntry(dados)

    with open(str(DIR)+"/"+dados['id']+".json", "w") as f:
        json.dump(dados, f, indent=4)

def CleanseHymnText(hino_data):
    # remove ' ' no começo do nome dos hinos
    hino_data["name"] = hino_data["name"].strip()
    # remove \n no começo das estrofes
    for e in hino_data["content"]:
        e["text"] = e["text"].strip('\n') # remove quebras de linha no inicio e final da string. Mantém espaços caso existam no começo da string

def RegisterEntry(hino_data):
    ### registra em 'hinos.json' o caminho do arquivo do hino gerado
    indexFileData = {}
    with open(indexPath, "r") as f:
        indexFileData = json.load(f)
    
    indexFileData[hino_data["id"]]= str(typstReaderDIR)+"/"+hino_data['id']+".json"
    
    with open(indexPath, "w") as f:
        json.dump(indexFileData, f, indent=4)
    
    
    ### registra em 'columns.json' uma nova entrada para este hino caso não exista
    columnsFileData = {}
    with open(columnsPath, "r") as f:
        columnsFileData = json.load(f)

    if not columnsFileData.get(hino_data["id"]): # se não existir: cria
        #print("registrando para "+hino_data["id"])
        columnsFileData[hino_data["id"]] = 2 # 2 é o valor padrão para os hinos. em certos casos manualmente será definido para 1 dentro do json
    #else: # se existir
        #print("já existe registrado a coluna para "+hino_data["id"])
        
        
    with open(columnsPath, "w") as f:
        json.dump(columnsFileData, f, indent=4)


#SaveHymnAsJson("https://www.churchofjesuschrist.org/study/music/hymns-for-home-and-church/come-thou-fount-of-every-blessing?lang=por")
#SaveHymnAsJson("https://www.churchofjesuschrist.org/study/music/hymns-for-home-and-church/think-a-sacred-song?lang=por")
#SaveHymnAsJson("https://www.churchofjesuschrist.org/study/music/hymns-for-home-and-church/when-the-savior-comes-again?lang=por")


for h in hinos:
    link = "https://www.churchofjesuschrist.org/"+h.find("a")["href"]
    print(link)
    SaveHymnAsJson(link)

#SaveHymnAsJson("https://www.churchofjesuschrist.org/study/music/hymns-for-home-and-church/peace-peace-be-still?lang=por")
