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
    info = {'Timestamp': 'string',
    'data': {
        'TrasformaL': 'number',
        'TrasformaP': 'number'
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

def test_csv(snapshot):
    df = read_csv("/workspaces/2023-25.BD.UFS14/Calzavara/Estensimetro Esempio Letture.csv.csv")
    snapshot.snapshot_dir = 'snapshots'  
    pierino = str(df)
    snapshot.assert_match(pierino, 'es_output.txt')
    
schema = {
    'Timestamp': 'object',
    'data': {
            'TrasformaL': 'float',
            'TrasformaP': 'float'
        }
    }
def bool_validate(instance, schema):
    try:
        validate(instance = instance, schema = schema)
        return True
    except:
        return False
def test_json():
    assert bool_validate(instance=trasformazione(df), schema=schema) == True


def func(x):
    return x+1

def test_answer():
    assert func(3) == 4

df = read_csv("/workspaces/2023-25.BD.UFS14/Calzavara/Estensimetro Esempio Letture.csv.csv")
if df is not None:
    trasformazione(df)