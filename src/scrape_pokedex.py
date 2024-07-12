from bs4 import BeautifulSoup
import requests
import pandas as pd
import sqlite3
import os
import plotly.express as px


class ScraperURL:
    '''
        Scrapes table from the provided url with the specified table from the 
        page from that url.
    '''

    def __init__(self):
        self.url = 'https://pokemondb.net/pokedex/all'
        # self.df = None


    def request_page(self):
        '''
            Create HTML request from the given URL and extract HTML code.
        '''
        pass

    
    def find_table(self):
        '''
            From the extracted page, extract the target table.
        '''
        pass


    def find_headers(self):
        '''
            From the table, separate the headers.
            Then store it to a data frame
        '''
        pass


    def find_data_row(self):
        '''
            From the table, extract rows of data.
            Then store it in the same data frame.
        '''
        pass


    def create_db_conn(self):
        '''
            Create connection with the database.
        '''
        pass


    def load_df_to_csv(self):
        '''
            Load data frame to csv.
        '''
        pass


def main():
    scrap = ScraperURL()

    


if __name__ == '__main__':
    main()