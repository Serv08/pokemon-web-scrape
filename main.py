from bs4 import BeautifulSoup
import requests
import pandas as pd
import sqlite3
import logging


class ScraperURL():
    '''
        Scrapes table from the provided url with the specified table from the 
        page from that url.
    '''

    def __init__(self, url='https://pokemondb.net/pokedex/all', path=r'C:\Users\SERVIN\Desktop\Important local files\Data Analyst\scraped_data'):
        self.url = url
        self.filepath = path
        self.logger = self.get_logger()
        # self.df = None


    def request_page(self):
        '''
            Create HTML request from the given URL and extract HTML code.
        '''
        try:
            page = requests.get(self.url)
            self.soup = BeautifulSoup(page.text, 'html')
        except Exception as e:
            self.get_logger().error(f'request_page() error: {e}')

    
    def find_table(self):
        '''
            From the extracted page, extract the target table.
        '''
        try:
            self.table = self.soup.find('table', class_ = "data-table sticky-header block-wide")
        except Exception as e:
            self.get_logger().error(f'find_table() error: {e}')


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


    def find_data_row(self):
        '''
            From the table, extract rows of data.
            Then store it in the same data frame.
        '''
        try:
            columns_data = self.table.find_all('tr')   

            for row in columns_data[1:0]:
                row_data = row.find_all('td')
                indiv_row_data = [data.text.strip() for data in row_data]

                row_length = len(self.df)
                self.df.loc[row_length] = indiv_row_data

        except Exception as e:
            self.get_logger().error(f'find_data_row() error: {e}')


    def create_db_conn(self):
        '''
            Create connection with the database.
        '''
        recon_try = 0
        try:
            self.conn = sqlite3.connect(f'{self.filepath}\database.db')
            self.cursor = self.conn.cursor()

        except Exception as e:
            self.get_logger().error(f'find_table() error: {e}')
            recon_try += 1
            self.get_logger().warning(f'RECONNECTING... ({recon_try} tries)')
            self.create_db_conn()
            if recon_try >= 5:
                raise sqlite3.OperationalError
        
        except sqlite3.OperationalError as err:
            self.get_logger().error(f'Cannot connect to database. Error: {e}')


    def load_df_to_csv(self):
        '''
            Load data frame to csv.
        '''
        try:
            self.df.to_csv(f'{self.filepath}\poke_index_data.csv', index = True)

        except Exception as e:
            self.get_logger().error(f'load_df_to_csv() error: {e}')


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
            f_handler = logging.FileHandler(f'{self.filepath}\scraper.log')
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


    def main(self):
        try:
            self.get_logger().info("EXECUTING FILE...")
            self.get_logger().info("Requesting page...")
            self.request_page()

            self.get_logger().info("Collecting headers...")
            self.find_table()
            self.find_headers()

            self.get_logger().info("Collecting data...")
            self.find_data_row()

            self.get_logger().info("Converting data frame to csv...")
            self.load_df_to_csv()

            self.get_logger().info("Creating db connection...")
            self.create_db_conn()

            self.get_logger().info("Creating table schema...")
            self.create_table_schema()

            self.get_logger().info("Converting data frame to db...")
            self.load_df_to_db()

            self.get_logger().info("DONE!\n")

        except Exception as e:
            self.get_logger().error(f'main() error: {e}')


if __name__ == '__main__':
    scrap = ScraperURL()
    scrap.main()
    scrap.conn.close()
    scrap.get_logger().info("DB Connection closed!")
