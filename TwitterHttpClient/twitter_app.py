import socket
import sys
import requests
import requests_oauthlib
import json
from signal import signal, SIGPIPE, SIG_DFL, SIG_IGN
# Replace the values below with yours

consumer_key = 'b5Im5nYm2LBOwpWfE00alCoB4'
consumer_secret = 'PrA5l1eBoq7WSz5CxYU6PrivNB4ypZTOTyKZQtNx5ZBP1owVAB'
access_key = "1252316931778109445-js4jRCfo4JAopjJqseqosz6amNx85V"
access_secret = "pQLoi2mlfAuQCumOSnpMslqsylID6u0ZAeLei0aaxgVvK"
my_auth = requests_oauthlib.OAuth1(consumer_key, consumer_secret,access_key, access_secret)


def send_tweets_to_spark(http_resp, tcp_connection):
    for line in http_resp.iter_lines():
        try:
            full_tweet = json.loads(line.decode("utf-8"))
            # print(full_tweet)
            tweet_text = full_tweet['text'] + '\n' # pyspark can't accept stream, add '\n'
            print("Tweet Text: " + tweet_text)
            print ("------------------------------------------")
            tcp_connection.send(tweet_text.encode())
        except:
            e = sys.exc_info()[0]
            print("Error: %s" % e)


def get_tweets():
    url = 'https://stream.twitter.com/1.1/statuses/filter.json'
    #query_data = [('language', 'en'), ('locations', '-130,-20,100,50'),('track','#')]
    query_data = [('locations', '-122.75,36.8,-121.75,37.8,-74,40,-73,41'),('language','en')] #this location value is San Francisco & NYC
    query_url = url + '?' + '&'.join([str(t[0]) + '=' + str(t[1]) for t in query_data])
    # print(query_url)
    response = requests.get(query_url, auth=my_auth, stream=True)
    print(url, response)
    return response


TCP_IP = "localhost"
TCP_PORT = 9009
conn = None
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)
print("Waiting for TCP connection...")
conn, addr = s.accept()
print("Connected... Starting getting tweets.")
resp = get_tweets()
send_tweets_to_spark(resp,conn)



