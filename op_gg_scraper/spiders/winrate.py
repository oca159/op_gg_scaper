# -*- coding: utf-8 -*-

import scrapy


class WinrateSpider(scrapy.Spider):
    name = 'winrate'
    
    def start_requests(self):
        url = 'http://op.gg/champion/ajax/statistics/trendChampionList/type=winratio'
        headers = {
            'X-Requested-With': 'XMLHttpRequest',
        }
        yield scrapy.Request(url, headers=headers)

    def parse(self, response):
        
        def get_winrate_list(role):
            winrate_list = response.xpath(f"//tbody[contains(@class, '{role}')]/tr")
            champions = []
            for champion in winrate_list:
                winrate, pickrate = champion.xpath("./td[contains(@class, 'value')]/text()").extract()[:2]
                champions.append({
                    "position": champion.xpath("./td[contains(@class, 'rank')]/text()")
                        .extract_first(default="Not found").strip(),
                    "name": champion.xpath(".//div[contains(@class, 'name')]/text()")
                        .extract_first(default="Not found").strip(),
                    "winrate": winrate,
                    "pickrate": pickrate,

                })
            return champions

        yield {
            "all": get_winrate_list("ALL"),
            "top": get_winrate_list("TOP"),
            "jungle": get_winrate_list("JUNGLE"),
            "mid": get_winrate_list("MID"),
            "adc": get_winrate_list("ADC"),
            "support": get_winrate_list("SUPPORT"),
        }
