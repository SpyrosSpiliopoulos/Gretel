import time
from pyvis.network import Network
from bs4 import BeautifulSoup
import requests
import os
import re
import subprocess
from chrome_connector import PyChromeConnector
from cookie_visualizer import visualize_tohtml_audit



if __name__=="__main__":

    print("welcome to cookie tracker")

    p=subprocess.Popen(["chrome","--remote-debugging-port=9222","--incognito","--user-data-dir=remote-profile"])
    chrome_session = PyChromeConnector(port=9222)

    graphmap_inter={"source":[],"target":[],"weight":[],"profile_type":[],"domain":[]}
    url=input("Enter url : ")
    chrome_session.go_page(url)

    try:
        while True:

                answer = None
                while answer not in ("yes", "no"):

                    answer = input("Do you want to fetch cookies? (yes or no): ")
                    if answer == "yes":
                        profile_type=input("What is the cookie profile? (provide description i.e. necessary, optional...):" )
                        cookies=chrome_session.get_cookies()
                        for cookie in cookies:
                            domain=url.lower().split("www")[-1]
                            graphmap_inter["source"].append(domain)
                            graphmap_inter["target"].append(cookie["domain"])
                            graphmap_inter["weight"].append(1)
                            graphmap_inter["source"].append(cookie["domain"])
                            graphmap_inter["target"].append(cookie['name'])
                            graphmap_inter["weight"].append(0.3)
                            graphmap_inter["profile_type"].append(profile_type)
                            graphmap_inter["domain"].append(domain)
                        chrome_session.clear_cookies()
                        chrome_session.go_page(url)
                    elif answer == "no":
                         continue
                    else:
                    	print("Please enter yes or no.")
    except KeyboardInterrupt:
        print('interrupted!')
    except Exception as e:
        print(e)

    visualize_tohtml_audit(graphmap_inter)
    p.kill()
