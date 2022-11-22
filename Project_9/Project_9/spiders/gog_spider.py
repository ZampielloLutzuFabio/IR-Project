import scrapy

class GogSpider(scrapy.Spider):
    name = 'gog_spider'
    start_urls = ['https://www.gog.com/en/games?tags=indie']
    page = 1

    def parse(self, response):

        for i in response.css('div.product-tile__info'):
            title = i.css('.product-tile__title::attr(title)').get()
            # author = i.css('.game_author a::text').get()
            # genre = i.css('.game_genre::text').get()
            # platform = i.css('.game_platform::text').get()
            # href = i.css('.game_title a::attr(href)').get()

            yield{
                'title': title,
                # 'author': author, 
                # 'genre': genre,
                # 'platform': platform,
                # 'href': href
            }


        if self.page < 20:
            self.page += 1
            yield response.follow('https://www.gog.com/en/games?tags=indie&page=' + str(self.page), self.parse)    