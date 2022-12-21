# -*- coding: utf-8 -*-
"""
Created on Fri Dec 16 17:04:05 2022

@author: Boundless
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Dec 21 09:18:57 2022

@author: brady.r.wainio
"""

import csv
import requests
from html.parser import HTMLParser
from lxml.html import parse


# ------------------------testing------------------------#
all_cwes = []


# ----------------------- testing ----------------------#
def get_cwe_list(url):
    raw_html = []
    class MyHTMLParser(HTMLParser):
        def handle_data(self, data):
            raw_html.append(data)

    
    cwes = []
    req = requests.get(url)
    req_text = req.text
    print(req_text)
    
    parser = MyHTMLParser()
    feed = parser.feed(req_text)
    print(feed)
                
    for item in raw_html:
        if item[0:4] == "CWE-":
            x = ''
            for letter in item:
                if letter.isdigit() == True:
                    x = x + letter
            cwes.append(int(x))
    cwes_unique = sorted(list(set(cwes)))
    raw_html = []
    return cwes_unique


        
    

# Unedited url below, sorting generates the base url
# "https://www.cvedetails.com/vulnerability-list/cweid-X/vulnerabilities.html"
# page num on base url replaced with 'X', cweid replaced with'Y', sorted by date version
base_url = "https://www.cvedetails.com/vulnerability-list.php?vendor_id=0&product_id=0&version_id=0&page=X&hasexp=0&opdos=0&opec=0&opov=0&opcsrf=0&opgpriv=0&opsqli=0&opxss=0&opdirt=0&opmemc=0&ophttprs=0&opbyp=0&opfileinc=0&opginf=0&cvssscoremin=0&cvssscoremax=0&year=0&month=0&cweid=Y&order=1&trc=4779&sha=3027a88c1cb77e186062e297bad7e6637bcf0b66"

# generate cweid list
    # owasp top 10 urls
owasp_urls = [
    "https://owasp.org/Top10/A01_2021-Broken_Access_Control/",
    "https://owasp.org/Top10/A02_2021-Cryptographic_Failures/",
    "https://owasp.org/Top10/A03_2021-Injection/",
    "https://owasp.org/Top10/A04_2021-Insecure_Design/",
    "https://owasp.org/Top10/A05_2021-Security_Misconfiguration/"
    "https://owasp.org/Top10/A06_2021-Vulnerable_and_Outdated_Components/",
    "https://owasp.org/Top10/A07_2021-Identification_and_Authentication_Failures/",
    "https://owasp.org/Top10/A08_2021-Software_and_Data_Integrity_Failures/",
    "https://owasp.org/Top10/A09_2021-Security_Logging_and_Monitoring_Failures/",
    "https://owasp.org/Top10/A10_2021-Server-Side_Request_Forgery_%28SSRF%29/"]


for url in owasp_urls:
    cwe_list = get_cwe_list(url)
    all_cwes.append(cwe_list)
    
# get_cwe_list("https://owasp.org/Top10/A01_2021-Broken_Access_Control/")

            # download each page
                # Count cweid
                # snag cweids from the url subelements within each page
                    # append to [cweids]
                    # check if len([cweids]) matches cweid count
                    # write line to cweids csv file

# generate url --- url.replace('X', cweid)
    # apppend to [cweid_urls]
        # for each cweid url
            # wget (or equiv) page 1
            # check if cve list empty or not
            # if not empty, extract minimum and maximum page numbers
                # append cweid, min_pn, max_pn to list of lists [[cweid_pns]]
            # if empty, append cweid to [empty_cweids]
                #pop cweid from [cweid_urls]
# generate directory for each cweid in [cweid_pns][0][:] (excludes empty cweids (no cves))

# for each url in [cweid_urls]
    # for pn in range(cweid_pns[1][:] (max_pn), cweid_pns[2][:] (min_pn)):
        # url = cweid_url.replace('Y', 'pn') 
        # [urls].append(url)

# write each url to url_file.csv

#ingest url_file.csv
    #for url in url_file.csv
        # wget
        # wait 1.5 sec
        # save page as cweid_pn_max_pn in matching cweid dir
      
# for every cweid dir, ingest * files
    # append cve to [cves]
    # count cves
    # sort by condition on each row
    # constrain count by min 15, max 30
    # alter conditions variable based on count
    # if r < 15, decrement year. If r > 30 increment severity
    # check r
        # condition: year >= 2021 & severity >=7 
            # write line new csv file with cweid, cve number, severity, description
            # inside the corresponding cwe dir
print("done")