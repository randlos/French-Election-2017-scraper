import scrapy
from frosch.items import com, dep
from geopy.geocoders import Nominatim

class frosch(scrapy.Spider):
    name = 'communes'
    allowed_domains = ['http://elections.interieur.gouv.fr/']
    start_urls = [
        'http://elections.interieur.gouv.fr/presidentielle-2017/',
    ]

    def start_requests(self):

        for baseurl in self.start_urls:
            yield scrapy.Request(baseurl, callback=self.dep_links)


    def dep_links(self, response):

        for regionURL in response.xpath("//*[@id='listeDpt']/option/@value").extract():
            if regionURL != "#":
                url = response.url + regionURL
                yield scrapy.Request(url, callback=self.dep, dont_filter=True)


    def dep(self, response):


        for url in self.start_urls:
            baseurl = url

        for sub_regionURL in response.xpath('//div[@class="row-fluid pub-index-communes"]//a/@href').extract():
            scrapeURL = sub_regionURL.replace("../../", "")
            url =  baseurl + scrapeURL
            yield scrapy.Request(url, callback=self.commune_links, dont_filter=True)

        #self.logger.info('A response from %s just arrived!', response.url)

    def commune_links(self, response):
        for url in self.start_urls:
            baseurl = url

        for url in response.xpath('//table[@class="table table-bordered tableau-communes"]//td//@href').extract():
            url = url.replace("../../", "")
            parse_url = baseurl + url
            yield scrapy.Request(parse_url, callback=self.parse, dont_filter=True)




    def parse(self, response):

        commune = com()
        sel = response.selector

        commune['commune'] = response.xpath('//*[@id="top"]/div[2]/div[1]/div[4]/div/h3[1]/text()').extract_first()

        geolocator = Nominatim()
        adress = commune['commune'] + ', FR'
        location = geolocator.geocode(adress)
        commune['location'] = location.latitude, location.longitude

        for tr in sel.xpath("//table[contains(@class, 'tableau-resultats-listes-ER')]/tbody/tr"):
            commune['kandidat'] = tr.xpath('td[1]/text()').extract_first()
            commune['stimmen'] = tr.xpath('td[2]/text()').extract_first()
            prozent = tr.xpath('td[4]/text()').extract_first()
            commune['prozent'] = prozent.strip()
            yield commune
