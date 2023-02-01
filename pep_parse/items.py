import scrapy


class PepParseItem(scrapy.Item):
    """Описание модели для парсера Pep."""
    number = scrapy.Field()
    name = scrapy.Field()
    status = scrapy.Field()
