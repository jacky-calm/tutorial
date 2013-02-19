from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector

class HouseSpider(BaseSpider):
    name = "house"
    allowed_domains = ["soufun.com"]
    start_urls = [
        #"http://newhouse.sh.soufun.com/house/web/Search_Result.php"
        "http://newhouse.sh.soufun.com/house/%C9%CF%BA%A3______%D7%A1%D5%AC__________1_1_.htm"
    ]

    def extract(self, select):
        return unicode.encode(select.extract()[0], 'utf-8')

    def parseDistricts(self, response):
        filename = "newhouse-districts.htm"
        out = open(filename, 'wb')
        hxs = HtmlXPathSelector(response)
        sites = hxs.select('//div[@class="s3"]/a')
        total = 0
        for site in sites:
          name = self.extract(site.select('text()'))
          link = self.extract(site.select('@href'))
          print name, link
          out.write(" ".join((name, link, "</br>")))
          total += 1
          if total==18:
            break

    def parseList(self, response):
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

    def parse(self, response):
        self.parseDistricts(response)
