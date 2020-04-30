#!/usr/bin/env python

#-----------------------------------------------------------------------
# twitter-trends
#  - lists the current global trending topics
#-----------------------------------------------------------------------

from twitter import *

#-----------------------------------------------------------------------
# load our API credentials
#-----------------------------------------------------------------------
import sys
sys.path.append(".")
import config

#-----------------------------------------------------------------------
# create twitter API object
#-----------------------------------------------------------------------
twitter = Twitter(auth = OAuth(config.access_key,
                  config.access_secret,
                  config.consumer_key,
                  config.consumer_secret))
'''
consumer_key = 'b5Im5nYm2LBOwpWfE00alCoB4'
consumer_secret = 'PrA5l1eBoq7WSz5CxYU6PrivNB4ypZTOTyKZQtNx5ZBP1owVAB'
access_key = "252316931778109445-z6QbBu2baVIyqayEjBjfh8JcbnvV4A"
access_secret = "Zp7xIWg7SkSPNueWW4JPD3diXUfcfYtRFAwy3N52nZexw"
twitter = TwitterAPI(
                  consumer_key,
                  consumer_secret,access_key,access_secret)
                  '''
#-----------------------------------------------------------------------
# retrieve global trends.
# other localised trends can be specified by looking up WOE IDs:
#   http://developer.yahoo.com/geo/geoplanet/
# twitter API docs: https://dev.twitter.com/rest/reference/get/trends/place
#-----------------------------------------------------------------------
def getHot():
    results = twitter.trends.place(_id = 2459115)
    s={}
    for location in results:
        for trend in location["trends"] :
            if   trend["tweet_volume"] !=None:
                s["%s" % trend["name"]]=trend["tweet_volume"]
    s1=sorted(s.items(),key = lambda x:int(x[1]),reverse = True)
    ans = []
    for i in s1:
        ans.append(i[0])
    return ans[0:10]
