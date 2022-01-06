from urllib.parse import urlparse
import re

# Test url list.
urlList = ["https://user:pwd[@example.com",
            "https://user:pwd[@example.com]",
            'https://pythön.com', 
            "https://user:pwd@example.com]",
            "https://[user:[pwd@example.com]",
            "https://[user]:[[[pwd@example.com]",
            "https://]user:[pwd@example.com]\n",
            "https://]user:[pwd@example.com][",
            "https://{]user:[pwd@example.com]",
            "https://العربية | أبرز الأخبار العالمية والمحلية العاجلة",
            ]

for urlStr in urlList:
    urlStr = urlStr.encode(encoding='UTF-8', errors='strict').decode()
    lCount = urlStr.count('[')
    rCount = urlStr.count(']')
    hIdex = urlStr.find("://")+3
    msg = urlStr
    if lCount > rCount: 
        msg = urlStr + ']' * (lCount - rCount)
    elif lCount < rCount:
       msg = urlStr[:hIdex] + '[' * (rCount - lCount) + urlStr[hIdex:]
    print(">> Process url %s" %str(msg))
    info = urlparse(msg)
    msg = re.sub('[\[\]]', '', msg)
    print(msg)
    print(info.path)
