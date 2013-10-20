from flask import Flask, request #@UnresolvedImport
from services.NetworkRequestController import NetworkRequestController
from types import ListType, UnicodeType

# if __name__ == '__main__':
    
app = Flask(__name__)

@app.route('/test')
def hello_world():
    return 'Hello World!'

@app.route('/network_request', methods=['POST'])
def network_request():
    if not request.json or 'message' not in request.json or 'recipients' not in request.json:
        abort(400)

    recipients = request.json['recipients']
    message = request.json['message']

    if isinstance(recipients, ListType) and isinstance(message, UnicodeType):
        return NetworkRequestController.handle_routing(message, recipients)
    else:
        abort(400)
        
    
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)