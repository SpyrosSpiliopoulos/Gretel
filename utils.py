import PyChromeDevTools
import time


def go_get_cookies(chrome,url):
    chrome.Page.navigate(url="http://"+url)
    event,messages=chrome.wait_event("Page.frameStoppedLoading", timeout=60)
    time.sleep(3)
    #Wait last objects to load
    cookies=chrome.Network.getCookies()
    return cookies["result"]["cookies"]
