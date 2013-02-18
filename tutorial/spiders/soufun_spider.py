from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector

class DmozSpider(BaseSpider):
    name = "soufun"
    allowed_domains = ["soufun.com"]
    start_urls = [
        "http://newhouse.sh.soufun.com/house/%C9%CF%BA%A3_________________1_.htm"
    ]

    def extract(self, select):
        return unicode.encode(select.extract()[0], 'utf-8')

    def parse(self, response):
        filename = "newhouse.htm"
        out = open(filename, 'wb')

        hxs = HtmlXPathSelector(response)
        sites = hxs.select('//ul/li[@class="s1"]')
        for site in sites:
          name = self.extract(site.select('div/a/text()'))
          house_type = self.extract(site.select('div[@class="dot6"]/text()'))
          print name, house_type
          out.write(" ".join((name, house_type)))
