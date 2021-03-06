import time
from pyvis.network import Network
import requests
import os
import re
import subprocess
from chrome_connector import PyChromeConnector
from cookie_visualizer import visualize_tohtml_audit
import pdb,traceback,sys



def ask_url_and_get_alias():
    url=input("Enter url : ")
    alias_question=None
    while alias_question not in ("yes", "no"):
        alias_question=input("do you want to alias the domain name? (yes or no): ")
    alias=None
    if alias_question=="yes":
        alias=input("provide an alias to the domain name: ")
    return url,alias

def get_domain(url):
    return url.lower().split("www")[-1].split("/")[0]

if __name__=="__main__":

    print("welcome to cookie tracker")

    p=subprocess.Popen(["chrome","--remote-debugging-port=9222","--incognito","--user-data-dir=remote-profile"])
    chrome_session = PyChromeConnector(port=9222)

    graphmap_inter={"source":[],"target":[],"weight":[],"profile_type":[],"domain":[],"value":[]}

    url,alias=ask_url_and_get_alias()


    try:
        chrome_session.go_page(url)
    except:
        chrome_session.go_page(url,"http://")

    try:
        while True:

                answer = None
                while answer not in ("yes", "no"):

                    answer = input("Do you want to fetch cookies? (yes or no): ")
                    if answer == "yes":
                        profile_type=input("What is the cookie profile? (provide description i.e. necessary, optional...): " )
                        cookies=chrome_session.get_cookies()
                        for cookie in cookies:
                            if not alias:
                                domain=get_domain(url)
                            else:
                                domain=alias
                            graphmap_inter["source"].append(domain)
                            graphmap_inter["target"].append(cookie["name"])
                            graphmap_inter["weight"].append(.01)
                            graphmap_inter["profile_type"].append(profile_type)
                            graphmap_inter["domain"].append(domain)
                            graphmap_inter["value"].append(None)

                            graphmap_inter["source"].append(cookie['name'])
                            graphmap_inter["target"].append(get_domain(cookie["domain"]))
                            graphmap_inter["weight"].append(.01)
                            graphmap_inter["profile_type"].append(profile_type)
                            graphmap_inter["domain"].append(domain)
                            graphmap_inter["value"].append(cookie["value"])

                        chrome_session.clear_cookies()
                        try:
                            chrome_session.go_page(url)
                        except:
                            chrome_session.go_page(url,"http://")
                    elif answer == "no":
                        doanother=None
                        while doanother not in ("yes", "no"):
                            doanother = input("Do you want to add another website? (yes or no): ")
                        if doanother=="yes":
                            try:
                                url,alias=ask_url_and_get_alias()
                                chrome_session.go_page(url)
                            except:
                                chrome_session.go_page(url,"http://")
                        else:
                            print("now visualizing the results. Please wait...")
                            try:
                                visualize_tohtml_audit(graphmap_inter)
                            except:
                                extype, value, tb = sys.exc_info()
                                traceback.print_exc()
                                pdb.post_mortem(tb)
                            sys.exit()
                    else:
                    	print("Please enter yes or no.")
    except KeyboardInterrupt:
        print('interrupted!')
    except Exception as e:
        print(e)

    p.kill()
