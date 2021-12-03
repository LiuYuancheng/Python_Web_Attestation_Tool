# WebAttestation
**Program Design Purpose**: We want to check several batch of web URLs (1~100 K) and find the phishing website/URL among them. 



[TOC]

### Introduction 

This module is designed to do the URL/web attestation by using the API from NUS-Phishperida-Project. The program contents four main parts: DatasetLoader ,WebDownloader, webScreenShoter and PhishperidaPKG. 



###### DatasetLoader

This module is used to load the URLs data from the URL list, record the processed URLs and error URLs. If the program/thread crashed, the program will continuous its task after restarting: the processed url will be ingored, then it will remove the corrupted file and continuous with not processed URLs 



###### WebDownloader

This module will provide API to download the webpage component: html file, image file, javascript file, href link file based on the input URL. 

**Module detail doc** : https://github.com/LiuYuancheng/WebAttestation/blob/main/WebDownloadReadme.md



###### WebScreenShoter

This module will use different web browser's driver or QT5-webEngine to capture the webpage's screen shot based on the given URL.

**Module detail doc** :https://github.com/LiuYuancheng/WebAttestation/blob/main/WebScreenShotReadme.md



###### PhishperidaPKG

This module is used to encapsulate the NUS-Phishperida project (not OOP) as a black box API for other projects to use.

NUS-Phishperida project: https://github.com/lindsey98/Phishpedia

**Module detail doc** :https://github.com/LiuYuancheng/WebAttestation/blob/main/PhishpediaReadme.md



For each URL, the program will do below steps:

1. Use webDownloader module to download all the web components.1
2. Use webScreenShoter module to get a webpage screenshot of the url.

3. Pass the web components and the screen shot to PhishperidaPKG to do the siamese checking



###### Program Workflow

If you set the program running under single thread, the program work flow diagram will be shown as below: 

![](doc/img/workflow.png)

version: v_0.2



------

#### Program Setup

###### Development Environment : python 3.7.10

###### Additional Lib/Software Need

- **WebDownloader**:   Refer to program setup section in [***`WebDownloaderReadme.md`***]
- **WebScreenShoter**:  Refer to program setup section in [***`WebScreenShoterReadme.md`***]
- **PhishperidaPKG:** Refer to program setup section in [***`PhishperidaPKGReadme.md`***]

###### Hardware Needed

- **WebDownloader**:   N.A
- **WebScreenShoter**:  [optional] Computer with video output.
- **PhishperidaPKG:** [optional] Computer with Nvidia graph card. 

###### Program File List 

version: v0.1

| Program File           | Execution Env | Description                                                  |
| ---------------------- | ------------- | ------------------------------------------------------------ |
| src/webAttestation.py  | python 3.7.4  | Main web Attestation execution program.                      |
| src/webScreenShoter.py | python 3.7.10 | Web screen shot  module.                                     |
| src/webDownload.py     | python 3.7.10 | Web components download module.                              |
| src/phishpediaPKG.py   | python 3.8.10 | Encapsulated API the NUS-Phishperida project for OPP.        |
| src/webGlobal.py       | python 3.7.4  | Global parameters file which will be used in the other modules. |
| src/ConfigLoader       | python 3.7.4  | Data set loader module.                                      |
| src/urllist.txt        |               | URLs record list (url need to process).                      |
| resultPcdurl.txt       |               | Successful processed URLs list.                              |
| resultErrurl.txt       |               | Failed proessed URLs list.                                   |



------

#### Program Usage

###### Module API Usage

- **WebDownloader**:   Refer to program API usage section in [***`WebDownloaderReadme.md`***]
- **WebScreenShoter**:  Refer to program API usage section in [***`WebScreenShoterReadme.md`***]
- **PhishperidaPKG:** Refer to program API usage section in [***`PhishperidaPKGReadme.md`***]

###### Program Execution 

1. Copy the url you want to check in the url record file "***urllist.txt***"

2. Cd to the program folder and run program execution cmd: 

   ```
   python webAttestation.py
   ```

3. Check the process result in file: `resultPcdurl.txt` and `resultErrurl.txt`

######  MultiThread Design

Use mutli thread with background execution controller , multithread execution, task balancer

![](doc/img/mutliThread.png)



------

#### Reference 

- https://sites.google.com/view/phishpedia-site/home?authuser=0



------

> Last edit by LiuYuancheng(liu_yuan_cheng@hotmail.com) at 03/12/2021
