import scrapy

class ItchioSpider(scrapy.Spider):
    name = 'itchio_spider'
    page = 1
    start_urls = ['https://itch.io/games?page=' + str(page)]
    def parse(self, response):
        
        for i in response.css('div.game_cell'):
            title = i.css('.game_title a::text').get()
            author = i.css('.game_author a::text').get()
            genre = i.css('.game_genre::text').get()
            platform = i.css('.game_platform > span::attr(title)').getall()
            price = i.css('.price_value::text').get()
            if price is None:
                price = 'free'
            sale = i.css('.sale_tag::text').get()
            href = i.css('.game_title a::attr(href)').get()

            for a in range(len(platform)):
                platform[a] = platform[a].replace("Download for ", "")

            yield{
                'title': title,
                'author': author, 
                'genre': genre,
                'platform': platform,
                'price' : price,
                'sale' : sale,
                'href': href
            }

        self.page += 1
        if self.page < 20:
            next_page = 'https://itch.io/games?page=' + str(self.page)
            yield response.follow(next_page, self.parse)