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