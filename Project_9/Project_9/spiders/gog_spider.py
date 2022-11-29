import scrapy

class GogSpider(scrapy.Spider):
    def parse_inside(self, response):
        item = response.meta['item']

        rows = response.css('.details__content.table__row-content')

        item['author'] = rows[4].css('a::text').getall()[0]
        item['genre'] = rows[0].css('a::text').getall()

        item['platform'] = response.css('svg.ic-svg.productcard-os-support__system::attr(class)').getall()

        for i in range(len(item['platform'])):
            item['platform'][i] = item['platform'][i].split(' ')[2].replace('productcard-os-support__system--', '').replace("windows", "Windows").replace("osx", "macOS").replace("linux", "Linux")

        return item

    name = 'gog_spider'
    start_urls = ['https://www.gog.com/en/games?tags=indie']
    page = 1

    def parse(self, response):

        for i in response.css('a.product-tile'):
            title = i.css('.product-tile__title::attr(title)').get()
            price = i.css('price-value .final-value::text').get()
            sale = i.css('price-discount::text').get()
            if sale is None:
                sale = '-0%'
            href = i.css('::attr(href)').get()

            if price is None:
                price = 'free'

            yield scrapy.Request(href, callback=self.parse_inside, meta = {'item': {
                'title': title,
                'price': price,
                'sale': sale,
                'href': href
            }})


        


        if self.page < 20:
            self.page += 1
            yield response.follow('https://www.gog.com/en/games?tags=indie&page=' + str(self.page), self.parse)    