from google.appengine.api import urlfetch
from django.utils import simplejson 
import logging
class BitLy():
    def __init__(self, login, apikey):
        self.login = login
        self.apikey = apikey

    def shorten(self,param):
        url = param
        request = "http://api.bit.ly/v3/shorten?longUrl="
        request += url
        request += "&login=" + self.login + "&apiKey=" +self.apikey
        result = urlfetch.fetch(request)
        json = simplejson.loads(result.content)
        return json