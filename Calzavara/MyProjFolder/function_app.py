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
                tempo_rimanente = 100 - int(eta)
                if tempo_rimanente <= 0:
                    return func.HttpResponse('You are already dead')
                if tempo_rimanente > 95:
                    return func.HttpResponse('Tooo much')
                return func.HttpResponse(f'Per arrivare a 100 anni ti mancano {tempo_rimanente} anni')
            return func.HttpResponse(f"Hello, {name} {cognome}. To know how many years you need to reach 100 years, insert your age.")
        return func.HttpResponse(f"Hello, {name}. Pleaseeee, insert your surname so we can schedule you and steal all your data")
    else:
        return func.HttpResponse(
             "Hello, This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )