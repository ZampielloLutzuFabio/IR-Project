import scrapy

class SteamSpider(scrapy.Spider):
    def parse_inside(self, response):
        item = response.meta['item']

        if item['sale'] is not None:
            item['price'] = response.css('.discount_final_price::text').get().strip()
        else:
            item['price'] = response.css('.game_purchase_price.price::text').get().strip()

        if item['price'] is None:
            item['price'] = 'free'

        item['author'] = response.css('.dev_row a::text').get()
        item['genre'] = response.css(".popular_tags a::text").getall()
        for i in range(len(item['genre'])):
            item['genre'][i] = item['genre'][i].strip()

        item['genre'].remove("Indie")
        return item
    
    name = 'steam_spider'
    page = 1
    start_urls = ['https://store.steampowered.com/search/?tags=492?&page=' + str(page)]
    def parse(self, response):
        
        for i in response.css('.search_result_row'):
            if i.css('::attr(bundleid)').get() is not None:
                continue

            title = i.css('.title::text').get()
            sale = i.css('.search_discount span::text').get()
            href = i.css('::attr(href)').get()
            platform = i.css('.platform_img::attr(class)').getall()
            for a in range(len(platform)):
                platform[a] = platform[a].replace("platform_img ", "").replace("win", "Windows").replace("mac", "macOS").replace("linux", "Linux")

            yield scrapy.Request(href, callback=self.parse_inside, meta = {'item': {
                'title': title, 
                'platform': platform,
                'sale' : sale,
                'href': href
            }}, cookies = {
                'birthtime': "1007161201",
                'lastagecheckage': "1-0-2002"
            })
            
        self.page += 1
        if self.page < 10:
            yield response.follow('https://store.steampowered.com/search/?tags=492?&page=' + str(self.page), self.parse)   

    