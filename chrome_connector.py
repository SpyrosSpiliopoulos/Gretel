from PyChromeDevTools import ChromeInterface
import time
from exceptions import *
import re


class PyChromeConnector(ChromeInterface):

    def __init__(self,*args,**kwargs):
        super(PyChromeConnector, self).__init__(*args,**kwargs)
        self.Network.enable()
        self.Page.enable()

    def go_page(self,url,scheme="https://"):
        start_time=time.time()
        response=self.Page.navigate(url=scheme+url)
        self.wait_event("Page.loadEventFired", timeout=60)
        end_time=time.time()
        print ("Page Loading Time:", end_time-start_time)
        if response:
            result= response.get('result')
            errmsg=result.get('errorText')
            if not errmsg:
                event,messages=self.wait_event("Page.frameStoppedLoading", timeout=120)
                if event:
                    time.sleep(3)
            else:
                raise ConException(action="navigating to"+url,errmsg=errmsg)

    def get_cookies(self):
        #Wait last objects to load
        response=self.Network.getCookies()
        result= response['result']
        errmsg=result.get('errorText')
        if not errmsg:
            cookies=result.get('cookies')
            for cookie in cookies:
                cookie["domain"]=cookie["domain"].split("www")[-1]
            return cookies
        else:
            raise ConException(action="fetching cookies",errmsg=errmsg)

    def clear_cookies(self):
        response=self.Network.clearBrowserCookies()
        result= response['result']
        errmsg=result.get('errorText')
        if not errmsg:
            pass
        else:
            raise ConException(action="clearing cookies",errmsg=errmsg)


if __name__=="__main__":
    chrome_session = PyChromeConnector(port=9242)
    chrome_session.go_page("www.google.com")
    cookies=chrome_session.get_cookies()
    if cookies:
        print(cookies)
