#coding=utf-8

import hashlib
import json
import io
import httplib2
import gzip
import time
import random
import sys
import os
import platform
import re
from bs4 import BeautifulSoup
import urllib

def download_page_by_url(str_url):
    #print('start download ...')
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:26.0) Gecko/20100101 Firefox/26.0',
              'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
              'Accept-Encoding': 'gzip, deflate',
              'Connection': 'keep-alive'}
    '''
    req = urllib.request.Request(str_url, headers=header)
    rsp = urllib.request.urlopen(req)
    string = rsp.read()

    if rsp.info().get('content-encoding') == 'gzip':
        out_data = io.BytesIO(string)
        gf = gzip.GzipFile(fileobj=out_data, mode='rb')
        curr_page = gf.read().decode('gbk')
    else:
        curr_page = string.decode('gbk')
    '''

    h = httplib2.Http(timeout=30)
    finish_get = False
    retry = 5
    #str_url = re.match('^(.*\?)(.*)', str_url).group(1) + urllib.parse.quote_plus(re.match('^(.*\?)(.*)', str_url).group(2))
    str_url = str_url.replace(' ','%20')
    while (not finish_get) :
        try:
            #print('downloading %s' % str_url)
            resp, content = h.request(str_url,headers=header)
            finish_get = True
        except:
            print('get fail : %s' % str_url)
            retry = retry - 1
            if (retry<=0) :
                raise

            second = random.uniform(10, 20)
            time.sleep(second)
    #print('get ...')
    try:
        curr_page = content.decode('gb18030')
        #print('decode ...')
    except:
        #enc = chardet.detect(content)
        #curr_page = content.decode(enc['encoding'])
        curr_page = content.decode('gb18030','ignore')
        print('decode ignore ...')

    #print('end download .')

    return curr_page

def save_page(new_file, str_url, curr_page):
    # print("文件名: ",  newFile.name)
    # fo.seek(0, 2)
    new_file.write(str_url+'\n')
    new_file.write(curr_page)
    new_file.close()
    return

def get_md5(str_url: str):
    md5 = hashlib.new('md5')
    md5.update(str_url.encode("utf-8"))
    return md5.hexdigest()

def create_dirs(str_dirs):
    if not os.path.exists(str_dirs):
        os.makedirs(str_dirs)
    return

def get_href(url, href):
    rtn = href
    urlBase = re.match('^(.*/)', url).group()
    if re.match('^(http://)', href) == None:
        rtn = urlBase + href
    return rtn

def download_or_cache(filePath, url):
    #print ('start download_or_cache ...')
    page = None;
    if os.path.exists(filePath):
        #print('loading ...')
        file = open(filePath, "r+", encoding='utf-8')
        url = file.readline()
        page = file.read()
        file.close()
    else:
        #print('downloading ...')
        page = download_page_by_url(url);
        #print('new file ...')
        newF = open(filePath, 'w', encoding='utf-8')
        #print('saving ...')
        save_page(newF, url, page)
    #print ('end download_or_cache .')
    return page


create_dirs('listPages')
create_dirs('prjPages')
create_dirs('suPages')
create_dirs('sbPages')
create_dirs('housePages')

downloadUrlList = []
for i in range(1,len(sys.argv),1) :
    downloadUrlList.insert(0, sys.argv[i])
downloadPrjUrlList = []
downloadBldUrlList = []
downloadHUrlList = []

