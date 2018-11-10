import urllib
import pymysql
import pandas as pd
import re
import urllib.request
from bs4 import BeautifulSoup
import os
from string import ascii_lowercase

def make_soup(get_url):
    """Here we are using the BeautifulSoup library to search for the classes relevant to our table metrics."""
    thepage = urllib.request.urlopen(get_url)
    soupdata = BeautifulSoup(thepage, "html.parser") # This is difficult to read but having the documentation open would be a great resource
    get_rank = soupdata.findAll('td', {"class" : "ranking-table__cell ranking-table__cell--rank"})
    get_summoner_name = soupdata.findAll('td', {"class" : "ranking-table__cell ranking-table__cell--summoner"})
    get_tier = soupdata.findAll('td', {"class" : "ranking-table__cell ranking-table__cell--tier"})
    get_LP = soupdata.findAll('td', {"class" : "ranking-table__cell ranking-table__cell--lp"})
    get_wr = soupdata.findAll('td', {"class" : "ranking-table__cell ranking-table__cell--winratio"})
    return get_data(get_rank,get_summoner_name,get_tier,get_LP,get_wr)

def get_data(get_rank,get_summoner_name,get_tier,get_LP,get_wr):
    """We could take this a step further once OP.GG fixes a few bugs. Right now this only works on the NA server but next patch should fix bugs when loading the page"""
    rank, summoner_name, tier, lp, wr = [0,0,0,0,0]
    rank_list, summoner_name_list, tier_list, lp_list, wr_list= [],[],[],[],[]
    while (rank < len(get_rank)) and (summoner_name < len(get_summoner_name)) and (tier < len(get_tier)) and (lp < len(get_LP)) and (wr < len(get_wr)):
        contains1 = get_rank[rank]
        rank += 1
        rank_list.append(contains1.text)
        contains2 = get_summoner_name[summoner_name]
        summoner_name += 1
        summoner_name_list.append(contains2.span.text)
        contains3 = get_tier[tier]
        tier += 1
        tier_list.append(re.sub('\s+','',contains3.text)) # re.sub might be a bit difficult to read but I am still testing with regex once I release the full version. This is just getting rid delimiters in the text.
        contains4 = get_LP[lp]
        lp += 1
        lp_list.append(re.sub('\s+','',contains4.text))
        contains5 = get_wr[wr]
        wr += 1
        wr_list.append(re.sub('\s+','',contains5.div.span.text))
    #print(summoner_name_list)    
    df = pd.DataFrame({'rank_num' : rank_list, 'summoner_name' : summoner_name_list, 'tier' : tier_list, 'current_LP' : lp_list, 'win_rate' : wr_list})
    print(df)

def url():
    get_url = "http://na.op.gg/ranking/ladder/page=1" # It works for all pages but it's messy until op.gg updates. I will leave it at 1 for now and create loop in the full version.
    make_soup(get_url)
url()
