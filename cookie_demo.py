import PyChromeDevTools
import time
import pandas as pd
from bs4 import BeautifulSoup
import requests
import os
import re
from cookie_visualizer import visualize_tohtml_globalmap
from chrome_connector import PyChromeConnector
import subprocess


def get_demo_cookies(chrome):
    try:
        with open("c:/workspace/msc/cookie_visualizer/websites.txt","r") as f:
            websites=eval(f.read())
    except:
        websites=[]
        #get alexa websites
        page = requests.get("https://www.alexa.com/topsites/countries/GR")
        soup = BeautifulSoup(page.content, 'html.parser')
        mydivs = soup.findAll("div", {"class": "td DescriptionCell"})
        for div in mydivs:
            websites.extend(div.a.contents)
        #get quantcast websites
        for pagenum in range(1,60):
            print(pagenum)
            page = requests.get("https://www.quantcast.com/top-sites/GR/%s"%(pagenum))
            soup = BeautifulSoup(page.content, 'html.parser')
            rows = soup.findAll('td', {'class': "link"})
            for row in rows:
                try:
                    websites.append(row.img["name"])
                except:
                    pass
        with open("c:/workspace/msc/Gretel/websites.txt","w+") as f:
            f.write(str(websites))


    greekwebsites=list(filter(lambda x: re.match(".+\.gr",x), websites))

    try:
        graphmap_inter=pd.read_pickle("c:/workspace/msc/Gretel/graphmap_cookies.pkl")
    except:
        graphmap = pd.DataFrame({"source":[],"target":[],"weight":[]})
        for i,website in enumerate(greekwebsites):
            print("now fetching cookies from: ",website)
            chrome.go_page(website)
            cookies=chrome.get_cookies()
            for cookie in cookies:
                domain_only=cookie["domain"].split("www")[-1]
                if re.match("^\..+",domain_only):
                    domain_only=domain_only[1:]
                graphmap.loc[len(graphmap)]=[website.lower(),domain_only,1]
            print("completed item no. ",i+1,"out of ",len(greekwebsites))

        graphmap_inter=graphmap.loc[graphmap["target"]!=graphmap["source"]]
        graphmap_inter["color"]="white"
        graphmap_inter["color"]=graphmap_inter["color"].where(graphmap_inter["source"]==graphmap_inter["target"],other="red")

        graphmap_inter.to_pickle("c:/workspace/msc/Gretel/graphmap_cookies.pkl")

    return graphmap_inter


if __name__=="__main__":
        #subprocess.Popen(["chrome", "--remote-debuggin-port=9242","--headless","www.google.com"])
        subprocess.Popen(["chrome","--remote-debugging-port=9222","--user-data-dir=remote-profile"])
        chrome = PyChromeConnector(host="localhost",port="9222")

        graphmap_inter=get_demo_cookies(chrome)
        visualize_tohtml_globalmap(graphmap_inter)
