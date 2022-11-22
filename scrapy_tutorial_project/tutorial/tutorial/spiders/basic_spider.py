import scrapy

class BasicSpider(scrapy.Spider):
    name = 'basic'
    
    start_urls = ['https://quotes.toscrape.com']

    def parse(self, response):
        for quote in response.css('div.quote'):
            author = quote.css('.author::text').get()
            text = quote.css('.text::text').get()
            tags = quote.css('.tag::text').getall()

            yield {
                'author' : author,
                'quote_text' : text,
                'tags' : tags
                }
        next_page = response.css('.next a::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)