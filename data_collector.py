## adapted FROM https://towardsdatascience.com/collecting-data-from-the-new-york-times-over-any-period-of-time-3e365504004

import os,json,time,requests,datetime
import dateutil
import pandas as pd
from dateutil.relativedelta import relativedelta

with open('nyt.api.txt') as f:
    for line in f:
        APIKEY = line
        break

def send_request(url):
    '''Sends a request to the NYT Archive API for given date.'''
    response = requests.get(url).json()
    time.sleep(6)
    return response


def is_valid(article, date):
    '''An article is only worth checking if it is in range, and has a headline.'''
    #update this to check for Palestine
    pass


def parse_response(response):
    '''Parses and returns response as pandas data frame.'''
    data = {'headline': [],  
        'date': [], 
        'doc_type': [],
        'material_type': [],
        'section': [],
        'keywords': []}
    
    articles = response['response']['docs'] 
    for article in articles: # For each article, make sure it falls within our date range
        date = dateutil.parser.parse(article['pub_date']).date()
        if is_valid(article, date):
            data['date'].append(date)
            data['headline'].append(article['headline']['main']) 
            if 'section' in article:
                data['section'].append(article['section_name'])
            else:
                data['section'].append(None)
            data['doc_type'].append(article['document_type'])
            if 'type_of_material' in article: 
                data['material_type'].append(article['type_of_material'])
            else:
                data['material_type'].append(None)
            keywords = [keyword['value'] for keyword in article['keywords'] if keyword['name'] == 'subject']
            data['keywords'].append(keywords)
    return pd.DataFrame(data) 


def get_data(dates):
    '''Sends and parses request/response to/from NYT Archive API for given dates.'''
    total = 0
    print('Date range: ' + str(dates[0]) + ' to ' + str(dates[-1]))
    if not os.path.exists('headlines'):
        os.mkdir('headlines')
    for date in dates:
        response = send_request(date)
        df = parse_response(response)
        total += len(df)
        df.to_csv('headlines/' + date[0] + '-' + date[1] + '.csv', index=False)
        print('Saving headlines/' + date[0] + '-' + date[1] + '.csv...')
    print('Number of articles collected: ' + str(total))


if __name__ == '__main__':
    
    url = f"https://api.nytimes.com/svc/news/v3/content/nyt/world.json?api-key={APIKEY}"
    r = send_request(url)
    print(r['results'][0])
    # narrow down by subsection = 'Middle East', geo_facet = ['Israel', 'Palestine']
    # then download the article using the URL
    # then sleep
