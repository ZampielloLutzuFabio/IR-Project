import scrapy

class SteamSpider(scrapy.Spider):
    def parse_inside(self, response):
        item = response.meta['item']
        item['author'] = response.css('.dev_row a::text').get()
        item['genre'] = response.css(".popular_tags a::text").getall()
        for i in range(len(item['genre'])):
            item['genre'][i] = item['genre'][i].strip() 
        return item
    
    name = 'steam_spider'
    page = 1
    start_urls = ['https://store.steampowered.com/search/?tags=492?&page=' + str(page)]
    def parse(self, response):
        
        for i in response.css('.search_result_row'):
            title = i.css('.title::text').get()
            
            platform = i.css('.platform_img::attr(class)').getall()
            sale = i.css('.search_discount span::text').get()
            if sale is None:
                price = i.css('.search_price::text').get().strip().replace(",", ".")
            else:
                price = i.css('.search_price strike::text').get().strip().replace("\u20ac", "").replace(",", ".")
                price = str(round(float(price) - abs((float(sale.strip('%'))/100) * float(price)), 2)) + "\u20ac"
            href = i.css('::attr(href)').get()
            for a in range(len(platform)):
                platform[a] = platform[a].replace("platform_img ", "").replace("win", "Windows").replace("mac", "macOS").replace("linux", "Linux")

            yield scrapy.Request(href, callback=self.parse_inside, meta = {'item': {
                'title': title, 
                'platform': platform,
                'price' : price,
                'sale' : sale,
                'href': href
            }}, cookies = {
                'birthtime': "1007161201",
                'lastagecheckage': "1-0-2002"
            })
            
        self.page += 1
        if self.page < 10:
            yield response.follow('https://store.steampowered.com/search/?tags=492?&page=' + str(self.page), self.parse)   

    