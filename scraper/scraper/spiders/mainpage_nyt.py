import scrapy
from bs4 import BeautifulSoup

class MainpageNytSpider(scrapy.Spider):
    name = 'mainpage-nyt'
    # allowed_domains = ['https://www.nytimes.com/']
    start_urls = ['https://www.nytimes.com/2022/01/07/realestate/pandemic-move-friends.html']

    parsed = []

    def parse(self, response):

        
        article_body = response.css('.css-1r7ky0e').extract()
        # article_soup = BeautifulSoup(article_body, 'html5lib')
        
        headline = response.css('.css-hzs6w4').extract()
        # headline_soup = BeautifulSoup(headline,'html5lib')
        
        summary = response.css('.css-w6ymp8')
        # summary_soup = BeautifulSoup(summary,'html5lib')

        return (article_body, headline, summary)
        # print(article_soup.text)

        # for item in zip(article_body,headline,summary):
        #     items = ({
        #         'article_body':article_soup.text,
        #         'headline':headline_soup.text,
        #         'summary':summary_soup.text})
        #     yield items

        # ! there is no need for something as advanced as scrapy