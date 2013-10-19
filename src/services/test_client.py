import urllib
import urllib2
import json

if __name__ == '__main__':
    
    url = "http://localhost:5000/network_request"
    
    recipients = [str(x) for x in xrange(5000)]
    
    
    value = {'message' : 'SendHub Rocks!',
          'recipients' : recipients
          }

    data = json.dumps(value)

    try:
      
        req = urllib2.Request(url, data, {'Content-Type': 'application/json'})
         
        f = urllib2.urlopen(req)
        response = f.read()
        f.close()
        
    except Exception, e:
        print e