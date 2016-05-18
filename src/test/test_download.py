import urllib.request, urllib.parse, urllib.error
import gzip
import io
from bs4 import BeautifulSoup
import re


header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:26.0) Gecko/20100101 Firefox/26.0',
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
'Accept-Encoding': 'gzip, deflate',
'Connection': 'keep-alive'}

req = urllib.request.Request("http://esf.fang.com/house/i31/", headers=header)


doc = urllib.request.urlopen(req)


string = doc.read()

if doc.info().get('content-encoding')=='gzip':
    outdata = io.BytesIO(string)
    gf = gzip.GzipFile(fileobj=outdata,mode='rb')
    newob = gf.read().decode('gbk')
else:
# 如果不是则正常转码
    newob = string.decode('gbk')

#print(type(doc))

#print(type(newob))

#print(newob)

soup = BeautifulSoup(newob, "html.parser")

#soup.find_all(id=re.compile('\blist_\w\d{2}_\d{2}\b'))

houseL = soup.find_all(id=re.compile('list_D03_\d{2}'))

for eachhouse in houseL:
    print(eachhouse.find('p', class_="mt10").find('a').find('span').string)







