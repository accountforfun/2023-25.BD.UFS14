import requests
from bs4 import BeautifulSoup

def PDF(url):
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
    parole_da_trovare = []
    while True:
        parole_sante = (input(str()))
        if parole_sante == 'exit':
            break
        parole_da_trovare.append(parole_sante)
    for i in siti_pdf:
        lettura(i, parole_da_trovare)
    
    #for i in siti_pdf:
    #   lettura(i)
def farmaci(farmaco):
    with open("C:/Users/FabioCalzavara/OneDrive - ITS Angelo Rizzoli/Desktop/cir.html", "r", encoding="utf-8") as web:
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
        PDF(url[indice])
        return

farmaco = str(input("inserisci il farmaco: "))
farmaci(farmaco)
url = "https://www.cir-safety.org/ingredients"  # URL del sito web
import PyPDF2
def lettura(url):
    response = requests.get(url)
    pierino = response.content
    return pierino
    # Salva il contenuto del PDF in un file locale
    with open("C:/Users/FabioCalzavara/OneDrive - ITS Angelo Rizzoli/Desktop/FINITI/Project Work/file.pdf", 'wb') as file:
        file.write(response.content)
    
lettura('https://cir-reports.cir-safety.org//view-attachment?id=94742a1a-c561-614f-9f89-14ce58abfc0b')
'''
def test_function_output_snapshot(snapshot):
    snapshot.snapshot_dir = 'snapshots'  # This line is optional.
    pierino = lettura('https://cir-reports.cir-safety.org//view-attachment?id=94742a1a-c561-614f-9f89-14ce58abfc0b')
    snapshot.assert_match(pierino, 'pdf_output.txt')
'''