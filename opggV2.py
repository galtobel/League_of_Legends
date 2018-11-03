import urllib
import re
import urllib.request
from bs4 import BeautifulSoup
import os
from string import ascii_lowercase

def make_soup(get_url):
    thepage = urllib.request.urlopen(get_url)
    soupdata = BeautifulSoup(thepage, "html.parser")
    get_rank = soupdata.findAll('td', {"class" : "ranking-table__cell ranking-table__cell--rank"})
    get_summoner_name = soupdata.findAll('td', {"class" : "ranking-table__cell ranking-table__cell--summoner"})
    get_tier = soupdata.findAll('td', {"class" : "ranking-table__cell ranking-table__cell--tier"})
    get_LP = soupdata.findAll('td', {"class" : "ranking-table__cell ranking-table__cell--lp"})
    get_wr = soupdata.findAll('td', {"class" : "ranking-table__cell ranking-table__cell--winratio"})
    return get_data(get_rank,get_summoner_name,get_tier,get_LP,get_wr)

def get_data(get_rank,get_summoner_name,get_tier,get_LP,get_wr):
    rank, summoner_name, tier, lp, wr = [0,0,0,0,0]
    while (rank < len(get_rank)) and (summoner_name < len(get_summoner_name)) and (tier < len(get_tier)) and (lp < len(get_LP)) and (wr < len(get_wr)):
        rank_list = []
        contains1 = get_rank[rank]
        rank += 1
        rank_list.append(contains1.text)
        summoner_name_list = []
        contains2 = get_summoner_name[summoner_name]
        summoner_name += 1
        summoner_name_list.append(contains2.span.text)
        tier_list = []
        contains3 = get_tier[tier]
        tier += 1
        tier_list.append(re.sub('\s+','',contains3.text))
        lp_list = []
        contains4 = get_LP[lp]
        lp += 1
        lp_list.append(re.sub('\s+','',contains4.text))
        wr_list = []
        contains5 = get_wr[wr]
        wr += 1
        wr_list.append(re.sub('\s+','',contains5.div.span.text))
        print(rank_list + summoner_name_list + tier_list + lp_list + wr_list)

def url():
    get_url = "http://na.op.gg/ranking/ladder/page=1"
    make_soup(get_url)
url()