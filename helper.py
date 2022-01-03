import logging, requests, time

logging.basicConfig(filename="helpers.log", encoding = "utf-8", level = logging.DEBUG, filemode='w')
logging.basicConfig(format='%(asctime)s %(message)s')

with open('nyt.api.txt') as f:
    for line in f:
        APIKEY = line
        break
    logging.info("API key loaded in helper")

def send_request(url):
    '''Sends a request to the NYT Archive API for given date.'''
    sleep_time = 6

    logging.info(f"Getting Request from {url}")
    response = requests.get(url).json()
    
    logging.info(f"sleeping for {sleep_time}")
    time.sleep(sleep_time)
    
    return response


def is_valid(subsection, geo_facet):
    '''An article is only worth checking if it is in range, and has a headline.'''
    if subsection == "Middle East":
        # return True if 'palestine' in geo_facet or 'israel' in geo_facet else False
        return True
    return True


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

def download_article(article_url):
    search_term = grab_search_term(article_url)
    # fq = 'web_url:("'+str(article_url)+'")' # ! look through documentation again
    # url = f"https://api.nytimes.com/svc/search/v2/articlesearch.json?q='{search_term}'&fq={fq}&api-key={APIKEY}"
    fq = 'web_url:("'+str(article_url)+'")'
    url = f"https://api.nytimes.com/svc/search/v2/articlesearch.json?fq={fq}&api-key={APIKEY}"

    # print(url)
    
    response = send_request(url)['response']["docs"]
    # response = send_request(url)
    if response:
        logging.debug(response[0])
        response = response[0]
        snippet = response["snippet"]
        lead_paragraph = response["lead_paragraph"]
        # print(snippet, lead_paragraph)
        return {"snippet": snippet, "lead_paragraph":lead_paragraph}
    else:
        return None

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