import scrapy

class SteamSpider(scrapy.Spider):
    name = 'steam_spider'
    page = 1
    start_urls = ['https://store.steampowered.com/search/?tags=492?&page=' + str(page)]
    def parse(self, response):
        
        for i in response.css('.search_result_row'):
            title = i.css('.title::text').get()
            # author = i.css('.game_author a::text').get()
            # genre = i.css('.game_genre::text').get()
            platform = i.css('.platform_img::attr(class)').getall()
            # price = i.css('.price_value::text').get()
            # sale = i.css('.sale_tag::text').get()
            # href = i.css('.game_title a::attr(href)').get()

            for a in range(len(platform)):
                platform[a] = platform[a].replace("platform_img ", "").replace("win", "Windows").replace("mac", "macOS").replace("linux", "Linux")

            yield{
                'title': title,
                # 'author': author, 
                # 'genre': genre,
                'platform': platform,
                # 'price' : price,
                # 'sale' : sale,
                # 'href': href
            }
            
        self.page += 1
        if self.page < 10:
            yield response.follow('https://store.steampowered.com/search/?tags=492?&page=' + str(self.page), self.parse)    