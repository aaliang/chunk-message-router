from flask import Flask, request #@UnresolvedImport
from services.NetworkRequestController import NetworkRequestController
from types import ListType, UnicodeType, DictType
import logging
import os
import json
 

app = Flask(__name__)
logger = logging.getLogger("__name__")

@app.route('/network_request', methods=['POST'])
def network_request():
    if not request.json or 'message' not in request.json or 'recipients' not in request.json:
        abort(400)
 
    recipients = request.json['recipients']
    message = request.json['message']
 
    if isinstance(recipients, ListType) and isinstance(message, UnicodeType):
        try:
            return response_as_json(
                NetworkRequestController.handle_routing(message, recipients)
            )
        except Exception, e:
            logger.error(e.message)
            abort(500)
    else:
        abort(400)
         

def response_as_json(response):
    """
        Returns JSONified representation of the response
    """
    assert isinstance(response, DictType)
    return json.dumps(response)
        

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='127.0.0.1', port=port)


