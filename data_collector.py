## adapted FROM https://towardsdatascience.com/collecting-data-from-the-new-york-times-over-any-period-of-time-3e365504004

import os,json,time,requests,datetime
import dateutil
import pandas as pd
from dateutil.relativedelta import relativedelta
from requests.api import get
import csv

with open('nyt.api.txt') as f:
    for line in f:
        APIKEY = line
        break

def send_request(url):
    '''Sends a request to the NYT Archive API for given date.'''
    response = requests.get(url).json()
    time.sleep(6)
    return response


def is_valid(subsection, geo_facet):
    '''An article is only worth checking if it is in range, and has a headline.'''
    if subsection == "Middle East":
        # return True if 'palestine' in geo_facet or 'israel' in geo_facet else False
        return True
    return False


def parse_response(article_json):
    '''Parses and returns response as pandas data frame.'''
    data = {
        'title': article_json['title'] if article_json['title'] else 'EMPTY',
        'abstract' : article_json['abstract'],
        'subsection': article_json['subsection'],
        'author' : article_json['byline'],
        'publish_date': article_json['published_date'],
        'updated_date': article_json['updated_date'],
        'locations': article_json['geo_facet'],
        'descriptions': article_json['des_facet'],
        'url':article_json['url']
    }
    return data


def get_data(url):
    responses = send_request(url)['results']
    valid_articles = []
    for article in responses:
        if is_valid(article['subsection'],article['geo_facet']):
            valid_articles.append(parse_response(article))
    article_data = []
    for article_json in valid_articles:
       article_data.append(download_article(article_json['url']))
    
    return article_data

def grab_search_term(article_url):
    return article_url.split('/')[-1].split('-')[0]

def download_article(article_url):
    search_term = grab_search_term(article_url)
    fq = 'web_url:("'+str(article_url)+'")'
    url = f"https://api.nytimes.com/svc/search/v2/articlesearch.json?q='{search_term}'&fq={fq}&api-key={APIKEY}"
    # print(url)
    response = send_request(url)['response']["docs"][0]
    snippet = response["snippet"]
    lead_paragraph = response["lead_paragraph"]
    # print(snippet, lead_paragraph)
    return {"snippet": snippet, "lead_paragraph":lead_paragraph}

def add_to_csv(data):
    to_write = [data['snippet'], data['lead_paragraph']] # make the lead pargraph RAW
    with open("data.csv","a") as csvfile:
        writer = csv.writer(csvfile, delimiter=',',
                        quotechar='|', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(to_write)

def main():
    article_data = get_data(url)
    for data in article_data:
        # print(data)
        add_to_csv(data)
if __name__ == '__main__':

    url = f"https://api.nytimes.com/svc/news/v3/content/nyt/world.json?api-key={APIKEY}"
    main()
    # r = send_request(url)
    # print(r['results'][0])
    # print(get_data(url))
    

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
