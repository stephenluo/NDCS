import urllib.request, urllib.parse, urllib.error
import gzip
import io
from bs4 import BeautifulSoup
import re

header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:26.0) Gecko/20100101 Firefox/26.0',
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
'Accept-Encoding': 'gzip, deflate',
'Connection': 'keep-alive'}

req = urllib.request.Request("http://esf.fang.com/house/i33/", headers=header)

doc = urllib.request.urlopen(req)

string = doc.read()

if doc.info().get('content-encoding')=='gzip':
    outdata = io.BytesIO(string)
    gf = gzip.GzipFile(fileobj=outdata,mode='rb')
    newob = gf.read().decode('gbk')
else:
# 如果不是则正常转码
    newob = string.decode('gbk')

#利用BeautifulSoup解析网页内容
soup = BeautifulSoup(newob, "html.parser")

houseL = soup.find_all(id=re.compile('list_D03_\d{2}'))



for eachhouse in houseL:
    estatename = eachhouse.find('p', class_="mt10").find('a').find('span').string
    estateaddress = eachhouse.find('p', class_="mt10").find('span', class_='iconAdress ml10 gray9').string
    estateinfoarray = eachhouse.find('p', class_="mt12")
    roomtype = estateinfoarray.contents[0].replace(' ', '').replace('\r\n', '')
    floor = estateinfoarray.contents[2].replace(' ', '').replace('\r\n', '')
    direct = estateinfoarray.contents[4].replace(' ', '').replace('\r\n', '')
    buildyear = estateinfoarray.contents[6].replace(' ', '').replace('\r\n', '').replace('\t', '')
    area = eachhouse.find('div', class_='area alignR').find('p').string
    totalprice = eachhouse.find('span', class_='price').string
    unitprice = eachhouse.find('p', class_='danjia alignR mt5').contents[0].replace(' ', '').replace('\r\n', '')

    #持久化...







