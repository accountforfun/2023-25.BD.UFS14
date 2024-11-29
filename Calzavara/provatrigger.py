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
    cognome = req.params.get('cognome')
    eta = req.params.get('eta')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:
        if cognome:
            if eta:
                return func.HttpResponse('topo gigio')
            return func.HttpResponse(f"Hello, {name} {cognome}. This HTTP triggered function executed successfully.")
        return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully.")
    else:
        return func.HttpResponse(
             "ciaoThis HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )


import azure.functions as func
import logging
import requests
from bs4 import BeautifulSoup
import PyPDF2
import io

app = func.FunctionApp()

# Funzione per estrarre testo da un PDF dato un URL
def estrai_testo_pdf(url):
    response = requests.get(url)
    pdf_file = PyPDF2.PdfReader(io.BytesIO(response.content))
    
    testo_completo = ""
    for pagina in pdf_file.pages:
        testo_completo += pagina.extract_text()
        
    return testo_completo

# Funzione che cerca le parole in un testo (pdf_text)
def cerca_parole_in_testo(parole, testo):
    righe_con_parola = []
    
    # Dividi il testo in righe
    righe = testo.split('\n')
    
    for riga in righe:
        for parola in parole:
            if parola.lower() in riga.lower():  # Confronto case-insensitive
                righe_con_parola.append(riga)
                break  # Se la parola è trovata, aggiungi la riga e passa alla riga successiva
    
    return righe_con_parola

# Funzione che invia i dati
def invio(data):
    try:
        response = requests.post(f'/workspaces/2023-25.BD.UFS14/Calzavara/Estensimetro Esempio Letture.csv.csv', json=data)
        response.raise_for_status()  
        logging.info('Dati inviati correttamente a Zion.')
    except requests.exceptions.RequestException as e:
        logging.error(f'Errore nell\'invio dei dati: {e}')

# Funzione di esempio che risponde a una richiesta HTTP
@app.route(route="MyHttpTrigger", auth_level=func.AuthLevel.ANONYMOUS)
def MyHttpTrigger(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    name = req.params.get('name')
    
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')
    
    if not name:
        return func.HttpResponse(f"Inserire il nome del farmaco che si vuole cercare")
    
    return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully.")

# Funzione per cercare le parole nel testo PDF
@app.route(route="cercaParoleNelPdf", auth_level=func.AuthLevel.ANONYMOUS)
def cerca_parole(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Funzione HTTP chiamata per cercare parole nel testo PDF.')
    
    # Recupera le parole da cercare dalla query string
    parole = req.params.get('parole')
    if not parole:
        return func.HttpResponse("Per favore, inserisci le parole da cercare nella query string.", status_code=400)
    
    # Dividi le parole separate da virgola
    parole = parole.split(',')
    
    # URL del PDF (puoi modificarlo come necessario)
    url_pdf = "https://example.com/your_pdf.pdf"
    
    # Estrai il testo dal PDF
    pdf_text = estrai_testo_pdf(url_pdf)
    
    # Cerca le parole nel testo estratto
    righe_con_parola = cerca_parole_in_testo(parole, pdf_text)
    
    if righe_con_parola:
        risultato = "Le seguenti righe contengono le parole cercate:\n"
        risultato += "\n".join(righe_con_parola)
        return func.HttpResponse(risultato, status_code=200)
    else:
        return func.HttpResponse("Nessuna riga contiene le parole cercate.", status_code=200)



import azure.functions as func
import math
import requests
import logging

# Funzione per calcolare la distanza tra due coordinate geografiche usando la formula Haversine
def haversine(lat1, lon1, lat2, lon2):
    R = 6371.0  # Raggio della Terra in chilometri
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    
    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    distance = R * c  # Distanza in chilometri
    return distance

# Funzione per ottenere le coordinate (latitudine, longitudine) di un indirizzo
def get_coordinates(address):
    url = f'https://nominatim.openstreetmap.org/search?q={address}&format=json&addressdetails=1'
    response = requests.get(url)
    data = response.json()

    if data:
        # Prende la prima risposta dalla lista e restituisce latitudine e longitudine
        lat = float(data[0]['lat'])
        lon = float(data[0]['lon'])
        return lat, lon
    else:
        return None, None

app = func.FunctionApp()

@app.route(route="MyHttpTrigger", auth_level=func.AuthLevel.ANONYMOUS)
def MyHttpTrigger(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    # Prendi gli indirizzi dalla query string
    address1 = req.params.get('address1')
    address2 = req.params.get('address2')

    if address1 and address2:
        # Ottieni le coordinate per entrambi gli indirizzi
        lat1, lon1 = get_coordinates(address1)
        lat2, lon2 = get_coordinates(address2)

        if lat1 is None or lat2 is None:
            return func.HttpResponse(
                "Errore nella geocodifica degli indirizzi. Assicurati che gli indirizzi siano corretti.",
                status_code=400
            )
        
        # Calcola la distanza tra i due punti
        distance = haversine(lat1, lon1, lat2, lon2)
        
        return func.HttpResponse(
            f"La distanza tra '{address1}' e '{address2}' è di {distance:.2f} km.",
            status_code=200
        )
    else:
        return func.HttpResponse(
            "Per favore, passa i parametri 'address1' e 'address2' nella query string.",
            status_code=400
        )
