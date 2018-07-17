# -*- coding: utf-8 -*-

import scrapy


class TierSpider(scrapy.Spider):
    name = 'tier'
    start_urls = ['http://www.op.gg/champion/statistics']

    def parse(self, response):

        def get_tier_list(role):
            tier_list = response.xpath(f"//tbody[contains(@class,'tier-{role}')]/tr")
            champions = []
            for champion in tier_list:
                winrate, pickrate = champion.xpath("./td[contains(@class, 'value')]/text()").extract()[:2]
                champions.append({
                    "position": champion.xpath("./td[contains(@class, 'rank')]/text()").extract_first(default="Not found").strip(),
                    "name": champion.xpath(".//div[contains(@class, 'name')]/text()").extract_first(default="Not found").strip(),
                    "winrate": winrate,
                    "pickrate": pickrate,
                    "tier": champion.xpath("./td[contains(@class, 'value')]/img/@src").re_first("(\d+)", default="Not found").strip(),

                })
            return champions

        yield {
            "top": get_tier_list("TOP"),
            "jungle": get_tier_list("JUNGLE"),
            "mid": get_tier_list("MID"),
            "adc": get_tier_list("ADC"),
            "support": get_tier_list("SUPPORT"),
        }
