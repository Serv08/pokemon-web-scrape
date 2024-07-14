from bs4 import BeautifulSoup
import requests
import pandas as pd
import sqlite3
import logging
import sys


class ScraperURL():
    '''
        Scrapes table from the provided url with the specified table from the 
        page from that url.
    '''

    # def __init__(self, path='/data', url='https://pokemondb.net/pokedex/all'):
    def __init__(self, path, url):
        self.url = url
        # self.filepath = r'C:\Users\SERVIN\Desktop\Important local files\Data Analyst\data'
        self.filepath = path
        self.logger = self.get_logger()
        self.error_handler = 0
        self.recon_try = 0


    def request_page(self):
        '''
            Create HTML request from the given URL and extract HTML code.
        '''
        try:
            page = requests.get(self.url)
            self.soup = BeautifulSoup(
                page.text,
                features='lxml'
                )
        except Exception as e:
            self.get_logger().error(f'request_page() error: {e}')
            self.error_handler += 1

    
    def find_table(self):
        '''
            From the extracted page, extract the target table.
        '''
        try:
            self.table = self.soup.find('table', class_ = "data-table sticky-header block-wide")
        except Exception as e:
            self.get_logger().error(f'find_table() error: {e}')
            self.error_handler += 1


    def find_headers(self):
        '''
            From the table, separate the headers.
            Then store it to a data frame
        '''
        try:
            titles = self.table.find_all('th')
            table_title_list = [title.text.strip() for title in titles]
            self.df = pd.DataFrame(columns= table_title_list)

        except Exception as e:
            self.get_logger().error(f'find_headers() error: {e}')
            self.error_handler += 1


    def find_data_row(self):
        '''
            From the table, extract rows of data.
            Then store it in the same data frame.
        '''
        try:
            columns_data = self.table.find_all('tr')   

            for row in columns_data[1:]:
                row_data = row.find_all('td')
                indiv_row_data = [data.text.strip() for data in row_data]

                row_length = len(self.df)
                self.df.loc[row_length] = indiv_row_data

        except Exception as e:
            self.get_logger().error(f'find_data_row() error: {e}')
            self.error_handler += 1


    def create_db_conn(self):
        '''
            Create connection with the database. 
            Uses recursion to perform multiple tries in connecting to database.
        '''
        try:
            self.conn = sqlite3.connect(f'{self.filepath}/database.db')
            self.cursor = self.conn.cursor()

        except Exception as e:
            self.get_logger().error(f'find_table() error: {e}')
            self.recon_try += 1
            self.get_logger().warning(f'RECONNECTING... ({self.recon_try} tries)')
            
            if self.recon_try < 5:
                self.create_db_conn()
            else:
                raise ValueError

        except ValueError as e:
            self.get_logger().error(f'Cannot connect to database. Error: {e}')
            self.error_handler += 1


    def load_df_to_csv(self):
        '''
            Load data frame to csv.
        '''
        try:
            self.df.to_csv(f'{self.filepath}/poke_index_data.csv', index = False)

        except Exception as e:
            self.get_logger().error(f'load_df_to_csv() error: {e}')
            self.error_handler += 1


    def create_table_schema(self):
        '''
            Creates table schema. This is hardcoded and in need to be automated.
            TODO: Automate creating schema using {self.check_table_data_types()}
        '''
        self.create_table = '''CREATE TABLE IF NOT EXISTS pokemonData(
        '#' INTEGER NOT NULL,
        Name VARCHAR(40) NOT NULL,
        Type VARCHAR(40) NOT NULL,
        Total INTEGER NOT NULL,
        HP INTEGER NOT NULL,
        Attack INTEGER NOT NULL,
        Defense INTEGER NOT NULL,
        'Sp. Atk' INTEGER NOT NULL,
        'Sp. Def' INTEGER NOT NULL,
        Speed INTEGER NOT NULL);
        '''


    def load_df_to_db(self):
        '''
            Load csv to SQLite db.
        '''
        try:
            self.cursor.execute(self.create_table)
            self.conn.commit()
            self.df.to_sql('pokemonData', self.conn, if_exists='append', index = False)

        except Exception as e:
            self.get_logger().error(f'load_df_to_db() error: {e}')
            self.error_handler += 1


    def get_logger(self):
        '''Logs'''
        # Create a custom logger
        logger = logging.getLogger(__name__)
        
        # Check if logger has handlers to avoid duplicate logs
        if not logger.hasHandlers():
            # Set the logging level
            logger.setLevel(logging.DEBUG)
            
            # Create handlers
            c_handler = logging.StreamHandler()
            f_handler = logging.FileHandler('scraper.log')
            c_handler.setLevel(logging.DEBUG)
            f_handler.setLevel(logging.DEBUG)
            
            # Create formatters and add it to handlers
            c_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            c_handler.setFormatter(c_format)
            f_handler.setFormatter(f_format)
            
            # Add handlers to the logger
            logger.addHandler(c_handler)
            logger.addHandler(f_handler)
        
        return logger
    

    def check_table_data_types(self):
        '''
            Checks table data type to be used for creating table schema.
        '''
        # self.cursor.execute("PRAGMA table_info(pokemonData)")
        # table_info = self.cursor.fetchall()
        # for column in table_info:
        #     print(column)
        pass


def main(argv):
    file_path = './data'
    url = 'https://pokemondb.net/pokedex/all'

    if '-p' in argv:
        path_index = argv.index('-p') + 1
        if path_index < len(argv):
            file_path = argv[path_index]
    
    if '-u' in argv:
        url_index = argv.index('-u') + 1
        if url_index < len(argv):
            url = argv[url_index]

    scrap = ScraperURL(path=file_path, url=url)
    print(file_path, url)

    try:
        scrap.get_logger().info("EXECUTING FILE...\n")
        scrap.get_logger().info("Requesting page...")
        scrap.request_page()

        scrap.get_logger().info("Collecting headers...")
        scrap.find_table()
        scrap.find_headers()

        scrap.get_logger().info("Collecting data...")
        scrap.find_data_row()

        scrap.get_logger().info("Converting data frame to csv...")
        scrap.load_df_to_csv()

        scrap.get_logger().info("Creating db connection...")
        scrap.create_db_conn()

        scrap.get_logger().info("Creating table schema...")
        scrap.create_table_schema()

        scrap.get_logger().info("Converting data frame to db...")
        scrap.load_df_to_db()

        if scrap.error_handler == 0:
            scrap.get_logger().info("DONE!")
            scrap.get_logger().info(f"Data saved to {file_path}\n")
        else:
            scrap.get_logger().error("THERE WAS AN ERROR!\n")

    except Exception as e:
        scrap.get_logger().error(f'main() error: {e}')


if __name__ == "__main__":
    main(sys.argv[1:])
