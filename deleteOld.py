import requests
import sys
print 'Deleting one week old or older data'
DELETE_ENDPOINT = "http://localhost:3000/data/old"
try:
    r = requests.delete(url = DELETE_ENDPOINT)
except requests.exceptions.RequestException as e:
    print e
    sys.exit(1)
print r.text
