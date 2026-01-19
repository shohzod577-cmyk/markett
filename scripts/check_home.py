import urllib.request
import sys
try:
    r = urllib.request.urlopen('http://127.0.0.1:8000', timeout=5)
    print('STATUS', r.getcode())
    data = r.read(200).decode('utf-8', errors='replace')
    print(data)
except Exception as e:
    print('ERROR', e)
    sys.exit(1)
