# -*- coding: utf-8 -*-
import scrapy


class SummonerSpider(scrapy.Spider):
    name = 'summoner'
    allowed_domains = ['http://lan.op.gg/summoner/userName=oca159']
    start_urls = ['http://lan.op.gg/summoner/userName=oca159']

    def parse(self, response):
        def extract_first_with_css(query, context=response):
            return context.css(query).extract_first().strip()

        def extract_all_with_css(query, context=response):
            return context.css(query).extract()

        def re_first_with_css(query, regex, context=response):
            return context.css(query).re_first(regex).strip()

        def re_all_with_css(query, regex, context=response):
            return context.css(query).re(regex)

        def get_most_played_champions():
            champion_box = response.css(".ChampionBox.Ranked")
            most_played_champions = []
            for champion in champion_box:
                most_played_champions.append({
                    "name": extract_first_with_css(".ChampionName::attr(title)", champion),
                    "winratio": extract_first_with_css(".WinRatio::text", champion),
                    "kda": extract_first_with_css("span.KDA::text", champion),
                })
            return most_played_champions

        yield {
            "name": extract_first_with_css("span.Name::text"),
            "elo": extract_first_with_css("span.tierRank::text"),
            "lp": extract_first_with_css("span.LeaguePoints::text"),
            "wins": extract_first_with_css("span.wins::text"),
            "losses": extract_first_with_css("span.losses::text"),
            "winratio": re_first_with_css("span.winratio::text", "(\d+%)"),
            "most_played_champions": get_most_played_champions(),
        }
