import os
import csv

def twitter_scraper(word):
    res = []
    os.system('GetOldTweets3 --querysearch' +' "' + word + '"' + ' --maxtweets 10')
    with open('output_got.csv', 'r') as f:
        res = []
        reader = csv.reader(f)
        for i in reader:
            res.append(i[-2] + ': ' + i[6])
    return res[1:]

