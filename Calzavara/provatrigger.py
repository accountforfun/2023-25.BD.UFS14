import azure.functions as func
import datetime
import json
import logging

app = func.FunctionApp()

@app.route(route="MyHttpTrigger", auth_level=func.AuthLevel.ANONYMOUS)
def MyHttpTrigger(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    logging.info('informazioni utili????')

    name = req.params.get('name')
    tante = []
    
    while(True):
        parole_da_trovare = req.params.get()
        if parole_da_trovare:
            tante.append(parole_da_trovare)
        else:
            break
    
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')
    if not name:
        return func.HttpResponse(f"Inserire il nome del farmaco che si vuole cercare")
    if len(tante) == 0:
        return func.HttpResponse(f"Inserire delle parole che si vogliono cercare")
    if name:
        farmaci(name,tante)
        return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully.")
    else:
        return func.HttpResponse(
             "ciaoThis HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )


import requests
from bs4 import BeautifulSoup

def PDF(url,tante):
    print("arrivato")
    print (url)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    pdf = soup.find_all('a')
    pdf.pop()
    pdf.pop(0)
    pdf.pop(0)
    print(pdf)
    siti_pdf=[]
    for i in pdf:
        provvisorio = i['href']
        provvisorio = provvisorio[2:]
        url_completo = 'https://cir-reports.cir-safety.org/' + provvisorio
        siti_pdf.append(url_completo)
        print(url_completo)
    print("inserire il nome delle parole ce si vogliono cercare, quando finito digita exit")
    parole_da_trovare = tante
    
    for i in siti_pdf:
        lettura(i, parole_da_trovare)

def farmaci(farmaco,tante):
    with open("/workspaces/2023-25.BD.UFS14/Calzavara/MyProjFolder/cir.html", "r", encoding="utf-8") as web:
        content = web.read()
        #url = "https://cir-reports.cir-safety.org/"    # Analizza il contenuto HTML con BeautifulSoup
        #response = requests.get(url)
        #soup = BeautifulSoup(response.text, 'html.parser')
        soup = BeautifulSoup(content, 'html.parser')
        siti = soup.find_all('a')
        url=[]
        for i in siti:
            url_completo = 'https://cir-reports.cir-safety.org' + i['href']
            url.append(url_completo)
        lista = [lista.text for lista in siti]
    #print(lista)
    if farmaco not in lista:
        print("il farmaco non è presente oppure il nome non è completo")
        return
    else:
        print("successo")
        indice = lista.index(farmaco)
        PDF(url[indice],tante)
        return



url = "https://www.cir-safety.org/ingredients"  # URL del sito web
import PyPDF2
def lettura(url):
    response = requests.get(url)
    pierino = response.content
    return pierino
    # Salva il contenuto del PDF in un file locale
#    with open("C:/Users/FabioCalzavara/OneDrive - ITS Angelo Rizzoli/Desktop/FINITI/Project Work/file.pdf", 'wb') as file:
#        file.write(response.content)
