from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector

class DmozSpider(BaseSpider):
    name = "soufun"
    allowed_domains = ["soufun.com"]
    start_urls = [
        "http://newhouse.sh.soufun.com/house/web/Search_Result.php"
    ]

    def extract(self, select):
        return unicode.encode(select.extract()[0], 'utf-8')

    def parse(self, response):
        filename = "newhouse.htm"
        out = open(filename, 'wb')

        hxs = HtmlXPathSelector(response)
        sites = hxs.select('//div[@class="searchListNoraml"]')
        for site in sites:
          name = self.extract(site.select('div[@class="info"]/ul/li[@class="s1"]/div[@class="name"]/a/text()'))
          house_type = self.extract(site.select('div[@class="info"]/ul/li[@class="s1"]/div[@class="dot6"]/text()'))
          price = self.extract(site.select('div[@class="anther"]/div[@class="antherBox"]/div[@class="price"]/span[@class="price_type"]/text()'))
          print name, house_type, price
          out.write(" ".join((name, house_type, price)))