while len(downloadUrlList)>0 :
    dUrl = downloadUrlList.pop();
    print ('list page (%d : %s) : %s'%(len(downloadUrlList)+1,get_md5(dUrl),dUrl))
    downloadFilePath = 'listPages' + os.sep + get_md5(dUrl) + ".txt"
    page = download_or_cache(downloadFilePath,dUrl)

    soup = BeautifulSoup(page, "html.parser")
    nextUrl = None
    if (soup.find('a', string='[下一页]')!=None) :
        nextUrl = soup.find('a', string='[下一页]')['href']
    if nextUrl!=None :
        downloadUrlList.insert(0, get_href(dUrl, nextUrl))
        #downloadUrlList.append(get_href(dUrl, nextUrl))

    search = '总套数'
    if (soup.find('td',string=search)==None):
        search = '总面积'
    data_base = soup.find('td',string=search).parent.parent
    #print(data_base)
    for data_item in data_base.find_all('tr',onmouseout=True):
        #print(data_item)
        dataList = []
        for sibling in data_item.find_all('td'):
            #print(sibling)
            if (sibling.string!=None):
                dataList.append(sibling.string)

            if sibling.find('a') != None :
                prjUrl = get_href(dUrl, sibling.find('a')['href'])
                #print(prjUrl)
                dataList.insert(0, get_md5(prjUrl))
                downloadPrjUrlList.append(prjUrl)

        print(dataList) # 项目数据: projectID,......

        dpUrl = downloadPrjUrlList.pop()
        print('project page (%d - %d : %s) : %s' % (len(downloadUrlList)+1,len(downloadPrjUrlList)+1,get_md5(dpUrl),dpUrl))
        downloadPrjFilePath = 'prjPages' + os.sep + get_md5(dpUrl) + ".txt"
        page2 = download_or_cache(downloadPrjFilePath, dpUrl)

        soup2 = BeautifulSoup(page2, "html.parser")
        if (soup2.find('iframe', id='SUList') != None):
            data_item2 = soup2.find('iframe', id='SUList')
            suUrl = get_href(dpUrl, data_item2['src'])
            #print(suUrl)
            downloadSUFilePath = 'suPages' + os.sep + get_md5(suUrl) + ".txt"
            page3 = download_or_cache(downloadSUFilePath, suUrl)

            soup3 = BeautifulSoup(page3, "html.parser")
            for data_item3 in soup3.find_all('a', target='SBList'):
                sbUrl = get_href(suUrl, data_item3['href'])
                downloadBldUrlList.append(sbUrl)

                data_base3 = data_item3.parent.parent
                dataList3 = []
                dataList3.insert(0, get_md5(dpUrl))
                dataList3.insert(0, get_md5(sbUrl))
                for sibling3 in data_base3.find_all('td'):
                    if (sibling3.string != None):
                        dataList3.append(sibling3.string)
                print(dataList3) #预售证数据: salePermitID,projectID,......

            #print('start download building page ...')
            while len(downloadBldUrlList)>0 :
                sbUrl = downloadBldUrlList.pop()
                print('project building page (%d - %d - %d : %s) : %s' % (len(downloadUrlList)+1,len(downloadPrjUrlList)+1,len(downloadBldUrlList)+1,get_md5(sbUrl),sbUrl))
                downloadSBFilePath = 'sbPages' + os.sep + get_md5(sbUrl) + ".txt"
                page4 = download_or_cache(downloadSBFilePath, sbUrl)

                soup4 = BeautifulSoup(page4, "html.parser")
                for data_item4 in soup4.find_all('a', href=re.compile('^House')):
                    hUrl = get_href(sbUrl, data_item4['href'])
                    downloadHUrlList.append(hUrl)

                    data_base4 = data_item4.parent.parent
                    dataList4 = []
                    dataList4.insert(0, get_md5(dpUrl))
                    dataList4.insert(0, get_md5(sbUrl))
                    dataList4.insert(0, get_md5(hUrl))
                    for sibling4 in data_base4.find_all('td'):
                        if (sibling4.string != None):
                            dataList4.append(sibling4.string)
                    print(dataList4) #楼栋数据: buildingID,salePermitID,projectID,......

                #print('start download house page ...')
                while len(downloadHUrlList)>0 :
                    hUrl = downloadHUrlList.pop()
                    print('House page (%d - %d - %d - %d : %s) : %s' % (len(downloadUrlList)+1,len(downloadPrjUrlList)+1,len(downloadBldUrlList)+1,len(downloadHUrlList)+1,get_md5(hUrl),hUrl))
                    downloadHFilePath = 'housePages' + os.sep + get_md5(hUrl) + ".txt"
                    page5 = download_or_cache(downloadHFilePath, hUrl)

                    soup5 = BeautifulSoup(page5, "html.parser")


                #print('end download house page .')
            #print('end download building page .')

print('---end---')