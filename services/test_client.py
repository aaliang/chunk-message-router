import urllib
import urllib2
import json


def make_requests(num, url):

#     recipients = [str(x) for x in xrange(num)]
    recipients = ['1', '2', '3']
    value = {'message' : 'SendHub Rocks!',
          'recipients' : recipients
          }

    data = json.dumps(value)

    try:
      
        req = urllib2.Request(url, data, {'Content-Type': 'application/json'})
         
        f = urllib2.urlopen(req)
        response = f.read()
        f.close()
        print response

        
    except Exception, e:
        print e

if __name__ == '__main__':
    
    url = "http://localhost:5000/network_request"
#     url = "http://guarded-plains-1377.herokuapp.com/network_request"

    #for i in xrange(5000):
#         make_requests(i, url)


    make_requests(0, url)