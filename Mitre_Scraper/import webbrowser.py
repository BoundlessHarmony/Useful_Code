import requests, bs4

exampleFile = open('C:\\Users\\Boundless\\PycharmProjects\\mitre_scraper\\view-source_https___attack.mitre.org_groups_G0046_.html')
exampleSoup = bs4.BeautifulSoup(exampleFile, 'html.parser')
type(exampleSoup)