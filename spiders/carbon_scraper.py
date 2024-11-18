import scrapy

class carbon38Spider(scrapy.Spider):
    name = 'carbon'
    start_urls = [
        'https://www.carbon38.com/shop-all-activewear/tops',
    ]
    
    def parse(self, response):
        for products in response.css('a.ProductItem__ImageWrapper::attr(href)'):
            yield response.follow(products.get(), callback=self.parse_products)

        next_page = response.css('a.Pagination__NavItem[rel="next"]::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)

    def parse_products(self, response):
        yield {
            'brand': response.css('h2.ProductMeta__Vendor a::text').get(),
            'primary_img_url': response.css('div.AspectRatio img::attr(src)').get(),
            'product_name': response.css('h1.ProductMeta__Title::text').get(),
            'price': response.css('span.ProductMeta__Price::text').get(),
            'colour': response.css('span.ProductForm__SelectedValue::text').get(),
            'sizes': response.css('label.SizeSwatch::text').getall(),
            'description': response.css('div.Faq__Answer p::text').get(),
            'product_id': response.css('status-save-button[product-id]::attr(product-id)').get(),
            'img_urls': response.css('a.Product__SlideshowNavImage img::attr(src)').getall(),
            'febric_and_care': response.css('div.Faq__Answer.Rte span.metafield-multi_line_text_field::text').get(),
        }

