import json
import logging
import azure.functions as func

# def main(event: func.EventGridEvent, outdoc: func.Out[func.Document]):
def main(event: func.EventGridEvent):
    try:
        result = {
        'id': event.id,
        'data': event.get_json(),
        'topic': event.topic,
        'subject': event.subject,
        'event_type': event.event_type,
        }
        logging.info(event.get_json().decode('utf-8'))
        # json_data = event.get_json()["properties"]
        # logging.info('json_data: %s', json_data)
        # logging.info("-----------------------------------------------------------------")
        # logging.info(event)
        
        # outdoc.set(func.Document.from_dict(result))
        # {
        # "type": "cosmosDB",
        # "direction": "out",
        # "name": "outdoc",
        # "databaseName": "tracktech",
        # "collectionName": "tracktech",
        # "createIfNotExists": "true",
        # "connectionStringSetting": "AzureCosmosDBConnectionString"
        # }
    except Exception as ex:
        logging.info('Exception because of: %s', str(ex))
