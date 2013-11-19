from flask import Flask, request, abort, jsonify #@UnresolvedImport
from services.NetworkRequestController import NetworkRequestController
from types import ListType, UnicodeType, DictType, IntType
import logging
import os
import json
 

app = Flask(__name__)
logger = logging.getLogger("__name__")

@app.route('/send_message/unicast', methods=['POST'])
def route_message_request():
    if not request.json or 'message' not in request.json or 'recipients' not in request.json:
        abort(400)
 
    recipients = request.json['recipients']
    message = request.json['message']
 
    if isinstance(recipients, ListType) and isinstance(message, UnicodeType):
        len_recipients = len(recipients)
        if len_recipients == 0 or len_recipients > NetworkRequestController.MAX_RECIPIENTS:
            try:
                return ("Invalid Length", 400, {'message': 'Invalid length for input "recipients"'})
            except Exception, e:
                print e
        if len(set(recipients)) != len(recipients):
            return ("Invalid", 400, {'message': 'Invalid input "recipients", not unique'})
        
        try:
            return response_as_json(
                NetworkRequestController.handle_routing(message, recipients),
                200
            )
        except Exception, e:
            logger.debug(e.message, exc_info=1)
            abort(500)
    else:
        abort(400) #invalid request


def response_as_json(response, status):
    """
        Returns JSONified representation of the response
    """
    assert isinstance(response, DictType)
    assert isinstance(status, IntType)

    resp = jsonify(response)
    resp.status_code = status
    
    return resp

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='127.0.0.1', port=port)


