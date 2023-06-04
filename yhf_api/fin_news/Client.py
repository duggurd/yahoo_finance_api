"""Yahoo Finance News article stream API client"""

from typing import Optional
import requests
from requests.sessions import Session

from .Payload import Payload

class Client:
    """Client class for finnews API"""
    ROOT_URL = "https://finance.yahoo.com/_finance_doubledown/api/resource"
    def __init__(self, session:Optional[Session]=None, user_agent:Optional[str]=None):
        if session is None:
            self._session = Session()
        else:
            self._session = session
        
        self.headers = {}
        self.headers["user-agent"] = user_agent if user_agent is not None else "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"
    
    def __call__(self, payload:Payload) -> requests.Response:
        return self._session.post(url=self.ROOT_URL, json=payload, headers=self.headers)