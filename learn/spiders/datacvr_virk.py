import scrapy
from convert import *
from convert import sample


class DatacvrVirkSpider(scrapy.Spider):
    name = 'datacvr_virk'
    allowed_domains = ['datacvr.virk.dk', 'virk.queue-it.net']
    start_urls = ['https://datacvr.virk.dk/data/index.php?antal_ansatte=null&region=hovedstaden%2Csjaelland'
                  '%2Csyddanmark%2Cmidtjylland%2Cnordjylland%2Cgroenland&soeg=&q=visninger&language=en-gb']

    base_url = 'https://datacvr.virk.dk'
    page_count = 150
    count = 0

    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/93.0.4577.82 YaBrowser/21.9.1.686 Yowser/2.5 Safari/537.36 '
    }

    def parse(self, response, **kwargs):
        self.count += 1
        cvrs = response.xpath("//div[@class='cvr']/p[2]/text()").extract().rstrip()
        if self.count < self.page_count:
            # print(cvrs)
            for cvr in cvrs:
                print(cvr)
                unit_url = f"https://datacvr.virk.dk/data/index.php?antal_ansatte=null&enhedstype=virksomhed&id={cvr}&region=hov&q=visenhed&language=en-gb"
                yield scrapy.Request(unit_url, headers=self.headers, callback=self.parse_unit)

            next_url = f'https://datacvr.virk.dk/data/index.php?page={self.count}antal_ansatte=null&region=hovedstaden%2Csjaelland%2Csyddanmark%2Cmidtjylland%2Cnordjylland%2Cgroenland&soeg=&q=visninger&language=en-gb'
            yield scrapy.Request(next_url, headers=self.headers, callback=self.parse)

    def parse_unit(self, response, **kwargs):
        info = sample
        company_name = response.xpath("//div[@class='enhedsnavn']/h1/text()").extract_first()
        if company_name:
            info['company_name'] = company_name
        # convert
        table1 = response.xpath("//div[@class='table stamdata']/div/div[1]/h2/strong/text()").extract()
        table2 = response.xpath("//div[@class='table stamdata']/div/div[2]").extract()
        info = convert(table1, table2, information=info)
        # convert
        table3 = response.xpath("//div[@id='collapse_-Flere-Stamdata']/div/div/div[1]/h2/strong/text()").extract()
        table4 = response.xpath("//div[@id='collapse_-Flere-Stamdata']/div/div/div[2]").extract()
        info = convert(table3, table4, dict='expanded_business_information', information=info)
        # convert_power_to_bind_and_key_individuals_and_auditor
        # table5 = response.xpath("//div[@id='collapse_-Tegningsregel-personkreds-og-revisor']/div/div/div[1]/h2/strong/text()").extract()
        # table6 = response.xpath("//div[@id='collapse_-Tegningsregel-personkreds-og-revisor']/div/div/div[2]").extract()
        # info = convert_power_to_bind_and_key_individuals_and_auditor(table5, table6, information=info)
        # convert_ownership
        # table7 = response.xpath("//div[@id='collapse_-Ejerforhold']/div/div/div[1]/h2/strong/text()").extract()
        # table8 = response.xpath("//div[@id='collapse_-Ejerforhold']/div/div/div[2]/div").extract()
        # info = convert_ownership(table7, table8, information=info)
        # convert information_on_main_company
        table9 = response.xpath("//div[@id='collapse_-Oplysninger-om-hovedselskab']/div/div/div[1]/h2/strong/text()").extract()
        table10 = response.xpath("//div[@id='collapse_-Oplysninger-om-hovedselskab']/div/div/div[2]").extract()
        info = convert(table9, table10, dict='information_on_main_company', information=info)
        # convert production_units
        table11 = response.xpath("//div[@class='virksomheds-penheder']/div/div/div[1]/h2/strong/text()").extract()
        table12 = response.xpath("//div[@class='virksomheds-penheder']/div/div/div[2]").extract()
        info = convert(table11, table12, dict='production_units', information=info)
        # convert_history
        table13 = response.xpath("//div[@id='collapse_-Historisk']/div/div/div").extract()
        info = convert_history(table13, information=info)
        yield info


