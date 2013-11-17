import urllib
import urllib2
import json

from utils.MessageRelays import MessageRelays


#pointing to heroku
#url = "http://guarded-plains-1377.herokuapp.com/send_message/unicast"

#local url
url = "http://localhost:5000/send_message/unicast"

#hastily created test client to validate quickly certain parts of the app
#note: using this script is not sufficient in itself to test correctness

def create_request(message, recipients):
    """
        Creates a json request object
    """

    value = {'message' : message,
          'recipients' : recipients
          }
    
    return json.dumps(value)
    
def make_requests_with_n_recipients(num, url):
    """
        Makes request with {num} unique recipients
    """
    recipients = [str(x) for x in xrange(num)]

    data = create_request('TEST MESSAGE!', recipients)
    return call_api_endpoint(url, data)

def call_api_endpoint(url, data):
    """
        returns the response if successful
    """
    try:
      
        req = urllib2.Request(url, data, {'Content-Type': 'application/json'})
         
        f = urllib2.urlopen(req)
        response = f.read()
        f.close()
        return response

        
    except urllib2.HTTPError, e:
        if e.code == 400:
            return -1

def validate_response(recipients, response):
    """
        Validates that this is a solution
    """
    
    result_obj = json.loads(response)
    assert 'message' in result_obj
    assert 'routes' in result_obj
    
    total = 0
    for r in result_obj['routes']:
        assert 'ip' in r
        num_r = len(r['recipients'])

        #sum the number of recipients
        total += num_r

        relay_type = MessageRelays.get_relay_type_by_throughput(num_r)
        subnet_split = relay_type.subnet_prefix.split('.')
        ip_split = r['ip'].split('.')
        
        #make sure the subnet is correct
        assert ip_split[2] == subnet_split[2]
            
    assert total == len(recipients)

def run_tests():
    
    #test for no recipients
    result = make_requests_with_n_recipients(0, url)
    assert result == -1, result

    #test for 5000 recipients
    
    recipients = range(5000)
    request = create_request('TEST MESSAGE!', recipients)
    result = call_api_endpoint(url, request)
    assert result != -1, result
    print result
    validate_response(recipients, result)
    
    
    #test for 983 recipients
    
    recipients = range(983)
    request = create_request('TEST MESSAGE!', recipients)
    result = call_api_endpoint(url, request)
    assert result != -1, result
    print result
    validate_response(recipients, result)
    
    
    request = create_request('test', [1,1])
    result = call_api_endpoint(url, request)
    assert result == -1, result

if __name__ == '__main__':
    print 'starting tests'
    run_tests()
    print 'tests passed'


    
