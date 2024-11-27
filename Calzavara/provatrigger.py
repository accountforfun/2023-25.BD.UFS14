import azure.functions as func
import logging
import requests
from bs4 import BeautifulSoup
import PyPDF2


app = func.FunctionApp()

@app.route(route="MyHttpTrigger", auth_level=func.AuthLevel.ANONYMOUS)
def MyHttpTrigger(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    name = req.params.get('name')
    tante = []
    
    # Collect all search words
    while True:
        parole_da_trovare = req.params.get('parole')
        if parole_da_trovare:
            tante.append(parole_da_trovare)
        else:
            break  # Stop when no more search words are provided
    
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
    
    # Process the drug search and keyword search
    if name:
        farmaci(name, tante)
        return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully.")
    else:
        return func.HttpResponse(
             "ciao! This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )

def farmaci(farmaco, tante):
    with open("/workspaces/2023-25.BD.UFS14/Calzavara/MyProjFolder/cir.html", "r", encoding="utf-8") as web:
        content = web.read()
        soup = BeautifulSoup(content, 'html.parser')
        sites = soup.find_all('a')
        urls = ['https://cir-reports.cir-safety.org' + i['href'] for i in sites]
        names = [i.text for i in sites]

    if farmaco not in names:
        print("Farmaco non trovato.")
        return
    else:
        print("Farmaco trovato!")
        index = names.index(farmaco)
        PDF(urls[index], tante)

def PDF(url, tante):
    print("Fetching PDF from:", url)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    pdf_links = soup.find_all('a')[2:]
    
    siti_pdf = []
    for link in pdf_links:
        pdf_url = 'https://cir-reports.cir-safety.org/' + link['href'][2:]
        siti_pdf.append(pdf_url)
        print(pdf_url)

    for pdf_url in siti_pdf:
        pdf_text = lettura(pdf_url)
        if pdf_text:
            if search_keywords_in_pdf(pdf_text, tante):
                print(f"Keyword(s) found in the PDF: {pdf_url}")
        else:
            print(f"Failed to read PDF: {pdf_url}")

def lettura(url):
    response = requests.get(url)
    if response.status_code == 200:
        pdf_file = response.content
        try:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
            return text
        except PyPDF2.errors.PdfReadError:
            logging.error(f"Error reading PDF from {url}")
            return None
    else:
        logging.error(f"Failed to fetch the PDF from {url}")
        return None

def search_keywords_in_pdf(pdf_text, keywords):
    for keyword in keywords:
        if keyword.lower() in pdf_text.lower():
            print(f"Keyword '{keyword}' found in PDF!")
            return True
    return False
