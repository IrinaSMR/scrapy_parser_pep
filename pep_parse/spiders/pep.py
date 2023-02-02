import scrapy

from pep_parse.items import PepParseItem


class PepSpider(scrapy.Spider):
    name = 'pep'
    allowed_domains = ['peps.python.org']
    start_urls = ['https://peps.python.org/']

    def parse(self, response):
        """Собирает ссылки на документы Pep."""
        tbody = response.css('tbody')

        for tr in tbody.css('tr'):
            link_pep_page = tr.css('td').css('a::attr(href)').get()
            if link_pep_page is not None:
                yield response.follow(
                    link_pep_page + '/',
                    callback=self.parse_pep
                )

    def parse_pep(self, response):
        """Парсит отдельную страницу Pep."""
        title = response.css('h1.page-title::text').get()
        data = {
            'number': title.partition(' – ')[0].replace('PEP ', ''),
            'name': title,
            'status': (
                response.css('dt:contains("Status") + dd abbr::text').get()
            )
        }
        yield PepParseItem(data)
