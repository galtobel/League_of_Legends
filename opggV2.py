import urllib
import pymysql
import pandas as pd
import re
import urllib.request
from bs4 import BeautifulSoup
import os
from string import ascii_lowercase

def user():
    region_input = input("Welcome! This is a simple script that scrapes op.gg for the top 2000 players across each region. All you need to do is input what region you will like (NA,KR,JP,EUW,EUNE,OCE,BR,LAS,LAN,RU,TR)")
    if region_input == "NA":
        post_url = "http://na.op.gg/ranking/ladder/page="

    elif region_input == "KR":
        post_url = "http://www.op.gg/ranking/ladder/page="

    elif region_input == "JP":
        post_url = "http://jp.op.gg/ranking/ladder/page="

    elif region_input == "EUW":
        post_url = "http://euw.op.gg/ranking/ladder/page="

    elif region_input == "EUNE":
        post_url = "http://eune.op.gg/ranking/ladder/page="

    elif region_input == "OCE":
        post_url = "http://oce.op.gg/ranking/ladder/page="

    elif region_input == "BR":
        post_url = "http://br.op.gg/ranking/ladder/page="

    elif region_input == "LAS":
        post_url = "http://las.op.gg/ranking/ladder/page="

    elif region_input == "LAN":
        post_url = "http://lan.op.gg/ranking/ladder/page="
    
    elif region_input == "RU":
        post_url = "http://ru.op.gg/ranking/ladder/page="
    
    elif region_input == "TR":
        post_url = "http://tr.op.gg/ranking/ladder/page="

    else:
        None
    return url(post_url)

def make_soup(get_url):
    """Here we are using the BeautifulSoup library to search for the classes relevant to our table metrics."""
    
    thepage = urllib.request.urlopen(get_url)
    soupdata = BeautifulSoup(thepage, "html.parser") # This is difficult to read but having the documentation open would be a great resource
    get_rank = soupdata.findAll('td', {"class" : "ranking-table__cell ranking-table__cell--rank"})
    get_summoner_name = soupdata.findAll('td', {"class" : "ranking-table__cell ranking-table__cell--summoner"})
    get_tier = soupdata.findAll('td', {"class" : "ranking-table__cell ranking-table__cell--tier"})
    get_LP = soupdata.findAll('td', {"class" : "ranking-table__cell ranking-table__cell--lp"})
    get_wr = soupdata.findAll('td', {"class" : "ranking-table__cell ranking-table__cell--winratio"})
    #print(get_rank[0])
    return get_data(get_rank,get_summoner_name,get_tier,get_LP,get_wr)

def get_data(get_rank,get_summoner_name,get_tier,get_LP,get_wr):
    """We could take this a step further once OP.GG fixes a few bugs. Right now this only works on the NA server but next patch should fix bugs when loading the page"""
    
    rank_list, summoner_name_list, tier_list, lp_list, wr_list = [],[],[],[],[]
    for rank, summoner_name, tier, lp, wr in zip(get_rank,get_summoner_name,get_tier,get_LP,get_wr):
        rank_list.append(rank.text)
        summoner_name_list.append(summoner_name.span.text)
        tier_list.append(re.sub('\s+','',tier.text)) # re.sub might be a bit difficult to read but I am still testing with regex once I release the full version. This is just getting rid delimiters in the text.
        lp_list.append(re.sub('\s+','',lp.text))
        wr_list.append(re.sub('\s+','',wr.div.span.text))
    #print(rank_list)
    return create_dataframe(rank_list, summoner_name_list, tier_list, lp_list, wr_list)

def create_dataframe(rank_list, summoner_name_list, tier_list, lp_list, wr_list): 
    """This gets all of our data that we scraped and stores into a pandas dataframe"""
    df = pd.DataFrame({'rank_num' : rank_list, 'summoner_name' : summoner_name_list, 'tier' : tier_list, 'current_LP' : lp_list, 'win_rate' : wr_list})
    df = df.reset_index(drop=True)
    #print(df)
    #os.chdir(r"C:/Users/Root/Desktop/LOL")
    #df.to_excel("LeagueTest.xlsx")

def url(post_url):
    """This gets our user input based on what region they want"""
    pages = [str(i) for i in range(1,2)]
    for page in pages:
        get_url = post_url + page
        make_soup(get_url)
user()
