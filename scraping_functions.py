import requests
import dill as pickle
import pandas as pd
from bs4 import BeautifulSoup
import time

'''
actor_movie_table
The following function generates a list of lists consisting of the first table found on a particular
actor's boxofficemojo page

The movie_attribute protion of the code loops through the html table, capturing everything until the
table list generated by beautifulsoup ends

all_movies is the list of lists containing all movies found on the table on the actor's page
'''


def actor_movie_table(actor_page, all_movie_html_block):
    movie_table = []
    all_movies = []
    for x in range(1, len(all_movie_html_block)):
        movie_html_block = all_movie_html_block[x]
        movie_items = []
        for i in range(0, len(movie_html_block.find_all('td'))):
            movie_attribute = movie_html_block.find_all('td')[i].text
            movie_items.append(movie_attribute)
            try:
                movie_html = movie_html_block.find_all('td')[i].a['href']
            except:
                movie_html = ""
            #attribute_info = [movie_attribute, movie_html]
            movie_items.append(movie_html)
        movie_table.append(movie_items+[actor_page])
    all_movies = all_movies + movie_table
    return all_movies

'''
actor_page_loop loops through all actors on a list to capture their list of movies using the
actor_movie_table function

all_movies retrieves a list of lists consisting of all the movies found on all the actor's pages
'''

def actor_page_loop(actor_list):
    all_movies = []
    for row in actor_list:
        url = row[1]
        response = requests.get(url)
        while response.status_code != 200:
            if response.status_code == 403:
                break
            print "Waiting for webpage to respond"
            print url
            time.sleep(randint(1,10))
        page = response.text
        soup = BeautifulSoup(page)
        actor_page = row[0]
        try:
            movie_desc_block = soup.find_all('table')[1].find_all('tr')[0].find_all('td')[0].find_all('tr')
            movie_list = actor_movie_table(actor_page, movie_desc_block)
        except:
            movie_list = [['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '']]
        all_movies = all_movies + movie_list
    return all_movies

def movie_desc_table(movie_name, all_movie_html_block):
    movie_table = []
    movie_html_block = []
    movie_attribute = []
    movie_items = []
    movie = []
    contributor_desc = ""
    for x in range(len(all_movie_html_block)): #len(all_movie_html_block)
        movie_items = [] #this is cleared out as we reloop through the list to append new individual movie attributes
        movie_html_block = all_movie_html_block[x] #individual blocks from all_movie_html_block
        movie = movie_name
        for i in range(1, len(movie_html_block.find_all('a'))):
            movie_role = movie_html_block.find_all('a')[0].text
            name = movie_html_block.find_all('a')[i].text
            try:
                movie_html = movie_html_block.find_all('a')[i]['href']
            except:
                movie_html = ""
            movie_items =[movie, name, movie_role, movie_html] #movie_role, 
            movie_table.append(movie_items)
    return movie_table

def movie_page_loop(loop_df):
    nc_movies = []
    for row in loop_df:
        url = row
        response = requests.get(url)
        while response.status_code != 200:
            if response.status_code == 403:
                break
            print "Waiting for webpage to respond"
            print url
            time.sleep(randint(1,10))
        page = response.text
        soup = BeautifulSoup(page)
        #Sets the block that we are looking at that contains the contributors for the film
        try:
            movie_name = soup.find_all('b')[1].text
            movie_desc_block = soup.find(text = 'The Players').parent.parent.find_all('table')[0].find_all('tr')
            movie = movie_desc_table(movie_name, movie_desc_block)
        except:
            movie = [["","","",""]]
        nc_movies.append(movie)
    return nc_movies
