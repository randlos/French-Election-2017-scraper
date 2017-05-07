import scrapy
from frosch.items import com, dep
from geopy.geocoders import Nominatim



class frosch(scrapy.Spider):
    name = 'departments'
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

        departement = dep()
        sel = response.selector

        dep_str = response.xpath('//*[@id="top"]/div[2]/div[1]/div[2]/div/a[3]/text()').extract_first()
        departement['departement'] = dep_str[:-5]

        geolocator = Nominatim()
        adress = departement['departement'] + ', FR'
        location = geolocator.geocode(adress)
        departement['location'] = location.latitude, location.longitude

        for tr in sel.xpath("//table[contains(@class, 'tableau-resultats-listes-ER')]/tbody/tr"):
            departement['kandidat'] = tr.xpath('td[1]/text()').extract_first()
            departement['stimmen'] = tr.xpath('td[2]/text()').extract_first()
            prozent = tr.xpath('td[4]/text()').extract_first()
            departement['prozent'] = prozent.strip()
            yield departement

