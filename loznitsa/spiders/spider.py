import scrapy
from scrapy.exceptions import CloseSpider

from scrapy.loader import ItemLoader
import re

from w3lib.html import remove_tags

from ..items import LoznitsaItem


class LoznitsaSpider(scrapy.Spider):
	name = 'loznitsa'
	start_urls = ['http://old.loznitsa.bg/news.php']
	page = 0

	def parse(self, response):
		post_links = response.xpath('//div[@class="news-footer"]/a[text() = "Прочети повече"]/@href')
		yield from response.follow_all(post_links, self.parse_post)

		self.page += 9
		next_page = f'news.php?rowstart={self.page}'

		if not post_links:
			raise CloseSpider('no more pages')

		yield response.follow(next_page, self.parse)

	def parse_post(self, response):
		title = response.xpath('//h2/text()').get()
		description = response.xpath('//div[@class="panelbody"]/div[@class="floatfix"]/p').getall()
		description = remove_tags(''.join(description)).strip()
		date = response.xpath('(//div[@class="news-footer"]/text())[3]').get()[4:]
		date = re.sub('·', '', date).strip()

		item = ItemLoader(item=LoznitsaItem(), response=response)
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
