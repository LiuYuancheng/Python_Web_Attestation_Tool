#!/usr/bin/python
#-----------------------------------------------------------------------------
# Name:        webAttestation.py
#
# Purpose:     This module is used to do the url/web attestation (find the phashing
#              or malicious web)by using the NUS-Phishperida API. The user can list 
#              all the urls he wants to check in the file "urllist.txt".
#              For each url, the program will do below steps:
#               1. use webDownloader module to download all the web components.
#               2. use webScreenShoter module to get a screenshot of the webpage.
#               3. pass the web components and the screen shot to Phishperida API
#               to do the phishing web/url checking. 
#
# Author:      Yuancheng Liu
#
# Created:     2021/11/25
# Version:     v_0.1.2
# Copyright:   Copyright (c) 2024 LiuYuancheng
# License:     MIT License 
#-----------------------------------------------------------------------------
import os
from urllib.parse import urlparse

import ConfigLoader as cfgL
import webDownloader as webDL
import webScreenShoter as webSS
#import phishpediaPKG as webPH

GV_FLG = True  # Flag to identify whether use global value

if GV_FLG: import webGlobal as gv

URL_RCD = gv.URL_LIST if GV_FLG else 'urllist.txt'  # file to save url list
RST_DIR = gv.DATA_DIR if GV_FLG else 'datasets'
URL_PCD_RCD = gv.URL_PCD_RCD if GV_FLG else "resultPcdurl.txt"
URL_ERR_RCD = gv.URL_ERR_RCD if GV_FLG else "resultErrurl.txt"

dlImg = gv.iDlImg if GV_FLG else True # download image
dlHref = gv.iDLHref if GV_FLG else True # download the components linked by href.
dlScript = gv.iDlScript if GV_FLG else True # download java scripts

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
def fileFunc(line):
    if 'http' in line: return True
    return False

def main():
    dataLoader = cfgL.ConfigLoader(URL_RCD, mode='r', logFlg=True)
    pcdLoader = cfgL.ConfigLoader(URL_PCD_RCD, mode='ra', logFlg=True)
    pcdLoader.appendLine('>Start', timeFlg=True, cmtChar='#') # Append the time rcd
    errLoader = cfgL.ConfigLoader(URL_ERR_RCD, mode='w', logFlg=True)
    errLoader.appendLine('>Start', timeFlg=True, cmtChar='#') # Append the time rcd
    downloader = webDL.webDownloader(imgFlg=dlImg, linkFlg=dlHref, scriptFlg=dlScript)
    capturer = webSS.webScreenShoter()
    #checker = webPH.phishperidaPKG()
    urlCount = failCount= 0
    outputFolder = os.path.join(gv.dirpath,  "outputFolder")
    if not os.path.exists(outputFolder): os.mkdir(outputFolder)
    if not os.path.exists(RST_DIR): os.mkdir(RST_DIR)
    print("> load url record file: %s" %URL_RCD)
    #allurls = set(dataLoader.getLines(filterFun=fileFunc))
    #pcdurls = set(pcdLoader.getLines(filterFun=fileFunc))
    # urllines = allurls - pcdurl # YC: Not use set as we want keep the url sequece.
    allurls = dataLoader.getLines(filterFun=fileFunc)
    pcdurls = pcdLoader.getLines(filterFun=fileFunc)
    print("> Ignore %s processed urls" %str(len(pcdurls)))
    urllines = [x for x in allurls if x not in pcdurls]
    for line in urllines:
        urlCount += 1
        domain = str(urlparse(line).netloc)
        downloadFolderPath = os.path.join(outputFolder,'_'.join((str(urlCount), domain)))
        result_d = downloader.downloadWebContents(line, downloadFolderPath)
        result_c = capturer.getScreenShot(line, downloadFolderPath)
        #result_p = checker.phishperidaCheck(RST_DIR)
        # soup.savePage('https://www.google.com', 'www_google_com')
        if result_d and result_c: 
            print('> Finished.')
            pcdLoader.appendLine(line)
        else:
            failCount +=1
            errLoader.appendLine(line)
    pcdLoader.appendLine('End', timeFlg=True, cmtChar='#') # Append the time rcd
    errLoader.appendLine('End', timeFlg=True, cmtChar='#') # Append the time rcd

    print("\n> Download result: download %s url, %s fail" %(str(urlCount), str(failCount)))

#-----------------------------------------------------------------------------
if __name__ == '__main__':
    main()
