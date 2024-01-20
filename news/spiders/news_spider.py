import scrapy
from google.cloud import bigquery
from google.api_core.exceptions import NotFound
import json

class NewsSpiderSpider(scrapy.Spider):
    name = "news_spider"
    allowed_domains = ["www.theguardian.com"]
    start_urls = ["https://www.theguardian.com/au"]
    items = []

    def parse(self, response):
        articles = response.css('a.dcr-lv2v9o').getall()
        for article in articles:
            article_html = scrapy.Selector(text=article)
            url = 'https://www.theguardian.com' + article_html.css('::attr(href)').get()
            headline = article_html.css('::attr(aria-label)').get()
            
            yield scrapy.Request(url, callback=self.parse_autor, meta={'url': url, 'headline': headline})

    def parse_autor(self, response):
        url = response.meta['url']
        headline = response.meta['headline']   
        author = response.css('a[rel="author"]::text').get()        
        if not author:
            author = response.xpath('//a[@rel="author"]/span[@itemprop="name"]/text()').get()
            if not author:
                author = response.xpath('//meta[@property="article:author"]/@content').get()
                if not author:
                    author = response.xpath('//div/p[@class="byline"]/text()').get()
                    if not author:
                        author = response.css('div.dcr-1fcd5by::text').get().split('|')[1].strip()
        
        published_on = response.css('span[class="dcr-u0h1qy"]::text').get()
        if not published_on:
            published_on = response.xpath('//time[@itemprop="datePublished"]/text()').get()
            if not published_on:
                published_on = response.xpath('//div[@class="dcr-1vmj0r" ]/text()').get()

        section = response.xpath('//meta[@property="article:section"]/@content').get()        
        if not section:
            section = response.xpath('//a[contains(@href, "commentisfree")]/text()').get() 
        
        text = ' '.join(response.xpath('//*[@id="maincontent"]//text()').getall()).replace('\n', ' ').strip()
        if not text:            
            text = ''.join(response.xpath('//div[@data-component="standfirst"]/p/text()').getall()).replace('\n', ' ').strip()
            
        item = {
        'URL': url,
        'Headline': headline,
        'Section': section.replace('\n', ' ').strip(),
        'Author': author,
        'Published_On': published_on.replace('\n', ' ').strip()[:15],
        'Text': text,
    }

    
        self.items.append(item)

    def closed(self, reason):
        
        if self.items:
            self.to_bigquery(self.items)

    def to_bigquery(self, items):
        client = bigquery.Client()

        dataset_id = 'theguardian'
        table_id = 'news_table'

        dataset_ref = client.dataset(dataset_id)
        table_ref = dataset_ref.table(table_id)

        
        try:
            client.get_dataset(dataset_ref)
        except NotFound:
            client.create_dataset(bigquery.Dataset(dataset_ref))

       
        schema = [
            bigquery.SchemaField("URL", "STRING"),
            bigquery.SchemaField("Headline", "STRING"),
            bigquery.SchemaField("Section", "STRING"),
            bigquery.SchemaField("Author", "STRING"),
            bigquery.SchemaField("Published_On", "STRING"),
            bigquery.SchemaField("Text", "STRING"),
        ]

        table = bigquery.Table(table_ref, schema=schema)

       
        try:
            client.get_table(table_ref)
        except NotFound:
            client.create_table(table)

        
        rows_to_insert = [
            (
                item['URL'],
                item['Headline'],
                item['Section'],
                item['Author'],
                item['Published_On'],
                item['Text'],
            )
            for item in items
        ]
        errors = client.insert_rows(table, rows_to_insert)

        if errors:
            print(f"Inserting rows into BigQuery error: {errors}")
        else:
            print("Data inserted into BigQuery successfully!")
