import urllib3

http = urllib3.PoolManager()
print('Sending message')
r = http.request('POST',
                 'https://api.semaphore.co/api/v4/messages',
                 fields={
                   'apikey': '8c0bc3925af627aaea9cd0e809757e32',
                   'sendername': 'SUMALINOG',
                   'number': '09700583600,09128557496',
                   'message': 'HELLO FROM JOHN LG SUMALINOG'
                 })
print('Message sent')
