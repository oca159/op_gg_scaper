# -*- coding: utf-8 -*-
import scrapy


class SummonerSpider(scrapy.Spider):
    name = 'summoner'
    regions = ["lan", "las", "br", "euw", "na"]

    def start_requests(self):
        username = getattr(self, 'username', 'oca159')
        region = getattr(self, 'region', None)
        url = f'http://op.gg/summoner/userName={username}'
        if region is not None and region in self.regions:
            url = f'http://{region}.op.gg/summoner/userName={username}'
        yield scrapy.Request(url)

    def parse(self, response):

        def get_most_played_champions():
            champion_box = response.css(".ChampionBox.Ranked")
            most_played_champions = []
            for champion in champion_box:
                most_played_champions.append({
                    "name": champion.css(".ChampionName::attr(title)").extract_first(default="Not found").strip(),
                    "winratio": champion.css(".WinRatio::text").extract_first(default="Not found").strip(),
                    "kda": champion.css("span.KDA::text").extract_first(default="Not found").strip(),
                })
            return most_played_champions

        yield {
            "name": response.css("span.Name::text").extract_first(default="Not found").strip(),
            "elo": response.css("span.tierRank::text").extract_first(default="Not found").strip(),
            "lp": response.css("span.LeaguePoints::text").extract_first(default="Not found").strip(),
            "wins": response.css("span.wins::text").extract_first(default="Not found").strip(),
            "losses": response.css("span.losses::text").extract_first(default="Not found").strip(),
            "winratio": response.css("span.winratio::text").re_first("(\d+%)", default="Not found").strip(),
            "most_played_champions": get_most_played_champions(),
        }
