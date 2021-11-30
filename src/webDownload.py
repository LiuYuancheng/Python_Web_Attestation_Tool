#!/usr/bin/python
#-----------------------------------------------------------------------------
# Name:        webDownload.py
#
# Purpose:     This module will provide API to download the webpage components: 
#              html file, image file, javascript file, href link file based on 
#              the input url. The user can list all the url he wants to downlad 
#              in the file "urllist.txt" .
#
# Author:      Yuancheng Liu
#
# Created:     2021/11/12
# Version:     v_0.1
# Copyright:   n.a
# License:     n.a
#-----------------------------------------------------------------------------

import os, sys
import re
import requests
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup

GV_FLG = True # Flag to identify whether use gloval value

if GV_FLG: import webGlobal as gv
URL_RCD = gv.URL_LIST if GV_FLG else 'urllist.txt' # file to save url list
RST_DIR = gv.DATA_DIR if GV_FLG else 'datasets'
URL_FN = 'info.txt' # url file name 

#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
class urlDownloader(object):
    """ Download the webpage components base on the input url."""
    def __init__(self, imgFlg=True, linkFlg=True, scriptFlg=True):
        self.url = ''
        self.soup = None
        self.imgFlg = imgFlg
        self.linkFlg = linkFlg
        self.scriptFlg = scriptFlg
        self.session = requests.Session()
        
    #-----------------------------------------------------------------------------
    def savePage(self, url, pagefilename='page', txtMD=True):
        """ Save the web page components based on the input url and dir path.
        Args:
            url ([try]): web url string.
            pagefilename (str, optional): path to save the web components.
        Returns:
            [bool]: whether the components saved the successfully.
        """
        self.url = url
        try:
            response = self.session.get(url)
            self.soup = BeautifulSoup(response.text, features="lxml")
            pagefolder =os.path.join( RST_DIR, pagefilename) # page contents
            if not os.path.exists(pagefolder): os.mkdir(pagefolder)
            if self.imgFlg: self._soupfindnSave(pagefolder, tag2find='img', inner='src')
            if self.linkFlg: self._soupfindnSave(pagefolder, tag2find='link', inner='href')
            if self.scriptFlg: self._soupfindnSave(pagefolder, tag2find='script', inner='src')
            with open(os.path.join(pagefolder, pagefilename+'.html'), 'wb') as file:
                file.write(self.soup.prettify('utf-8'))
            if txtMD: 
                # record the page url under text mode: 
                with open(os.path.join(pagefolder, URL_FN), "a+", encoding='ISO-8859-1') as f:
                    f.write(self.url)
            return True
        except Exception as e:
            print("> savePage(): create files failed: %s." % str(e))
            return False

    #-----------------------------------------------------------------------------
    def _soupfindnSave(self, pagefolder, tag2find='img', inner='src'):
        """ Saves on specified pagefolder all tag2find objects. """
        pagefolder = os.path.join(pagefolder, tag2find)
        if not os.path.exists(pagefolder): os.mkdir(pagefolder)
        for res in self.soup.findAll(tag2find):   # images, css, etc..
            try:
                if not res.has_attr(inner): continue # check if inner tag (file object) exists
                # clean special chars such as '@, # ? <>'
                filename = re.sub('\W+', '.', os.path.basename(res[inner]))
                # print("> filename:", filename)
                # Added the '.html' for the html file in the href
                if tag2find == 'link':
                    if not any(ext in filename for ext in ['css', 'png', 'ico', 'jpg', 'jpeg', 'mov', 'ogg', 'gif', 'xml','js']):
                        filename += '.html'
                fileurl = urljoin(self.url, res.get(inner))
                filepath = os.path.join(pagefolder, filename)
                # rename html ref so can move html and folder of files anywhere
                res[inner] = os.path.join(os.path.basename(pagefolder), filename)
                # create the file.
                if not os.path.isfile(filepath):
                    with open(filepath, 'wb') as file:
                        filebin = self.session.get(fileurl)
                        if len(filebin.content) > 0: # filter the empty file(imge not found)
                            file.write(filebin.content)
            except Exception as exc:
                print(exc, file=sys.stderr)


#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
def main():
    soup = urlDownloader(imgFlg=True, linkFlg=True, scriptFlg=True)
    count = failCount= 0
    if not os.path.exists(RST_DIR): os.mkdir(RST_DIR)
    print("> load url record file %s" %URL_RCD)
    with open(URL_RCD) as fp:
        urllines = fp.readlines()
        for line in urllines:
            if line[0] in ['#', '', '\n', '\r', '\t']: continue # jump comments/empty lines.
            count += 1
            print("> Process URL {}: {}".format(count, line.strip()))
            if ('http' in line):
                line = line.strip()
                domain = str(urlparse(line).netloc)
                folderName = "_".join((str(count), domain))
                result = soup.savePage(line, folderName)
                # soup.savePage('https://www.google.com', 'www_google_com')
                if result: 
                    print('Finished.')
                else:
                    failCount +=1
    print("\n> Download result: download %s url, %s fail" %(str(count), str(failCount)))

#-----------------------------------------------------------------------------
if __name__ == '__main__':
    main()
