import azure.functions as func
import math
import requests
import logging


def cal_distanza(lat1, lon1, lat2, lon2):
    R = 6371.0
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    
    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    distanza = R * c
    return distanza


def coordinate_reali(indirizzo):
    url = f'https://nominatim.openstreetmap.org/search?q={indirizzo}&format=json&addressdetails=1'
    response = requests.get(url)
    data = response.json()

    if data:
       
        lat = float(data[0]['lat'])
        lon = float(data[0]['lon'])
        return lat, lon
    else:
        return None, None

app = func.FunctionApp()

@app.route(route="MyHttpTrigger", auth_level=func.AuthLevel.ANONYMOUS)
def MyHttpTrigger(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    
    indirizzo1 = req.params.get('indirizzo1')
    indirizzo2 = req.params.get('indirizzo2')

    if indirizzo1 and indirizzo2:
        
        lat1, lon1 = coordinate_reali(indirizzo1)
        lat2, lon2 = coordinate_reali(indirizzo2)

        if lat1 is None or lat2 is None:
            return func.HttpResponse(
                "Errore nella geocodifica degli indirizzi. Assicurati che gli indirizzi siano corretti.",
                status_code=400
            )
        
        
        distanza = cal_distanza(lat1, lon1, lat2, lon2)
        
        return func.HttpResponse(
            f"La distanza tra '{indirizzo1}' e '{indirizzo2}' è di {distanza:.2f} km.",
            status_code=200
        )
    else:
        return func.HttpResponse(
            "Per favore, passa i parametri 'indirizzo1' e 'indirizzo2' nella query string.",
            status_code=400
        )
