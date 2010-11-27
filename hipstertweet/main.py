#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import logging
import tweepy
import os

from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from django.utils import simplejson as json
from google.appengine.api import urlfetch
from google.appengine.ext import db
from bitly import BitLy




TWITTER_CALLBACK = 'http://localhost:8080/callback'

#TWITTER_CALLBACK = 'http://toohipster.appspot.com/callback'

TWITTER_CONSUMER_KEY ='IFbmxlrnvIuKOtXiMEyEQ'
TWITTER_CONSUMER_SECRET ='Xhe2NOEWWY0ZWxzb8K5x5NUg22gyuwN4sgvCg9o0XY'

TWITTER_ACCESS_TOKEN='220091954-A1N3me3vSpiAavMVE73h6PevkDqPWOtyDlnKLjXN'
TWITTER_ACCESS_TOKEN_SECRET='mDa8HBjD38J6xUbe61aSaGC62ej0OLAK8Vn0Tc2HQP8'

BITLY_API_KEY = 'R_1ff412d8c04003ecdc217f821cd76183'
BITLY_LOGIN = 'robee'

class Song(db.Model):
    song_artist = db.StringProperty(required=True)
    rank = db.IntegerProperty(required=True)
    url = db.StringProperty(required=True)


class MainHandler(webapp.RequestHandler):
    def get(self):
        
        results = urlfetch.fetch(url='http://query.yahooapis.com/v1/public/yql?q=SELECT%20alt%2C%20src%20FROM%20html%20WHERE%0Aurl%3D%22http%3A%2F%2Fwww.bbc.co.uk%2Fradio1%2Fchart%2Fsingles%2F%22%20AND%20xpath%3D%22%2F%2Fli%2Fimg%22%20LIMIT%20100&format=json&diagnostics=true&callback=cbfunc',
                        payload='', 
                        method=urlfetch.GET,
                        headers={})
        
        
        results = results.content
        results = results.replace('cbfunc(', '').replace(');', '')
        
        results = json.loads(results)['query']['results']['img']
        
        
        current_songs = Song.all()
        count = 0
        for result in results:
            count = count+1
            song = Song( song_artist = result['alt'], rank = count, url = result['src'])
            logging.info(result['src'])
            if is_song_in_db(song.song_artist) == 0:
                message = buildMessage(song)
                tweet(message)
                song.put()
        
        #tweet('TestTweet')
        
        self.response.out.write('You arent supposed to be here')


class CallbackHandler(webapp.RequestHandler):
    def get(self):
        
        self.response.out.write('callback')


def is_song_in_db(song_artist):
    
    songs = Song.all().fetch(100)
    
    for song in songs:
        if song_artist == song.song_artist:
            return 1
        
    return 0

def buildMessage(song):
    
    #result[]
    #bitly = BitLy(BITLY_LOGIN, BITLY_API_KEY)
    #urlData = bitly.shorten(song.url)
    #shortURL = urlData['data']['url']
    message = song.song_artist + ' - is too mainstream to be "Hipster"' 
    return message
    
def tweet(msg):
    
    auth = tweepy.OAuthHandler(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET)
    auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)

    api = tweepy.API(auth_handler=auth, secure=True, retry_count=5)
    
    api.update_status(msg)  # post the tweet
   
        
    

def main():
    application = webapp.WSGIApplication([('/', MainHandler), ('/callback', CallbackHandler)],
                                         debug=True)
    util.run_wsgi_app(application)


#{u'status_code': 200, u'data': {u'url': u'http://bit.ly/gahzrM', u'hash': u'gahzrM', u'global_hash': u'fmwBAN', u'long_url': u'http://robotandgunshot.com', u'new_hash': 0}, u'status_txt': u'OK'}


    pass
if __name__ == '__main__':
    main()
