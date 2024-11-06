import pandas as pd
import requests
import time
import logging
from datetime import datetime
from jsonschema import validate

intervallo = 10

device_token='test_device_2024'

AL = 2.6647E-02
BL = -7.2683E+01

AP = 7.0405E-12
BP = -1.0504E-07
CP = 2.7117E-02
DP = -7.3308E+01

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
# Funzione per leggere il file CSV
def read_csv(file_path):
    df = pd.read_csv(file_path, sep=';', header=0)
    logging.info('File CSV letto correttamente.')
    return df


# Funzione per applicare le trasformazioni
def trasformazione(dati):
    dati['Value'] = dati['Value'].replace(',','',regex=True)
    valore = pd.to_numeric(dati['Value'], errors='coerce')
    for i in valore:
        time.sleep(intervallo)
        trasformaL = i * AL + BL
        trasformaP = i ** 3 * AP + i ** 2 * BP + i * CP + DP
        timestamp = datetime.now().isoformat()
    info = {
        'Timestamp': timestamp,
        'data': {
            'TrasformaL': trasformaL,
            'TrasformaP': trasformaP
        }
    }
    
    invio(info)
    return info
        
def invio(data):
    try:
        response = requests.post(f'https://zion.nextind.eu/api/v1/{device_token}/telemetry', json=data)
        response.raise_for_status()  
        logging.info('Dati inviati correttamente a Zion.')
    except requests.exceptions.RequestException as e:
        logging.error(f'Errore nell\'invio dei dati: {e}')
df = read_csv("C:/Users/FabioCalzavara/OneDrive - ITS Angelo Rizzoli/Desktop/Internet of Things/Estensimetro Esempio Letture.csv.csv")
def test_csv(snapshot):
    snapshot.snapshot_dir = 'snapshots'  # This line is optional.
    pierino = str(func(5))
    snapshot.assert_match(pierino, 'foo_output.txt')
    
schema = {"type" : "object",
    "properties" : {
        "price" : {"type" : "number"},
        "name" : {"type" : "string"},
    },}

def test_json(schema):
    instance = trasformazione(df)
    try:
        validate(instance = instance, schema = schema)
        return True
    except:
        return False
if df is not None:
    trasformazione(df)