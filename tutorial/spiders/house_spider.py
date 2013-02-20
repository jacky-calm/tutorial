from scrapy.spider import BaseSpider
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector

from tutorial.items import HouseItem

class HouseSpider(BaseSpider):
    name = "house"
    allowed_domains = ["newhouse.sh.soufun.com"]
    start_urls = [
        "http://newhouse.sh.soufun.com/house/%C9%CF%BA%A3______%D7%A1%D5%AC__________1_1_.htm"
    ]

    def __init__( self):
      filename = "newhouse-districts.htm"
      self.out = open(filename, 'wb')

    def extract(self, select):
        return unicode.encode(select.extract()[0], 'utf-8')

    def parseDistricts(self, response):
        return self.parseDivLink(response, 's3')

    def parseComm(self, response):
        return self.parseDivLink(response, 's4')

    def parseDivLink(self, response, divClass):
        hxs = HtmlXPathSelector(response)
        sites = hxs.select('//div[@class="'+divClass+'"]/a')
        items = []
        for site in sites:
          name = self.extract(site.select('text()'))
          link = self.extract(site.select('@href'))
          print name, link
          item = HouseItem()
          item['title'] = name
          item['link'] = "http://newhouse.sh.soufun.com"+link
          items.append(item)

          self.out.write(" ".join((item['title'], item['link'], "</br>")))
          if '/house/%C9%CF%BA%A3_____%C6%E4%CB%FB_%D7%A1%D5%AC__________1_1_.htm'==link or 'GO'==name:
            break
        return items

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
        items = self.parseDistricts(response)
        for item in items:
          #yield item
          #self.out.write(" ".join((item['title'], item['link'], '</br>')))
          yield Request(item['link'], callback=self.parseComm)
