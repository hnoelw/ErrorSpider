import scrapy
from scrapy.crawler import CrawlerProcess
import json


class MySpider(scrapy.Spider):
    name = "myspider"
    allowed_domains = ['nuruinternational.org']
    outfile = open("xperiencesites.json", 'w')
    def start_requests(self):
        yield scrapy.Request(
                "https://www.nuruinternational.org/",
                callback=self.parse,
                errback=self.errbackFun,
                dont_filter=True,
            )
       
    def parse(self, response):
        for href in response.xpath("//a/@href").getall():
            json_object = json.dumps({response.url: response.status})
            self.outfile.write(json_object)
            self.outfile.write("\n")
            yield scrapy.Request(response.urljoin(href), callback=self.parse, errback=self.errbackFun)
   
       
    def errbackFun(self, failure):
        response = failure.value.response
        json_object = json.dumps({response.url: response.status})
        self.outfile.write(json_object)
        self.outfile.write("\n")
process = CrawlerProcess(
    settings={
        "FEEDS": {
            "nurusites.json": {"format": "json"},
        },
    }
)


process.crawl(MySpider)
process.start()