import urllib
#import pymysql this is for my side only but if you want to play around with SQL le me know I can show you how to connect.
import pandas as pd
import re
import urllib.request
from bs4 import BeautifulSoup
#import os

def user():
    """We can make this a bit nicer with list of course but OP.gg is 
    going to be changing things for new season so I will leave it like this for now so it can be a bit better to read"""
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
    return url(post_url) # This is returning our user region input and POST the url based on that input

def make_soup(get_url):
    """Here we are using the BeautifulSoup library to search for the classes relevant to our table metrics. It would be helpful to
    have the BeautifulSoup doc open and possibly the webpage so you can follow along better."""
    
    thepage = urllib.request.urlopen(get_url)
    soupdata = BeautifulSoup(thepage, "html.parser") # This is difficult to read but having the documentation open would be a great resource
    get_rank = soupdata.findAll('td', {"class" : "ranking-table__cell ranking-table__cell--rank"})
    get_summoner_name = soupdata.findAll('td', {"class" : "ranking-table__cell ranking-table__cell--summoner"})
    get_tier = soupdata.findAll('td', {"class" : "ranking-table__cell ranking-table__cell--tier"})
    get_LP = soupdata.findAll('td', {"class" : "ranking-table__cell ranking-table__cell--lp"})
    get_wr = soupdata.findAll('td', {"class" : "ranking-table__cell ranking-table__cell--winratio"})
    #print(get_rank[0])
    return get_data(get_rank,get_summoner_name,get_tier,get_LP,get_wr)

#Global Variable - This is great example on where we have to use a global var because of looping through webpages
resultset = {'rank_num' : [], 'summoner_name' : [], 'tier' : [], 'current_LP' : [], 'win_rate' : []}
def get_data(get_rank,get_summoner_name,get_tier,get_LP,get_wr):
    """We could take this a step further once OP.GG fixes a few bugs. Right now this only works on the NA server but next patch should fix bugs when loading the page"""
    
    rank_list, summoner_name_list, tier_list, lp_list, wr_list = [],[],[],[],[]
    for rank, summoner_name, tier, lp, wr in zip(get_rank,get_summoner_name,get_tier,get_LP,get_wr):
        rank_list.append(rank.text)
        summoner_name_list.append(summoner_name.span.text)
        tier_list.append(re.sub('\s+','',tier.text)) # re.sub might be a bit difficult to read but I am still testing with regex once I release the full version. This is just getting rid delimiters in the text.
        lp_list.append(re.sub('\s+','',lp.text))
        wr_list.append(re.sub('\s+','',wr.div.span.text))
    # This block of code is a bit difficult to understand at first but what we are doing is actually appending are list from above to our global variable
    resultset['rank_num'] += rank_list
    resultset['summoner_name'] += summoner_name_list
    resultset['tier'] += tier_list
    resultset['current_LP'] += lp_list
    resultset['win_rate'] += wr_list
    create_dataframe(resultset)
    # We don't use a return at the end of our function because Python is executing our pages one by one so it would only send the last page.
    
def create_dataframe(resultset): # We are passing our dict global var from get_data()
    """This gets all of our data that was stored in resultset and creates a dataframe for us to use"""
    df = pd.DataFrame(data=resultset)
    df = df.reset_index(drop=True)
    #print(df)
    #os.chdir(r"C:/Users/Root/Desktop/LOL")
    df.to_excel("LeagueTest.xlsx",index=False) # We can send our user input here and create logic statements and fully automate the process


def url(post_url):
    """This gets our user input based on what region they want"""
    pages = [str(i) for i in range(1,21)] # EATS UP RAM!!! Please be aware (range(first_page, last_page + 1)) 
    for page in pages:
        get_url = post_url + page
        make_soup(get_url)
user()
