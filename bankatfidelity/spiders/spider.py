import scrapy

from scrapy.loader import ItemLoader

from ..items import BankatfidelityItem
from itemloaders.processors import TakeFirst


class BankatfidelitySpider(scrapy.Spider):
	name = 'bankatfidelity'
	start_urls = [
		'https://www.bankatfidelity.com/about/news/',
		'https://www.bankatfidelity.com/about/blog/',
	]

	def parse(self, response):
		post_links = response.xpath('//a[@class="btn read"]/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

	def parse_post(self, response):
		title = response.xpath('//h2[@class="page-title"]/text()').get()
		description = response.xpath('//div[@class="copy"]//text()[normalize-space()]').getall()
		description = [p.strip() for p in description if '{' not in p]
		description = ' '.join(description).strip()
		date = response.xpath('//div[@class="l-content"]/text()').get()

		item = ItemLoader(item=BankatfidelityItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
