## adapted FROM https://towardsdatascience.com/collecting-data-from-the-new-york-times-over-any-period-of-time-3e365504004

import os,json,time,requests,datetime
import dateutil
import pandas as pd
from dateutil.relativedelta import relativedelta
from requests.api import get
import csv

from helper import get_data

import logging

# logging.basicConfig(filename="helpers.log", encoding = "utf-8", level = logging.DEBUG, filemode='w') # ! Remove filemode W later
logging.basicConfig(format='%(asctime)s %(message)s')

with open('nyt.api.txt') as f:
    for line in f:
        APIKEY = line
        break
    logging.info("API key loaded in main")

def add_to_csv(data):
    logging.info("Writing to CSV")
    to_write = [data['snippet'], data['lead_paragraph']] # make the lead pargraph RAW
    with open("data.csv","a") as csvfile:
        writer = csv.writer(csvfile, delimiter=',',
                        quotechar='|', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(to_write)

def main():
    logging.info("Starting program")
    article_data = get_data(url)
    # logging.DEBUG(article_data)
    for data in article_data:
        if data:
            add_to_csv(data)

if __name__ == '__main__':

    url = f"https://api.nytimes.com/svc/news/v3/content/nyt/world.json?api-key={APIKEY}"
    main()
    # r = send_request(url)
    # print(r['results'][0])
    # print(get_data(url))
    # ! FIX THE TEXT

    # article_url = "https://www.nytimes.com/2021/12/03/world/middleeast/israel-shira-isakov-domestic-violence.html"
    # download_article(article_url)

    # narrow down by subsection = 'Middle East', geo_facet = ['Israel', 'Palestine']
    # then download the article using the URL
    # then sleep

    # returns of the file
        #   slug_name
        #   section
        #   *subsection
        #   *title
        #   *abstract
        #   *url (this is the article)
        #   *byline
        #   item_type (we want this to be article)
        #   source
        #   *updated_date
        #   *published_date
        #   *des_facet (descriptions?)
        #   *geo_facet (considered area)
